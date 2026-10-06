#!/usr/bin/env python3
"""
Example 3: Controlling the box with a saved clientId and clientKey.

Once you've paired (see examples/pairing.py) you never pair again: construct a
Device from the stored credentials and send commands. send_key/tune return True
when the box accepts the command.

    python3 examples/remote_commands.py {ip} {cid} {key}            # demo sequence
    python3 examples/remote_commands.py {ip} {cid} {key} volumeup   # press one key
"""

import sys

import _bootstrap  # noqa: F401

from telekom_iptv_remote import Device, Key, Remote

# --- paste your own values from the pairing step ---
BOX_IP = "<ip>"
CLIENT_ID = "<cid>"
CLIENT_KEY = "<key>"


def resolve_key(name: str) -> Key:
    """Accept a wire value ('volumeup') or an enum name ('VOLUME_UP')."""
    try:
        return Key(name)  # by wire value
    except ValueError:
        pass
    try:
        return Key[name.upper()]  # by enum member name
    except KeyError:
        raise SystemExit(f"Unknown key '{name}'. Options: {', '.join(k.value for k in Key)}")


def main():
    ip = sys.argv[1] if len(sys.argv) > 1 else BOX_IP
    cid = sys.argv[2] if len(sys.argv) > 2 else CLIENT_ID
    key = sys.argv[3] if len(sys.argv) > 3 else CLIENT_KEY

    remote = Remote(Device(ip=ip, cid=cid, key=key))

    # 4th arg: press just that one key and exit
    if len(sys.argv) > 4:
        button = resolve_key(sys.argv[4])
        ok = remote.send_key(button)
        print(f"{button.value} -> {'OK' if ok else 'FAILED'}")
        return

    # otherwise run the demo sequence
    # press buttons by name (type-safe enum, or a raw string like "volumeup")
    print("volume up   :", remote.send_key(Key.VOLUME_UP))
    print("channel up  :", remote.send_key(Key.CHANNEL_UP))

    # change channel by typing its number on the box (reliable way)
    for digit in (Key.NUMBER_1, Key.NUMBER_0, Key.NUMBER_1):  # -> channel 101
        remote.send_key(digit)
    print("typed 101   : done")

    # NOTE: tune() takes the box's *logical channel number* (LCN / "ref"), NOT the
    # EPG channel id from examples/epg.py. Passing an EPG id (e.g. "206") returns 404.
    #   remote.tune("1")   # tune to LCN 1

    # every available button:
    print("\nAll keys:", ", ".join(k.value for k in Key))


if __name__ == "__main__":
    main()
