#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from .codec import DEFAULT_PORT


@dataclass
class Device:
    ip: str
    cid: str
    key: str
    name: str = ""
    seq: int = 0
    port: int = DEFAULT_PORT
    volume_min: int = 1  # box volume scale, used by Remote.set_volume()
    volume_max: int = 25

    def base_url(self) -> str:
        return f"http://{self.ip}:{self.port}"
