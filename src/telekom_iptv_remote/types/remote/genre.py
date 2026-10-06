#!/usr/bin/env python3
"""A program genre, possibly with sub-genres (companion `op=genres`)."""

from __future__ import annotations

from dataclasses import dataclass, field

from ...utils import fields_of, localname


@dataclass(frozen=True)
class Genre:
    id: str
    name: str
    children: tuple["Genre", ...] = ()
    raw: dict = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_element(cls, element) -> "Genre":
        data = fields_of(element)
        children = tuple(
            cls.from_element(child) for child in element if localname(child.tag) == "genre"
        )
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            children=children,
            raw=data,
        )
