#!/usr/bin/env python3
from __future__ import annotations

import datetime
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

from .types.epg import Channel, ChannelGroup, Program
from .utils import localname

DEFAULT_BASE = "https://smartapp.telekom.hu/musorujsag/"
SERVLET = "EpgWebClient/EpgWebServlet"


class Epg:
    def __init__(
        self, base: str = DEFAULT_BASE, user_id: str = "0", session_id: str = "", timeout: int = 15
    ):
        self.base = base.rstrip("/")
        self.user_id = user_id  # "0" works for public guide data
        self.session_id = session_id
        self.timeout = timeout

    def _get(self, action: str, params: dict | None = None) -> ET.Element:
        query = {"action": action}
        if params:
            query.update(params)
        url = f"{self.base}/{SERVLET}?{urlencode(query)}"
        req = urllib.request.Request(url, headers={"User-Agent": "okhttp/3"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return ET.fromstring(resp.read())

    # --- personalized access (optional) ----------------------------------------
    def register_pin(self, pin: str) -> str:
        """ConfirmMobileRegistration: exchange the 4-digit PIN for a personal UserID."""
        if not (len(pin) == 4 and pin.isdigit()):
            raise ValueError("PIN must be 4 digits")
        root = self._get("ConfirmMobileRegistration", {"PIN": pin})
        reg = next((e for e in root.iter() if localname(e.tag) == "Registration"), None)
        user_id = reg.findtext("UserID") if reg is not None else None
        if not user_id:
            raise RuntimeError(f"registration failed / no UserID: {root.tag} {root.attrib}")
        self.user_id = user_id
        return user_id

    # --- guide data (one fetch each) --------------------------------------------
    def channels(self) -> list[Channel]:
        """GetTVChannels4iPhone -> list[Channel]."""
        root = self._get("GetTVChannels4iPhone", {"UserID": self.user_id})
        return [Channel.from_element(el) for el in root.iter() if localname(el.tag) == "channel"]

    def groups(self) -> list[ChannelGroup]:
        """GetAllTVGroups -> list[ChannelGroup]."""
        root = self._get("GetAllTVGroups")
        return [ChannelGroup.from_element(el) for el in root.iter() if localname(el.tag) == "group"]

    def schedules(self, channel_ids, date: str | None = None) -> dict[str, list[Program]]:
        """
        GetSchedulesForGenChannelListv2 -> {channel_id: [Program, ...]}.
        channel_ids: list or comma string; date: 'YYYY-MM-DD' (default today).
        """
        if isinstance(channel_ids, (list, tuple)):
            channel_ids = ",".join(str(c) for c in channel_ids)
        if date is None:
            date = datetime.date.today().isoformat()
        root = self._get(
            "GetSchedulesForGenChannelListv2",
            {
                "Duration": "1440",
                "UserID": self.user_id,
                "SessionID": self.session_id,
                "FromDate": date,
                "ChannelIDs": channel_ids,
            },
        )
        out: dict[str, list[Program]] = {}
        for schedule in root.iter():
            if localname(schedule.tag) != "schedules":
                continue
            out[schedule.get("channelid")] = [
                Program.from_element(p) for p in schedule if localname(p.tag) == "schedule"
            ]
        return out
