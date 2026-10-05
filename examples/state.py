#!/usr/bin/env python3
"""
Example 4: Dump everything the box can report about its current state.

Uses the companion read ops (which the official app never calls): capabilities,
activity, info, and the box channel list. Needs a paired clientId / clientKey.

    python3 examples/state.py {ip} {cid} {key}
"""

import sys

import _bootstrap  # noqa: F401

from telekom_remote import Device, Remote

# --- paste your own values from the pairing step ---
BOX_IP = "<ip>"
CLIENT_ID = "<cid>"
CLIENT_KEY = "<key>"


def main():
    ip = sys.argv[1] if len(sys.argv) > 1 else BOX_IP
    cid = sys.argv[2] if len(sys.argv) > 2 else CLIENT_ID
    key = sys.argv[3] if len(sys.argv) > 3 else CLIENT_KEY
    remote = Remote(Device(ip=ip, cid=cid, key=key))

    cap = remote.capabilities()
    print("== capabilities ==")
    if cap:
        print(f"  device    : {cap.device_type}  (Mediaroom {cap.client_version})")
        print(f"  disk/dvr  : disk={cap.disk_present}  dvr={cap.dvr_enabled}")
        print(f"  uptime    : since {cap.start_time}")
        print(f"  commands  : {', '.join(cap.commands)}")

    act = remote.activity()
    print("\n== activity (live state) ==")
    if act:
        print(f"  power     : {'on' if act.awake else 'standby'}")
        print(f"  channel   : LCN {act.channel}")
        print(f"  volume    : {act.volume}   muted: {act.muted}")
        print(
            f"  flags     : streaming={act.streaming} recording={act.recording} "
            f"screensaver={act.screensaver}"
        )
        print(f"  app       : {act.application}")
        print(f"  tuned at  : {act.tune_time}")

    now = remote.info()
    print("\n== now playing ==")
    if now:
        print(f"  title     : {now.title}  ({now.episode})")
        print(f"  when      : {now.start_time} -> {now.end_time}  ({now.duration})")
        print(f"  channel   : LCN {now.channel}  (EPG id {now.station_epg_id})")
        print(f"  type/rate : {now.asset_type}  {now.ratings}")
        print(f"  tune back : remote.tune({now.channel!r})")

    chans = remote.channels()
    print(f"\n== box channels ({len(chans)}) ==  LCN -> name (EPG id)")
    for c in chans[:10]:
        print(f"  {c.lcn:>3} -> {c.long_name:<18} (epg {c.epg_id})")
    print("  ...")

    devices = remote.devices()
    print(f"\n== paired devices ({len(devices)}) ==")
    for d in devices:
        print(f"  {d.cid}  name={d.name!r}  tags={d.tags!r}")

    apps = remote.apps()
    print(f"\n== installed apps ({len(apps)}) ==")
    for app in apps:
        print(f"  layer {app.layer}  {app.id}")

    genres = remote.genres()
    print(f"\n== genres ({len(genres)} top-level) ==")
    for g in genres:
        kids = ", ".join(f"{c.name}({c.id})" for c in g.children)
        print(f"  {g.name} ({g.id})" + (f" -> {kids}" if kids else ""))


if __name__ == "__main__":
    main()
