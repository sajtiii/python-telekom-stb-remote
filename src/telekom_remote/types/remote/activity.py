#!/usr/bin/env python3
"""Live device state: volume, channel, power, playback flags (companion `op=activity`)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ...utils import items_to_dict, opt_int, parse_datetime


def _flag(value) -> bool:
    return str(value).strip() in ("1", "true", "True")


@dataclass(frozen=True)
class Activity:
    channel: int | None = None  # current logical channel number (LCN)
    volume: int | None = None  # 0..?
    muted: bool = False
    awake: bool = True  # False == standby
    streaming: bool = False
    recording: bool = False
    screensaver: bool = False
    tune_time: datetime | None = None  # when the current channel was tuned
    channel_map: str | None = None
    application: str | None = None  # running app urn (channeltv == live TV)
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_element(cls, element) -> "Activity":
        items = items_to_dict(element)
        return cls(
            channel=opt_int(items.get("channel")),
            volume=opt_int(items.get("volume")),
            muted=_flag(items.get("mute")),
            awake=_flag(items.get("awake")),
            streaming=_flag(items.get("streaming")),
            recording=_flag(items.get("recording")),
            screensaver=_flag(items.get("screensaver")),
            tune_time=parse_datetime(items.get("tune-time")),
            channel_map=items.get("channelmap"),
            application=items.get("application"),
            raw=items,
        )
