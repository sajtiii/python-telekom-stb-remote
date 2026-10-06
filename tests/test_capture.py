#!/usr/bin/env python3
"""
Regression test against a REAL captured pairing transaction. If the crypto port
ever drifts, these byte-exact assertions fail. Run: python3 -m tests.test_capture
(from the project root) or: python3 tests/test_capture.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from telekom_iptv_remote.codec import (
    BOOTSTRAP_CID,
    Codec,
    compute_hash,
    guid_to_bytes,
    key_to_bytes,
)
from telekom_iptv_remote.remote import _parse_pair_response

# --- captured values -----------------------------------------------------------
CODE = "d67744ad"  # on-screen pairing code D67744AD
IP = "192.168.0.101"
EXPECT_REQUEST = bytes.fromhex(
    "036880D26380A0E1AAE3A31BC1B5677190B7A9E937CF858C"
    "3C24EFBD9C67D6EC49D4119D06EEB8A00B363AB8447790EB"
)
EXPECT_HASH = "00000000000000306C962AD12785352B"
RESPONSE = bytes.fromhex(
    "98AEDBAF18933C8334332DBAF85B386F7EE12336F4D261302CEA18DD5DFB7867"
    "35CE82ECE9242290D8EED250F02E5153F25AEF4A28D2D3888D53FE18AE335030"
    "B8F343006BCC1DA1862C9DF91F6D46D4147B691EED570C3ACB9C03A5363E3502"
    "AED9951CE7D903A57CC4A8FD71BC369 5B033113A3BC457C0CCC764F811DAB10"
    "8569520247B30D194A0936642ED87A3149BEE38920D78E3687A9084914E33025"
    "FBB8AC563438233E1D3E9D96D618CE7FB3FF32E8A54F39AF7F7E4DF5870887E60"
    "EAD165FCE9D6B5B053278CE994D723CEDDF847B5CC9DFFF536B75F7F200FB07F"
    "E82470E2E259CD10EEEBBA2905AABE6FEC86529B47E4BB618E9E9998A8E464A6"
    "B39242DB041FD296B91419FC2F14CCC6EFA753F32E99924EFEA8780A0FEE56E2"
    "51B6CCC514BD6C8858C8828B5539DD642475580E76F652AD31915A5EAEDA4F75"
    "E3C477A86C353691 7B04182823CF7D160F6941AD8C93CC5A2BB624EF2B3A61D"
    "97156924E9827E7712457143421F57011".replace(" ", "")
)
EXPECT_CID = "9d23c20a-13e1-4247-8240-878501cc2ad9"
EXPECT_KEY = "CD650A4967B45527"


def main():
    codec = Codec(BOOTSTRAP_CID, CODE + CODE)

    req = codec.encrypt(f"op=pair&key={CODE}&name=&tags=")
    assert req == EXPECT_REQUEST, "request body mismatch"

    digest = compute_hash(
        guid_to_bytes(BOOTSTRAP_CID),
        key_to_bytes(CODE + CODE),
        [int(x) for x in IP.split(".")],
        0,
        len(req),
    )
    assert digest == EXPECT_HASH, f"hash mismatch: {digest}"

    plaintext, _ = codec.decrypt(RESPONSE)
    cid, key, _, _ = _parse_pair_response(plaintext)
    assert cid == EXPECT_CID, f"cid mismatch: {cid}"
    assert key == EXPECT_KEY, f"key mismatch: {key}"

    print("PASS  request body, url hash, response decrypt, credential parse")
    print(f"      clientId = {cid}")
    print(f"      clientKey = {key}")


if __name__ == "__main__":
    main()
