"""
Typed data models, grouped by domain.

    from telekom_remote.types.epg import Channel, Program, ChannelGroup

The EPG models are also re-exported here for convenience.
"""

from .epg import Channel, ChannelGroup, Program

__all__ = ["Channel", "Program", "ChannelGroup"]
