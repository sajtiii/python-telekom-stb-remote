# Telekom IPTV remote and EPG

Reverse-engineered from the Magyar Telekom Műsorújság Android app
(`tmobile.hu.android.epgmiab`, v4.2.359). Stdlib only, no dependencies.

Two independent subsystems:

| Subsystem | Transport | Auth | Needs the box? |
|-----------|-----------|------|----------------|
| Local remote | HTTP to STB `:53208`, custom CS64/BV4 crypto | 8-hex code, then cid/key | yes |
| Cloud EPG | XML over HTTPS, `smartapp.telekom.hu` | UserID `0` (public) or PIN-linked | no |

## Package layout

```
src/telekom_iptv_remote/ reusable library (stdlib only)
  __init__.py     exports Remote, Device, Key, Epg
  codec.py        crypto engine (Codec), ported from Java with readable names
  device.py       Device dataclass (ip, cid, key, port, seq, name)
  remote.py       Remote: pair(), send_key(), tune(), unpair(), info(), activity(),
                          capabilities(), channels(), apps(), devices(), genres()
  epg.py          Epg: channels(), groups(), schedules(), register_pin()
  keys.py         Key enum (53 buttons)
  utils/          shared XML parsing and coercion helpers
  types/
    epg/          typed EPG models: Channel, Program, ChannelGroup
    remote/       typed box models: NowPlaying, Activity, BoxChannel,
                  Capabilities, App, PairedDevice, Genre
examples/
  pairing.py          one-time pairing, prints clientId and clientKey
  epg.py              channels and schedules (no box needed)
  remote_commands.py  send commands using a saved clientId and clientKey
  state.py            dump everything the box reports (state, now-playing,
                      channels, devices, apps, genres)
tests/
  test_capture.py byte-exact regression test against a real captured pairing
decompiled-reference/   jadx output for the crypto classes
```

A separate HomeAssistant integration package depends on this one.

## Library usage

```python
from telekom_iptv_remote import Remote, Device, Key, Epg

# one-time pairing (enter the 8-hex code shown on the TV)
remote = Remote.pair("192.168.1.50", "1a2b3c4d")
print(remote.device.cid, remote.device.key)  # persistent clientId and clientKey

# later: reuse the credentials, no re-pairing
remote = Remote(
    Device(
        "192.168.1.50",
        cid="12345678-90ab-cdef-1234-567890abcdef",
        key="0123456789ABCDEF",
        volume_min=0,  # the box's volume scale (default 1..25); configure per device
        volume_max=25,
    )
)
remote.send_key(Key.VOLUME_UP)  # True if the box accepted it
remote.set_volume(12)  # absolute volume: reads current, sends the up/down steps
remote.tune("8")  # by logical channel number (LCN)
remote.tune("206", epg_id=True)  # or by EPG id, resolved to the LCN via op=channels

# read live box state, returns typed models from telekom_iptv_remote.types.remote
act = remote.activity()  # Activity: volume, muted, channel (LCN), awake, streaming
print(act.volume, act.muted, act.channel, act.awake)
now = remote.info()  # NowPlaying: current program
print(now.title, now.start_time, now.end_time, now.tune, now.station_epg_id)
cap = remote.capabilities()  # Capabilities: device_type, client_version, commands
chans = remote.channels()  # list[BoxChannel], maps LCN to EPG id (paginated)

# cloud EPG (no box needed), returns typed models from telekom_iptv_remote.types.epg
epg = Epg()
channels = epg.channels()  # list[Channel] (ch.id, ch.name, ch.rank:int, ch.group_ids)
groups = epg.groups()  # list[ChannelGroup]
guide = epg.schedules(["206", "369"])  # dict[str, list[Program]]
for program in guide["206"]:  # program.start_time: datetime, program.channel_id: str
    print(program.title, program.start_time, program.end_time, program.channel_id)
user_id = epg.register_pin("1234")  # optional: personal UserID for recordings

# Each method is one fetch. Models carry raw ids (Channel.group_ids, Program.channel_id).
# Resolving those to objects and any caching are the caller's responsibility.
```

## Examples

Runnable from a checkout (each adds `src/` to `sys.path` via `_bootstrap`):

```bash
python3 examples/pairing.py 192.168.1.50 1A2B3C4D     # one-time, prints cid/key
python3 examples/epg.py                                # channels and today's guide
python3 examples/remote_commands.py <ip> <cid> <key>  # send a command or run the demo
python3 examples/state.py <ip> <cid> <key>            # dump all box state (read-only)
```

Install it as a dependency instead:

```bash
pip install -e .          # then: from telekom_iptv_remote import Remote, Device, Key, Epg
```

## Protocol notes

**Pairing.** `op=pair&key=<code>&name=&tags=` encrypted with bootstrap cid
`E7AAEC8C-…` and key `code+code`. The box replies with XML holding your persistent
`cid` and `key`.

**Commands.** `op=remotekey&key=<name>` and `op=tune&s=<ch>&type=channel`, encrypted
with your cid and key, POSTed to `http://<ip>:53208/companion?hash=…&cid=…`.

**State read-back.** The box supports many Mediaroom ops the app never uses.
`op=activity` returns live state: volume, mute, channel, awake or standby, streaming,
recording. `op=info` returns the current program. `op=channels` returns the box
channel list, which maps LCN to EPG id, paginated 30 per page via `&index=N`.
`op=capabilities` returns device info and the full command set. `op=apps`,
`op=devices`, and `op=genres` return the installed apps, paired companions, and the
genre tree. The library wraps these as `activity()`, `info()`, `channels()`,
`capabilities()`, `apps()`, `devices()`, and `genres()`.

**op=open.** `open()` raises `NotImplementedError` because the box's URL format is
unknown. An app urn returns 404, and the app has the op but never calls it.

**Ops that need parameters.** `op=diags` returns 404 (listed in capabilities but
unsupported on this box). `op=audio`, `op=sound`, `op=state`, `op=subtitles`,
`op=devicename`, and `op=listen` return 400 without parameters, whose format is
unknown. `op=listen` is probably a notification or subscribe channel worth working
out, so state updates could be pushed instead of polled.

**Crypto** (`codec.Codec`). A CBC-MAC and a CS64 word hash derive a per-message
nonce. An RC4-style stream (`StreamCipher`) encrypts the body. An 8-byte MAC trailer
authenticates it. The URL `hash` is a separate keyed digest over seq, length, ip, and
cid bytes. `seq` is always 0, and the cid is byte-reordered like .NET
`Guid.ToByteArray()`. Every class in `codec.py` maps one-to-one to a Java class, with
a mapping table at the top of the file.

## Verified

- `python3 tests/test_capture.py` matches a real captured pairing byte for byte:
  request body, URL hash, response decrypt, and credential parse.
- EPG checked live against `smartapp.telekom.hu`.
- Local remote checked live: `send_key` returns HTTP 204 from a real box.
- State read-back checked live: `activity()` returned `volume=21, channel=8,
  muted=False`, and `info()` returned the current program with parsed start and end
  times.
