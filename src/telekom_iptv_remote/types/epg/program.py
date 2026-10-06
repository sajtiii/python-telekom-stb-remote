#!/usr/bin/env python3
"""A single scheduled program (ApiService.getTVSchedules / ScheduleForChannelXML)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from ...utils import fields_of, opt_int, parse_datetime


@dataclass(frozen=True)
class Program:
    schedule_id: str
    title: str
    start_time: datetime | None  # parsed UTC datetime
    duration: int | None  # length in minutes
    channel_id: str | None = None  # iptvchannelid
    category: str | None = None
    age_limit: int | None = None
    program_id: str | None = None
    episode_id: str | None = None
    iptv_program_id: str | None = None
    start_time_ms: int | None = None  # starttimelong (epoch milliseconds)
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @property
    def end_time(self) -> datetime | None:
        if self.start_time is None or self.duration is None:
            return None
        return self.start_time + timedelta(minutes=self.duration)

    @classmethod
    def from_element(cls, element) -> "Program":
        data = fields_of(element)
        return cls(
            schedule_id=data.get("scheduleid", ""),
            title=data.get("title", ""),
            start_time=parse_datetime(data.get("starttime")),
            duration=opt_int(data.get("duration")),
            channel_id=data.get("iptvchannelid"),
            category=data.get("category"),
            age_limit=opt_int(data.get("agelimit")),
            program_id=data.get("programid"),
            episode_id=data.get("episodeid"),
            iptv_program_id=data.get("iptvprogramid"),
            start_time_ms=opt_int(data.get("starttimelong")),
            raw=data,
        )
