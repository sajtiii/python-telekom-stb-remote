#!/usr/bin/env python3
"""A channel as the box itself knows it (companion `op=channels`)."""

from __future__ import annotations

from dataclasses import dataclass, field

from ...utils import fields_of, opt_int


@dataclass(frozen=True)
class BoxChannel:
    lcn: int | None = None  # ch / ref: logical channel number (what tune() wants)
    short_name: str = ""
    long_name: str = ""
    epg_id: str | None = None  # trailing id from extId (joins to Epg.channels())
    ext_id: str | None = None  # full extId, e.g. "Station/MyListings, Inc./369"
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_element(cls, element) -> "BoxChannel":
        data = fields_of(element)
        ext = data.get("extId")
        return cls(
            lcn=opt_int(data.get("ch") or data.get("ref")),
            short_name=data.get("shortName", ""),
            long_name=data.get("longName", ""),
            epg_id=(ext.rsplit("/", 1)[-1] if ext else None) or None,
            ext_id=ext,
            raw=data,
        )
