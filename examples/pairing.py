#!/usr/bin/env python3
"""
Example 1: Pairing.

One-time setup: put the box's remote-pairing screen up so it shows an 8-hex code,
then run this. It pairs over the LAN and prints the persistent clientId/clientKey
you reuse forever after (see examples/remote_commands.py). No PIN needed.

    python3 examples/pairing.py {ip} {code}
"""

import sys

import _bootstrap  # noqa: F401  (adds the repo root to sys.path)

from telekom_iptv_remote import PairingError, Remote

# --- or hard-code instead of passing on the command line ---
BOX_IP = "<ip>"
PAIRING_CODE = "<code>"  # the 8 hex chars shown on the TV


def main():
    ip = sys.argv[1] if len(sys.argv) > 1 else BOX_IP
    code = sys.argv[2] if len(sys.argv) > 2 else PAIRING_CODE

    print(f"Pairing with {ip} using code {code} ...")
    try:
        remote = Remote.pair(ip, code)
    except PairingError as e:
        print(f"Pairing failed: {e}")
        print("Check the box IP and that the code is still on screen (they expire).")
        return 1

    dev = remote.device
    print("\nPaired. Save these. They do not change and need no re-pairing:\n")
    print(f"  clientId  (cid) = {dev.cid}")
    print(f"  clientKey (key) = {dev.key}")
    print(f"  name            = {dev.name}")
    print("\nNext: drop them into examples/remote_commands.py and control the box.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
