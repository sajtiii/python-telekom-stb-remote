#!/usr/bin/env python3
"""
Example 2: Electronic program guide (EPG).

Pulls channels, groups and today's schedule from Telekom's cloud guide. Needs no
box and no pairing. Public guide data works with the default UserID "0".

Each call is one fetch; the models carry raw id references (Channel.group_ids,
Program.channel_id). Resolving ids to objects and caching are up to the caller.

    python3 examples/epg.py
"""

import _bootstrap  # noqa: F401

from telekom_remote import Epg


def main():
    epg = Epg()

    # Channels -> list[Channel]
    print("Channels:")
    channels = epg.channels()
    for ch in channels[:10]:
        star = " *" if ch.is_favourite else ""
        print(f"  {ch.id:>6}  {ch.name:<20} groups={list(ch.group_ids)}{star}")
    print(f"  ... {len(channels)} channels total\n")

    # Groups -> list[ChannelGroup]
    print("Groups:")
    for group in epg.groups()[:5]:
        print(f"  [{group.id}] {group.name}")
    print()

    # Schedule -> dict[channel_id, list[Program]]
    some_ids = [ch.id for ch in channels[:2]]
    print(f"Today's schedule for channels {some_ids}:")
    guide = epg.schedules(some_ids)
    for channel_id, programs in guide.items():
        print(f"\n  == channel {channel_id} ==")
        for p in programs[:6]:
            start = p.start_time.strftime("%H:%M") if p.start_time else "?"
            print(f"    {start} ({p.duration}m)  {p.title}")

    # --- optional: personal UserID for recordings/favorites ---
    #   user_id = epg.register_pin("1234")   # then epg uses it for later calls


if __name__ == "__main__":
    main()
