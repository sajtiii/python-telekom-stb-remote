#!/usr/bin/env python3
"""Device info and supported command set (companion `op=capabilities`)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ...utils import items_to_dict, opt_bool, parse_datetime


@dataclass(frozen=True)
class Capabilities:
    device_type: str | None = None  # e.g. "STB-3112"
    api_version: str | None = None
    client_version: str | None = None
    user_agent: str | None = None
    commands: tuple[str, ...] = ()  # every op the box accepts
    disk_present: bool = False
    dvr_enabled: bool = False
    start_time: datetime | None = None  # box uptime start
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    def supports(self, command: str) -> bool:
        return command in self.commands

    @classmethod
    def from_element(cls, element) -> "Capabilities":
        items = items_to_dict(element)
        commands = tuple(c for c in (items.get("commands") or "").split(",") if c)
        return cls(
            device_type=items.get("device-type"),
            api_version=items.get("api-version"),
            client_version=items.get("client-version"),
            user_agent=items.get("user-agent"),
            commands=commands,
            disk_present=opt_bool(items.get("disk-present")),
            dvr_enabled=opt_bool(items.get("dvr-enabled")),
            start_time=parse_datetime(items.get("start-time")),
            raw=items,
        )
