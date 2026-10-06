#!/usr/bin/env python3
"""An application installed on the box (companion `op=apps`)."""

from __future__ import annotations

from dataclasses import dataclass, field

from ...utils import fields_of, opt_int


@dataclass(frozen=True)
class App:
    id: str  # urn, e.g. "urn:microsoft:mediaroom:application:channeltv"
    layer: int | None = None
    url: str | None = None  # content path on the box
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_element(cls, element) -> "App":
        data = fields_of(element)
        return cls(
            id=data.get("id", ""),
            layer=opt_int(data.get("layer")),
            url=data.get("url"),
            raw=data,
        )
