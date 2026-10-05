#!/usr/bin/env python3
"""
Low-level transaction codec for the Telekom (Microsoft Mediaroom) companion
protocol. Internal engine used by Remote; you normally don't touch this directly.

Ported byte-for-byte from the decompiled Android app. Verified against a real
captured pairing transaction (request body, URL hash, response decrypt).

Java class -> this module:
    c4.a  TaviranyitoCompanionShared   -> SBOX, compute_hash
    c4.b  TaviranyitoTransactionCodec  -> Codec
    d4.a  TaviranyitoBV4Key            -> StreamCipher
    d4.b  TaviranyitoCS64Key           -> CS64Key
    d4.c  TaviranyitoCSParve64         -> read/write helpers, keyed_digest
    d4.e  TaviranyitoHelper            -> (folded into Codec)
    d4.f  TaviranyitoMACHelper         -> block_encrypt/decrypt, cbc_mac, mac_mix
    d4.g  TaviranyitoWordSwapHelper    -> word_swap_fwd / word_swap_inv
    k4.a  TaviranyitoConverter         -> (inlined)

Naming: Java used obfuscated field names (f5638a, j6, iArr4...). Where a value has
a clear role it is named for that role; the mapping to the original is noted inline.
"""

from __future__ import annotations

MASK32 = 0xFFFFFFFF
MASK64 = 0xFFFFFFFFFFFFFFFF

# three fixed mixing constants baked into the protocol (c4 passes C|1, D|1, E|1)
CONST_C = 1206402005
CONST_D = 2418584567
CONST_E = 3864493069

# fixed bootstrap companion id used during pairing (model.b.o)
BOOTSTRAP_CID = "E7AAEC8C-F035-488a-AB39-C9A40547459F"
DEFAULT_PORT = 53208

# 256-entry substitution box (c4.a.f3934a)
SBOX = [
    48,
    179,
    102,
    100,
    0,
    1,
    0,
    0,
    18,
    112,
    89,
    255,
    158,
    237,
    151,
    7,
    201,
    249,
    254,
    152,
    232,
    21,
    90,
    96,
    183,
    210,
    187,
    12,
    165,
    236,
    200,
    135,
    8,
    226,
    155,
    239,
    93,
    110,
    121,
    35,
    135,
    95,
    239,
    165,
    170,
    47,
    156,
    99,
    135,
    43,
    119,
    196,
    126,
    199,
    226,
    134,
    160,
    190,
    53,
    136,
    23,
    49,
    195,
    211,
    186,
    140,
    88,
    146,
    104,
    218,
    249,
    178,
    149,
    135,
    211,
    11,
    107,
    131,
    155,
    175,
    143,
    125,
    17,
    111,
    201,
    149,
    13,
    177,
    91,
    125,
    187,
    104,
    239,
    94,
    243,
    124,
    33,
    46,
    36,
    214,
    0,
    130,
    55,
    72,
    45,
    55,
    4,
    183,
    39,
    250,
    120,
    97,
    225,
    13,
    214,
    113,
    216,
    229,
    12,
    3,
    52,
    251,
    164,
    33,
    113,
    117,
    57,
    67,
    85,
    249,
    41,
    10,
    4,
    173,
    70,
    31,
    20,
    159,
    110,
    84,
    199,
    141,
    16,
    224,
    176,
    250,
    136,
    0,
    72,
    35,
    85,
    210,
    117,
    15,
    121,
    36,
    129,
    131,
    86,
    76,
    46,
    243,
    53,
    161,
    133,
    204,
    3,
    164,
    118,
    42,
    235,
    222,
    70,
    250,
    25,
    153,
    81,
    162,
    180,
    158,
    162,
    32,
    41,
    158,
    173,
    210,
    106,
    32,
    40,
    71,
    109,
    112,
    4,
    104,
    187,
    200,
    136,
    41,
    81,
    210,
    82,
    139,
    197,
    64,
    115,
    222,
    216,
    87,
    191,
    174,
    174,
    150,
    238,
    10,
    40,
    119,
    13,
    118,
    244,
    82,
    250,
    152,
    68,
    112,
    250,
    17,
    50,
    198,
    77,
    254,
    252,
    59,
    69,
    120,
    89,
    28,
    109,
    58,
    136,
    82,
    26,
    66,
    129,
    13,
    232,
    103,
    175,
    5,
    20,
    192,
    7,
    194,
    233,
    128,
    173,
    33,
]
assert len(SBOX) == 256


# ------------------------------------------------------------------ byte helpers (d4.c)
def read_u32(buf, off):  # c.h : 4 bytes, big-endian -> unsigned 32-bit
    return ((buf[off] << 24) | (buf[off + 1] << 16) | (buf[off + 2] << 8) | buf[off + 3]) & MASK32


def read_u64(buf, off):  # c.i : 8 bytes, big-endian -> unsigned 64-bit
    value = 0
    for k in range(8):
        value = (value << 8) | (buf[off + k] & 0xFF)
    return value & MASK64


def write_u32(value, buf, off):  # c.j
    value &= MASK32
    buf[off] = (value >> 24) & 0xFF
    buf[off + 1] = (value >> 16) & 0xFF
    buf[off + 2] = (value >> 8) & 0xFF
    buf[off + 3] = value & 0xFF


def write_u64(value, buf, off):  # c.k
    value &= MASK64
    for k in range(8):
        buf[off + k] = (value >> (56 - 8 * k)) & 0xFF


def high32(x):  # c.e : upper 32 bits of a 64-bit value
    return (x >> 32) & MASK32


def low32(x):  # c.f : lower 32 bits
    return x & MASK32


def join64(high, low):  # c.g : (high << 32) | low
    return (((high & MASK32) << 32) | (low & MASK32)) & MASK64


def rotl8(byte):  # rotate an 8-bit value left by 1
    return ((byte << 1) | (byte >> 7)) & 0xFF


def rotr8(byte):  # rotate right by 1
    return ((byte << 7) | (byte >> 1)) & 0xFF


def swap_halves32(word):  # g.c : swap the two 16-bit halves of a 32-bit word
    return ((word << 16) | (word >> 16)) & MASK32


# ------------------------------------------------------------------ 8-byte block cipher (d4.f)
def block_encrypt(key, sbox, block):  # f.e : 8 rounds, in place on an 8-byte block
    for round_ in range(8, 0, -1):
        pos = 0
        while pos < 7:
            nxt = pos + 1
            mixed = (block[nxt] + sbox[(key[pos] + block[pos] + round_) & 255]) & 255
            block[nxt] = rotl8(mixed)
            pos = nxt
        mixed = (block[0] + sbox[(key[7] + block[7] + round_) & 255]) & 255
        block[0] = rotl8(mixed)


def block_decrypt(key, sbox, block):  # f.d : inverse of block_encrypt
    for round_ in range(1, 9):
        block[0] = (rotr8(block[0]) - sbox[(key[7] + block[7] + round_) & 255]) & 255
        for pos in range(6, -1, -1):
            nxt = pos + 1
            block[nxt] = (rotr8(block[nxt]) - sbox[(key[pos] + block[pos] + round_) & 255]) & 255


def cbc_mac(key, sbox, data, length):  # f.c : XOR each 8-byte block in, encrypt, repeat
    acc = [0] * 8
    for block_idx in range(length // 8):
        for i in range(8):
            acc[i] ^= data[block_idx * 8 + i]
        block_encrypt(key, sbox, acc)
    return read_u64(acc, 0)


def _mersenne_reduce(x):  # f.a : reduce a 64-bit value modulo 2^31 - 1
    high = high32(x)
    low = low32(x)
    doubled = (high << 1) & MASK32
    if doubled >= 0x7FFFFFFF:
        doubled = (doubled - 0x7FFFFFFF) & MASK32
    if low >= 0x7FFFFFFF:
        low -= 0x7FFFFFFF
    total = (doubled + low) & MASK32
    if total >= 0x7FFFFFFF:
        total = (total - 0x7FFFFFFF) & MASK32
    return total


def mac_mix(data, length, seed, const_c, const_d, const_e):  # f.b : auth-hash mixing stage
    word_count = length // 4
    seed_lo = _mersenne_reduce(low32(seed))
    seed_hi = _mersenne_reduce(high32(seed))
    even = _mersenne_reduce(
        (seed_lo * _mersenne_reduce((const_e * read_u32(data, 0)) & MASK64) + seed_hi) & MASK64
    )
    acc = even & MASK64
    odd = _mersenne_reduce(
        (const_c * _mersenne_reduce((even + read_u32(data, 4)) & MASK64) + const_d) & MASK64
    )
    acc = (acc + odd) & MASK64
    pair_idx = 1
    word_idx = 2
    while pair_idx < (word_count >> 1):
        next_word = word_idx + 1
        term = const_e * read_u32(data, word_idx << 2) + odd
        even = _mersenne_reduce((seed_lo * _mersenne_reduce(term & MASK64) + seed_hi) & MASK64)
        acc = (acc + even) & MASK64
        odd = _mersenne_reduce(
            (const_c * _mersenne_reduce((even + read_u32(data, next_word << 2)) & MASK64) + const_d)
            & MASK64
        )
        acc = (acc + odd) & MASK64
        pair_idx += 1
        word_idx = next_word + 1
    tail = odd + seed_hi
    return join64(
        low32(_mersenne_reduce((acc + const_d) & MASK64)), low32(_mersenne_reduce(tail & MASK64))
    )


# ------------------------------------------------------------------ CS64 polynomial key (d4.b)
def _ext_gcd32(a, b):  # b.c : extended Euclid, returns the two Bezout coefficients
    cur_a = a
    coef_x, prev_x = 1, 0
    coef_y, prev_y = 1, 0
    cur_b = b
    while cur_b != 0:
        quotient = (cur_a // cur_b) & MASK32
        next_x = (coef_x - quotient * prev_x) & MASK32
        coef_y, prev_y = prev_y, (coef_y - quotient * prev_y) & MASK32
        coef_x, prev_x = prev_x, next_x
        cur_a, cur_b = cur_b, (cur_a % cur_b) & MASK32
    return coef_x, coef_y


def _mod_inverse32(value):  # b.d : modular inverse modulo 2^32
    if value == 1:
        return 1
    x, y = _ext_gcd32(value, (MASK32 % value) + 1)
    return (x - y * (MASK32 // value)) & MASK32


class CS64Key:
    """
    A set of linear-congruential parameters derived from a 64-bit seed (d4.b).
    Java fields: f5638a..f5645h -> mul_a, add_a, mul_c, add_c, mul_e, inv_a, inv_c, inv_e.
    """

    def __init__(self):
        self.mul_a = self.add_a = self.mul_c = self.add_c = self.mul_e = 0
        self.inv_a = self.inv_c = self.inv_e = 0

    @classmethod
    def from_seed(cls, seed, const_c, const_d, const_e):  # b(BigInteger, C, D, E)
        self = cls()
        seed_hi = high32(seed)
        seed_lo = low32(seed)
        self.mul_a = (seed_lo | 1) & MASK32
        self.add_a = (seed_hi | 1) & MASK32
        self.mul_c = ((const_c ^ seed_lo) | 1) & MASK32
        self.add_c = ((seed_hi ^ const_d) | 1) & MASK32
        self.mul_e = ((const_e ^ seed_lo) | 1) & MASK32
        return self

    def copy_into(self, other):
        other.mul_a, other.add_a, other.mul_c, other.add_c = (
            self.mul_a,
            self.add_a,
            self.mul_c,
            self.add_c,
        )
        other.mul_e, other.inv_a, other.inv_c, other.inv_e = (
            self.mul_e,
            self.inv_a,
            self.inv_c,
            self.inv_e,
        )

    def hash_forward(self, data, word_count):  # b.a : forward polynomial hash
        stage1 = ((self.mul_a * ((self.mul_e * read_u32(data, 0)) & MASK32)) + self.add_a) & MASK32
        stage2 = ((self.mul_c * (read_u32(data, 4) + stage1)) + self.add_c) & MASK32
        running = (stage1 + stage2) & MASK32
        pair_idx = 1
        word_idx = 2
        while pair_idx < word_count // 2:
            next_word = word_idx + 1
            stage1 = (
                (self.mul_a * (stage2 + ((self.mul_e * read_u32(data, word_idx << 2)) & MASK32)))
                + self.add_a
            ) & MASK32
            running = (running + stage1) & MASK32
            stage2 = (
                (self.mul_c * (stage1 + read_u32(data, next_word << 2))) + self.add_c
            ) & MASK32
            running = (running + stage2) & MASK32
            pair_idx += 1
            word_idx = next_word + 1
        return join64(stage2, running)

    def hash_inverse(self, data, length, seed):  # b.b : inverse of hash_forward
        word_count = length // 4
        seed_lo = low32(seed)
        seed_hi = high32(seed)
        tail_lo = 0
        tail_hi = 0
        if word_count > 2:
            tail = self.hash_forward(data, word_count - 2)
            tail_lo = low32(tail)
            tail_hi = high32(tail)
        self.inv_a = _mod_inverse32(self.mul_a)
        self.inv_c = _mod_inverse32(self.mul_c)
        self.inv_e = _mod_inverse32(self.mul_e)
        base = (0 + seed_lo - tail_lo - seed_hi) & MASK32
        left = (self.inv_e * ((base - self.add_a) * self.inv_a - tail_hi)) & MASK32
        right = ((0 + self.inv_c) * ((seed_hi - self.add_c) & MASK32) - base) & MASK32
        return join64(left, right)


def derive_nonce(key, sbox, const_c, const_d, const_e, data, length, out_key):  # c.c
    """CBC-MAC the id bytes, build a CS64Key from that, return the transaction nonce."""
    mac = cbc_mac(key, sbox, data, length)
    cs_key = CS64Key.from_seed(mac, const_c, const_d, const_e)
    cs_key.copy_into(out_key)
    return (cs_key.hash_forward(data, length // 4) ^ mac) & MASK64


# ------------------------------------------------------------------ word-swap hash (d4.g)
# Each round keeps a small state: [word_index, accumulator, prev_output, prev_carry].
def _swap_round_fwd(k1, k2, k3, k4, k5, data, state):  # g.e
    carry, accumulator, word_index = state[3], state[1], state[0]
    mixed = (carry + read_u32(data, word_index << 2)) & MASK32
    out = ((mixed * k1) + (swap_halves32(mixed) * k2)) & MASK32
    carry_out = (
        (((swap_halves32(out) * k3) + (out * k4)) & MASK32) + (swap_halves32(out) * k5)
    ) & MASK32
    state[0] = word_index + 1
    state[1] = (accumulator + carry_out) & MASK32
    state[2] = out
    state[3] = carry_out


def _swap_final_fwd(k1, k2, k3, k4, k5, state):  # g.d (no data word)
    carry, accumulator, word_index = state[3], state[1], state[0]
    out = ((k1 * carry) + (swap_halves32(carry) * k2)) & MASK32
    carry_out = (
        (((swap_halves32(out) * k3) + (k4 * out)) & MASK32) + (swap_halves32(out) * k5)
    ) & MASK32
    state[0] = word_index
    state[1] = (accumulator + carry_out) & MASK32
    state[2] = out
    state[3] = carry_out


def word_swap_fwd(data, length, seed):  # g.b
    word_count = length // 4
    seed_lo = low32(seed) | 1
    seed_hi = high32(seed) | 1
    state = [0, 0, 0, 0]
    while word_count > 1:
        _swap_round_fwd(seed_lo, 817042533, 957654963, 2008139383, -1584789045, data, state)
        _swap_round_fwd(seed_hi, 1488610021, 1525158095, 224458411, -530701063, data, state)
        word_count -= 2
    if word_count == 1:
        _swap_round_fwd(seed_lo, 817042533, 957654963, 2008139383, -1584789045, data, state)
        _swap_final_fwd(seed_hi, 1488610021, 1525158095, 224458411, -530701063, state)
    return join64(state[1], state[3])


def _swap_round_inv(seed, k1, k2, k3, k4, final_k, data, state):  # g.g
    prev_out, accumulator, word_index = state[2], state[1], state[0]
    mixed = (prev_out + read_u32(data, word_index << 2)) & MASK32
    out = swap_halves32((mixed * seed) & MASK32)
    chain = (out * k1) & MASK32
    chain = (swap_halves32(chain) * k2) & MASK32
    chain = (swap_halves32(chain) * k3) & MASK32
    chain = (swap_halves32(chain) * k4) & MASK32
    folded = (chain + (out * final_k)) & MASK32
    state[0] = word_index + 1
    state[1] = (accumulator + folded) & MASK32
    state[2] = folded
    state[3] = out


def _swap_final_inv(seed, k1, k2, k3, k4, final_k, state):  # g.f (no data word)
    prev_out, accumulator, word_index = state[2], state[1], state[0]
    out = swap_halves32((prev_out * seed) & MASK32)
    chain = (out * k1) & MASK32
    chain = (swap_halves32(chain) * k2) & MASK32
    chain = (swap_halves32(chain) * k3) & MASK32
    chain = (swap_halves32(chain) * k4) & MASK32
    folded = (chain + (out * final_k)) & MASK32
    state[0] = word_index
    state[1] = (accumulator + folded) & MASK32
    state[2] = folded
    state[3] = out


def word_swap_inv(data, length, seed):  # g.a
    word_count = length // 4
    seed_lo = low32(seed) | 1
    seed_hi = high32(seed) | 1
    state = [0, 0, 0, 0]
    while word_count > 1:
        _swap_round_inv(seed_lo, -1396992403, -1651782415, 2032963901, -1328225133, 0, data, state)
        _swap_round_inv(seed_hi, 1708849391, 413217561, 1824744093, 1082356119, 0, data, state)
        word_count -= 2
    if word_count == 1:
        _swap_round_inv(seed_lo, -1396992403, -1651782415, 2032963901, -1328225133, 0, data, state)
        _swap_final_inv(seed_hi, 1708849391, 413217561, 1824744093, 1082356119, 0, state)
    return join64(state[1], state[2])


# ------------------------------------------------------------------ RC4-style stream cipher (d4.a)
class StreamCipher:
    """
    Keyed stream cipher seeded from an 8-byte key, used to en/decrypt the message
    body (TaviranyitoBV4Key). It is its own inverse: apply() XORs a keystream.
    """

    def __init__(self, key):
        # key-scheduling: shuffle a 256-entry state by the key
        state = list(range(256))
        swap_pos = 0
        key_pos = 0
        for i in range(256):
            swap_pos = (swap_pos + state[i] + key[key_pos]) & 255
            state[i], state[swap_pos] = state[swap_pos], state[i]
            key_pos += 1
            if key_pos == len(key):
                key_pos = 0
        # warm-up: derive a 132-byte schedule, then split into one seed word + 32 words
        schedule = [0] * 132
        idx_i = 0
        idx_j = 0
        for s in range(132):
            idx_i = (idx_i + 1) & 255
            picked = state[idx_i] & 255
            idx_j = (idx_j + picked) & 255
            state[idx_i] = state[idx_j]
            state[idx_j] = picked & 255
            schedule[s] = state[(state[idx_i] + picked) & 255]
        self.state = state
        self.idx_i = idx_i & 255
        self.idx_j = idx_j & 255
        self.accumulator = read_u32(schedule, 0)
        self.words = [read_u32(schedule, (n + 1) * 4) for n in range(32)]

    def apply(
        self, nbytes, data
    ):  # a(length, data) : transform first nbytes in place, word by word
        state = self.state
        words = self.words
        idx_i = self.idx_i
        idx_j = self.idx_j
        acc = self.accumulator
        word_index = 0
        for _ in range(nbytes >> 2):
            idx_i = (idx_i + 1) & 255
            picked = state[idx_i] & 255
            idx_j = (idx_j + picked) & 255
            state[idx_i] = state[idx_j]
            state[idx_j] = picked & 255
            mix_idx = (state[idx_i] + state[idx_j]) & 255
            byte_off = word_index << 2
            word_index += 1
            masked = (read_u32(data, byte_off) ^ ((acc * state[mix_idx & 255]) & MASK32)) & MASK32
            write_u32(masked, data, byte_off)
            sched_idx = mix_idx & 31
            acc = (acc + words[sched_idx]) & MASK32
            state[mix_idx] = (state[mix_idx] + words[sched_idx]) & 255
        self.idx_i = idx_i & 255
        self.idx_j = idx_j & 255
        self.accumulator = acc


# ------------------------------------------------------------------ id / key byte prep
def guid_to_bytes(cid: str):
    """Strip dashes, parse 16 bytes, reorder like .NET Guid.ToByteArray (model.b.m)."""
    cleared = cid.replace("-", "")
    count = len(cleared) // 2
    raw = [int(cleared[i * 2 : i * 2 + 2], 16) for i in range(count)]
    out = [0] * count
    for i in range(count):
        if i < 4:  # first 4 bytes reversed
            out[i] = raw[3 - i]
        elif i < 6:  # next 2 reversed
            out[i] = raw[9 - i]
        elif i < 8:  # next 2 reversed
            out[i] = raw[13 - i]
        else:  # remaining 8 unchanged
            out[i] = raw[i]
    return out


def key_to_bytes(companion_key: str):
    if len(companion_key) != 16:
        raise ValueError(f"key must be 16 hex chars, got {len(companion_key)}")
    return [int(companion_key[i * 2 : i * 2 + 2], 16) for i in range(8)]


def keyed_digest(key, sbox, const_c, const_d, const_e, data, length):  # c.d
    """Static keyed hash: CBC-MAC folded through mac_mix and both word-swap passes."""
    mac = cbc_mac(key, sbox, data, length)
    result = mac ^ mac_mix(data, length, mac, const_c, const_d, const_e)
    result = result ^ word_swap_fwd(data, length, result)
    result = result ^ word_swap_inv(data, length, result)
    return result & MASK64


def compute_hash(id_bytes, key_bytes, ip_bytes, seq, body_len):  # c4.a.a
    """The `hash` URL parameter: keyed digest over (seq, body length, ip, first 4 id bytes)."""
    block = [0] * 16
    write_u32(seq & MASK32, block, 0)
    write_u32(body_len, block, 4)
    for i in range(4):
        block[8 + i] = (ip_bytes[i] + 256) & 255
    block[12:16] = id_bytes[0:4]
    digest = keyed_digest(key_bytes, SBOX, CONST_C | 1, CONST_D | 1, CONST_E | 1, block, 16)
    return (f"{seq & MASK32:08x}{body_len & MASK32:08x}{digest:016x}").upper()


# ------------------------------------------------------------------ transaction codec (c4.b / d4.e)
class Codec:
    """
    Encrypts a command string and decrypts a response, keyed by a companion
    id + key (TaviranyitoTransactionCodec). Construction derives a per-session
    nonce from the id bytes; the same (id, key) always yields the same nonce.
    """

    def __init__(self, cid: str, key: str):
        id_bytes = guid_to_bytes(cid)
        key_bytes = key_to_bytes(key)
        if len(id_bytes) == 0 or len(id_bytes) % 8 != 0:
            raise ValueError("id length must be a nonzero multiple of 8")
        if len(key_bytes) < 8:
            raise ValueError("key must be >= 8 bytes")
        self.id_bytes = id_bytes
        self.key_bytes = list(key_bytes)
        self.cs_key = CS64Key()
        self.nonce = derive_nonce(
            self.key_bytes,
            SBOX,
            CONST_C | 1,
            CONST_D | 1,
            CONST_E | 1,
            list(id_bytes),
            len(id_bytes),
            self.cs_key,
        )

    def encrypt(self, text: str) -> bytes:
        payload = text.encode("utf-8")
        payload_len = len(payload)
        total = (
            payload_len + 12 + 7
        ) & ~7  # 4-byte length prefix + payload + 8-byte trailer, padded to 8
        buf = [0] * total
        write_u32(payload_len, buf, 0)
        write_u64(self.nonce, buf, total - 8)
        buf[4 : 4 + payload_len] = payload
        # build the 8-byte MAC trailer, then stream-encrypt everything before it
        mac_block = [0] * 8
        write_u64(self.cs_key.hash_forward(buf, total // 4), mac_block, 0)
        block_encrypt(self.key_bytes, SBOX, mac_block)
        body_end = total - 8
        buf[body_end : body_end + 8] = mac_block
        StreamCipher(mac_block).apply(body_end, buf)
        return bytes(b & 0xFF for b in buf)

    def decrypt(self, data: bytes):
        """Returns (plaintext, hash_ok) or None if the length is invalid."""
        buf = list(data)
        total = len(buf)
        if (total & 7) != 0 or total < 12:
            return None
        body_end = total - 8
        mac_block = buf[body_end : body_end + 8]
        StreamCipher(mac_block).apply(body_end, buf)
        block_decrypt(self.key_bytes, SBOX, mac_block)
        recovered = self.cs_key.hash_inverse(buf, total, read_u64(mac_block, 0))
        write_u64(recovered, buf, body_end)
        payload_len = read_u32(buf, 0)
        if payload_len > total - 12:
            payload_len = total - 12
        hash_ok = read_u64(buf, total - 8) == self.nonce
        text = bytes(buf[4 : 4 + payload_len]).decode("utf-8", errors="replace")
        return text, hash_ok
