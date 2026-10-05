"""Typed EPG data models."""

from .channel import Channel
from .group import ChannelGroup
from .program import Program

__all__ = ["Channel", "Program", "ChannelGroup"]
