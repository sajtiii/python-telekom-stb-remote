#!/usr/bin/env python3
"""Shared XML parsing and value-coercion helpers."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone


def localname(tag: str) -> str:
    """Strip any '{namespace}' prefix from an ElementTree tag."""
    return tag.rsplit("}", 1)[-1]


def fields_of(element) -> dict:
    """Collect an element's attributes plus the text of its simple child elements."""
    out = dict(element.attrib)
    for child in element:
        if len(child) == 0 and not child.attrib:
            out[localname(child.tag)] = (child.text or "").strip()
    return out


def opt_int(value) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def opt_bool(value) -> bool:
    return str(value).strip().lower() in ("1", "true", "yes")


def parse_datetime(value) -> datetime | None:
    """Parse the EPG timestamp format (e.g. '2026-10-05T23:55:00.000Z') to UTC."""
    if not value:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


_DURATION_RE = re.compile(r"^P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$")


def parse_duration(value) -> timedelta | None:
    """Parse an ISO-8601 duration like 'PT1H5M0S' to a timedelta."""
    if not value:
        return None
    m = _DURATION_RE.match(value)
    if not m:
        return None
    days, hours, minutes, seconds = (int(g) if g else 0 for g in m.groups())
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


def items_to_dict(element) -> dict:
    """Flatten a Mediaroom <data> element's <item name= value=> children into a dict."""
    out = {}
    for item in element.iter():
        if localname(item.tag) == "item" and item.get("name") is not None:
            out[item.get("name")] = item.get("value")
    return out
