#!/usr/bin/env python3
"""A companion paired with the box, as the box reports it (companion `op=devices`)."""

from __future__ import annotations

from dataclasses import dataclass, field

from ...utils import fields_of, opt_int


@dataclass(frozen=True)
class PairedDevice:
    cid: str  # companion id (clientId)
    name: str = ""
    key: str = ""  # companion key (clientKey), returned for every paired device
    tags: str = ""
    seq: int | None = None
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_element(cls, element) -> "PairedDevice":
        data = fields_of(element)
        return cls(
            cid=data.get("cid", ""),
            name=data.get("name", ""),
            key=data.get("key", ""),
            tags=data.get("tags", ""),
            seq=opt_int(data.get("seq")),
            raw=data,
        )
