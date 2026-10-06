#!/usr/bin/env python3
from enum import Enum


class Key(str, Enum):
    # --- volume / channel ---
    VOLUME_UP = "volumeup"
    VOLUME_DOWN = "volumedown"
    MUTE = "mute"
    CHANNEL_UP = "channelup"
    CHANNEL_DOWN = "channeldown"

    # --- navigation ---
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    OK = "select"
    BACK = "back"
    EXIT = "exit"
    INFO = "info"
    MENU = "menu"
    OPTIONS = "options"

    # --- colour buttons ---
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"

    # --- numbers ---
    NUMBER_0 = "0"
    NUMBER_1 = "1"
    NUMBER_2 = "2"
    NUMBER_3 = "3"
    NUMBER_4 = "4"
    NUMBER_5 = "5"
    NUMBER_6 = "6"
    NUMBER_7 = "7"
    NUMBER_8 = "8"
    NUMBER_9 = "9"
    ENTER = "enter"
    CLEAR = "clear"

    # --- playback / transport ---
    PLAY_PAUSE = "playpause"
    STOP = "stop"
    RECORD = "record"
    FAST_FORWARD = "ffwd"
    REWIND = "rwd"
    SKIP_FORWARD = "skipfwd"
    SKIP_BACK = "skipback"

    # --- shortcuts / screens ---
    GUIDE = "guide"
    VIDEO = "vod"
    TELETEXT = "teletext"
    RECENT = "recent"
    RECORDED_TV = "recordedtv"
    FAVORITES = "favorites"
    SEARCH = "search"
    HELP = "help"
    POWER = "power"

    # --- app shortcut slots ---
    APP_1 = "app1"
    APP_2 = "app2"
    APP_3 = "app3"
    APP_4 = "app4"
    APP_5 = "app5"
    APP_6 = "app6"

    def __str__(self):  # so str(member)/print() yield the wire value
        return self.value


ALL_KEYS = [k.value for k in Key]
