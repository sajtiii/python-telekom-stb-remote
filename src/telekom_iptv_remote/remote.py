#!/usr/bin/env python3
from __future__ import annotations

import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from .codec import BOOTSTRAP_CID, DEFAULT_PORT, Codec, compute_hash, guid_to_bytes, key_to_bytes
from .device import Device
from .keys import Key
from .types.remote import (
    Activity,
    App,
    BoxChannel,
    Capabilities,
    Genre,
    NowPlaying,
    PairedDevice,
)
from .utils import localname


class PairingError(RuntimeError):
    pass


class Remote:
    def __init__(self, device: Device):
        self.device = device

    # --- construction -----------------------------------------------------------
    @classmethod
    def pair(
        cls, ip: str, code: str, name: str = "", port: int = DEFAULT_PORT, timeout: int = 10
    ) -> "Remote":
        """
        LAN-pair with the box. `code` is the 8 hex chars shown on the TV. Returns a
        ready Remote whose Device holds the persistent cid/key the box issued.
        """
        code = code.lower()
        if len(code) != 8:
            raise ValueError("pairing code must be 8 hex characters")
        # pairing bootstraps with a fixed id and the code doubled as the key
        bootstrap = Device(ip=ip, cid=BOOTSTRAP_CID, key=code + code, port=port)
        decoded = cls(bootstrap)._request(f"op=pair&key={code}&name={name}&tags=", timeout=timeout)
        if decoded is None:
            raise PairingError("pairing failed: no response from box")
        cid, key, dev_name, seq = _parse_pair_response(decoded)
        return cls(Device(ip=ip, cid=cid, key=key, name=dev_name, seq=seq, port=port))

    # --- commands ---------------------------------------------------------------
    def send_key(self, key) -> bool:
        """Press a remote button. Accepts a Key or a raw wire string. True == accepted."""
        wire = key.value if isinstance(key, Key) else str(key)
        return self._send(f"op=remotekey&key={wire}")

    def tune(self, channel, *, epg_id: bool = False) -> bool:
        """Jump to a channel. By default `channel` is the box's logical channel
        number (LCN / "ref"), e.g. "8". With epg_id=True, `channel` is an EPG channel
        id from Epg.channels() and is resolved to the LCN via the box channel list
        (one extra, paginated op=channels fetch)."""
        if epg_id:
            lcn = self.lcn_for_epg_id(str(channel))
            if lcn is None:
                return False
            channel = lcn
        return self._send(f"op=tune&s={channel}&type=channel")

    def set_volume(self, level: int, *, max_rounds: int = 6) -> bool:
        """Set the absolute volume, clamped to the device's volume_min..volume_max.
        The box has no absolute-volume op, so this reads the current level via
        activity() and sends volume up/down presses. Because the box can drop rapid
        presses, it then re-reads and corrects the remaining delta, up to max_rounds.
        Returns True once the box reports the target level."""
        level = max(self.device.volume_min, min(self.device.volume_max, int(level)))
        for _ in range(max_rounds):
            act = self.activity()
            if act is None or act.volume is None:
                return False
            delta = level - act.volume
            if delta == 0:
                return True
            button = Key.VOLUME_UP if delta > 0 else Key.VOLUME_DOWN
            for _ in range(abs(delta)):
                self.send_key(button)
        return False

    def unpair(self) -> bool:
        return self._send("op=unpair")

    def open(self, url: str) -> bool:
        """`op=open`: launch a URL/app on the box. NOT IMPLEMENTED. The required URL
        format is unverified (an app urn returned 404, and the app has the op but never
        calls it). Capture the app performing a real launch to learn the payload."""
        raise NotImplementedError(
            "op=open: the box's URL format is unknown (an app urn returns 404)"
        )

    # --- state read-back (companion ops the app doesn't use) ---------------------
    def info(self) -> NowPlaying | None:
        """`op=info`: the program currently showing (title, times, channel, tune string)."""
        element = self._request_xml("op=info", "program")
        return NowPlaying.from_element(element) if element is not None else None

    def activity(self) -> Activity | None:
        """`op=activity`: live device state (volume, mute, channel, power, playback flags)."""
        element = self._request_xml("op=activity", "data")
        return Activity.from_element(element) if element is not None else None

    def capabilities(self) -> Capabilities | None:
        """`op=capabilities`: device info and the full set of commands the box accepts."""
        element = self._request_xml("op=capabilities", "data")
        return Capabilities.from_element(element) if element is not None else None

    def channels(self) -> list[BoxChannel]:
        """`op=channels`: the box channel list (LCN <-> EPG-id map). Paginated 30/page."""
        out: list[BoxChannel] = []
        index = 0
        while True:
            root = self._request_root(f"op=channels&index={index}")
            if root is None:
                break
            page = [
                BoxChannel.from_element(e) for e in root.iter() if localname(e.tag) == "channel"
            ]
            out.extend(page)
            total = _child_int(root, "totalResults")
            if not page or total is None or len(out) >= total:
                break
            index += len(page)
        return out

    def lcn_for_epg_id(self, epg_id: str) -> int | None:
        """Resolve an EPG channel id to the box's logical channel number, or None."""
        return next((c.lcn for c in self.channels() if c.epg_id == str(epg_id)), None)

    def apps(self) -> list[App]:
        """`op=apps`: applications installed on the box."""
        root = self._request_root("op=apps")
        if root is None:
            return []
        return [App.from_element(e) for e in root.iter() if localname(e.tag) == "application"]

    def devices(self) -> list[PairedDevice]:
        """`op=devices`: all companions currently paired with the box."""
        root = self._request_root("op=devices")
        if root is None:
            return []
        return [PairedDevice.from_element(e) for e in root.iter() if localname(e.tag) == "device"]

    def genres(self) -> list[Genre]:
        """`op=genres`: the box's genre tree (top-level genres, each with sub-genres)."""
        root = self._request_root("op=genres")
        if root is None:
            return []
        container = next((e for e in root.iter() if localname(e.tag) == "genres"), None)
        if container is None:
            return []
        return [Genre.from_element(e) for e in container if localname(e.tag) == "genre"]

    def _request_root(self, command: str):
        """Send a read command and return the parsed response root, or None."""
        body = self._request(command)
        if not body or body == "OK":
            return None
        return ET.fromstring(body)

    def _request_xml(self, command: str, tag: str):
        """Send a read command and return the first element whose local name is `tag`."""
        root = self._request_root(command)
        if root is None:
            return None
        return next((e for e in root.iter() if localname(e.tag) == tag), None)

    # --- transport (model.b.m) --------------------------------------------------
    def _send(self, command: str, timeout: int = 10) -> bool:
        """Send a fire-and-forget command. True if the box accepted it."""
        return self._request(command, timeout=timeout) is not None

    def _request(self, command: str, timeout: int = 10) -> str | None:
        """Send a command and return the box's reply ("OK" for 204, decrypted body
        for 200), or None on any failure. Used by both _send and pairing."""
        dev = self.device
        codec = Codec(dev.cid, dev.key)
        body = codec.encrypt(command)
        seq = 0  # the app resets the sequence to 0 for every request
        ip_bytes = [int(x) for x in dev.ip.split(".")]
        digest = compute_hash(
            guid_to_bytes(dev.cid), key_to_bytes(dev.key), ip_bytes, seq, len(body)
        )
        url = f"{dev.base_url()}/companion?hash={digest}&cid={dev.cid.lower()}"
        req = urllib.request.Request(url, data=body, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                payload = resp.read()
        except urllib.error.HTTPError:
            return None
        if status == 204:
            return "OK"
        if status == 200 and payload:
            decoded = codec.decrypt(payload)
            return decoded[0] if decoded else None
        return None


def _child_int(root, tag: str):
    """Parse the int text of the first element whose local name is `tag`, or None."""
    el = next((e for e in root.iter() if localname(e.tag) == tag), None)
    if el is None or not el.text:
        return None
    try:
        return int(el.text.strip())
    except ValueError:
        return None


def _parse_pair_response(xml_text: str):
    """Pull cid/key/name/seq out of the <device> element (f4.a), namespace-agnostic."""
    root = ET.fromstring(xml_text)
    dev = next((e for e in root.iter() if localname(e.tag) == "device"), None)
    if dev is None:
        raise PairingError(f"no <device> in pair response: {xml_text!r}")
    return dev.get("cid"), dev.get("key"), dev.get("name") or "", int(dev.get("seq") or "0")
