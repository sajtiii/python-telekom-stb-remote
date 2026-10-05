#!/usr/bin/env python3
"""A channel group / category (ApiService.getTVGroups / TVGroupsXML)."""

from __future__ import annotations

from dataclasses import dataclass, field

from ...utils import fields_of


@dataclass(frozen=True)
class ChannelGroup:
    id: str  # group id (e.g. "1")
    name: str  # display name (e.g. "Magyar")
    desc: str | None = None  # comma-separated channel preview
    img: str | None = None  # icon URL
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_element(cls, element) -> "ChannelGroup":
        data = fields_of(element)
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            desc=data.get("desc"),
            img=data.get("img"),
            raw=data,
        )
