#!/usr/bin/env python3
"""A TV channel from the EPG (ApiService.getTVChannels / TVChannelsXML)."""

from __future__ import annotations

from dataclasses import dataclass, field

from ...utils import fields_of, localname, opt_bool, opt_int


@dataclass(frozen=True)
class Channel:
    id: str  # EPG channel id (e.g. "206")
    name: str  # display name (e.g. "M1 HD")
    rank: int | None = None  # ordering position
    img: str | None = None  # logo URL
    is_favourite: bool = False  # marked as favourite
    account: str | None = None
    sanoma_channel_id: str | None = None
    resource_version: str | None = None
    group_ids: tuple[str, ...] = ()  # ids of the groups this channel belongs to
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_element(cls, element) -> "Channel":
        data = fields_of(element)
        group_ids = tuple(
            group.get("id")
            for child in element
            if localname(child.tag) == "groups"
            for group in child
            if localname(group.tag) == "group" and group.get("id")
        )
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            rank=opt_int(data.get("rank")),
            img=data.get("img"),
            is_favourite=opt_bool(data.get("fav")),
            account=data.get("account"),
            sanoma_channel_id=data.get("sanomachannelid"),
            resource_version=data.get("resourceversion"),
            group_ids=group_ids,
            raw=data,
        )
