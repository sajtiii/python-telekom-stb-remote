#!/usr/bin/env python3
"""The program currently showing on the box (companion `op=info`)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from ...utils import fields_of, opt_int, parse_datetime, parse_duration


@dataclass(frozen=True)
class NowPlaying:
    title: str
    channel: int | None = None  # ch / ref: logical channel number (LCN)
    description: str | None = None  # desc
    episode: str | None = None
    start_time: datetime | None = None  # time (UTC)
    duration: timedelta | None = None  # dur (ISO-8601)
    tune: str | None = None  # ready-made tune string, e.g. "s=8&type=channel"
    asset_type: str | None = None  # "live", "vod", ...
    ratings: str | None = None
    genres: str | None = None
    station_id: str | None = None  # stnId, e.g. "Station/MyListings, Inc./369"
    ext_id: str | None = None  # extId
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @property
    def end_time(self) -> datetime | None:
        if self.start_time is None or self.duration is None:
            return None
        return self.start_time + self.duration

    @property
    def station_epg_id(self) -> str | None:
        """The trailing EPG channel id from station_id (joins to Epg.channels())."""
        if not self.station_id:
            return None
        return self.station_id.rsplit("/", 1)[-1] or None

    @classmethod
    def from_element(cls, element) -> "NowPlaying":
        data = fields_of(element)
        return cls(
            title=data.get("title", ""),
            channel=opt_int(data.get("ch") or data.get("ref")),
            description=data.get("desc"),
            episode=data.get("episode"),
            start_time=parse_datetime(data.get("time")),
            duration=parse_duration(data.get("dur")),
            tune=data.get("tune"),
            asset_type=data.get("assetType"),
            ratings=data.get("ratings"),
            genres=data.get("genres"),
            station_id=data.get("stnId"),
            ext_id=data.get("extId"),
            raw=data,
        )
