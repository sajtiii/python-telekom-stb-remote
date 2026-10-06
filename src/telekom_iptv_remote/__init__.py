"""
Telekom (Microsoft Mediaroom) set-top-box remote + EPG client.

    from telekom_iptv_remote import Remote, Device, Key, Epg

    remote = Remote.pair("192.168.1.50", "1a2b3c4d")
    remote.send_key(Key.VOLUME_UP)

    epg = Epg()
    print(epg.channels())
"""

from .device import Device
from .epg import Epg
from .keys import ALL_KEYS, Key
from .remote import PairingError, Remote
from .types import Channel, ChannelGroup, Program
from .types.remote import (
    Activity,
    App,
    BoxChannel,
    Capabilities,
    Genre,
    NowPlaying,
    PairedDevice,
)

__all__ = [
    "Remote",
    "Device",
    "Key",
    "Epg",
    "PairingError",
    "ALL_KEYS",
    "Channel",
    "Program",
    "ChannelGroup",
    "NowPlaying",
    "Activity",
    "BoxChannel",
    "Capabilities",
    "App",
    "PairedDevice",
    "Genre",
]
