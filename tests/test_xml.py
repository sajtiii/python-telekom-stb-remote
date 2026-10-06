#!/usr/bin/env python3
"""Box replies with a raw ``&`` in an attribute must still parse. Run: python tests/test_xml.py"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from telekom_iptv_remote.types.remote.activity import Activity
from telekom_iptv_remote.utils import localname, parse_xml

ACTIVITY = """<?xml version="1.0" encoding="utf-8"?>
<response xmlns="http://schemas.microsoft.com/mediaroom/2009/companion">
<data xmlns="http://schemas.microsoft.com/mediaroom/2009/datasource/list" source="activity">
<item name="channel" value="13"/>
<item name="volume" value="18"/>
<item name="awake" value="1"/>
<item name="application" value="https://example.test/pair?ip=192.168.0.101&amp;pairingkey=abc&pincode=0000"/>
</data>
</response>
"""


def main():
    root = parse_xml(ACTIVITY.replace("&amp;pairingkey", "&pairingkey"))
    data = next(e for e in root.iter() if localname(e.tag) == "data")
    act = Activity.from_element(data)
    assert act.channel == 13
    assert act.volume == 18
    assert (
        act.application == "https://example.test/pair?ip=192.168.0.101&pairingkey=abc&pincode=0000"
    )

    already = parse_xml(ACTIVITY)
    data = next(e for e in already.iter() if localname(e.tag) == "data")
    assert Activity.from_element(data).application.endswith("pairingkey=abc&pincode=0000")
    print("PASS  bare ampersand in activity XML")


if __name__ == "__main__":
    main()
