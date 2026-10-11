#!/usr/bin/env python3
"""List the warlock demon looks and write data/demons.tsv.

    python3 inventory.py [--dbc <dir with the client's CreatureDisplayInfo.dbc>]

Every look so far is a display the realm's client already has (Project Reforged HD gives each
demon an HD model, effects and all), so they are listed here by client display id: no model to
convert, no patch. Each gets a name and the Individual Progression tier that unlocks it. With
--dbc, each display is checked against the client's table.

A display only makes a look if it shows the demon at about the pet's own size: the client has
most of these models at boss sizes too, and the server swaps the display, not the scale. The ones
here stand within 40% of the pet's own height.
"""
import argparse
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOOKS = os.path.join(HERE, "..", "data", "demons.tsv")
CLIENT_PREVIEW_BASE = 9502900   # client's own looks: base + position in CLIENT

# The demons, in tab order, with the pet's own display (the "default look", never listed).
DEMONS = [("imp", 4449), ("voidwalker", 1132), ("succubus", 4162), ("felhunter", 850),
          ("felguard", 14255), ("infernal", 169), ("doomguard", 1912)]

# Looks the client already has: (demon, name, tier, client display id). The tier is the Individual
# Progression state that unlocks the look (n = content n cleared, 0 = from the start).
CLIENT = [
    # Imp: the imp's other skins, and the Outland imp (retail's Fel Imp)
    ("imp", "Imp (Jade)", 0, 7552),
    ("imp", "Imp (Red)", 0, 10811),
    ("imp", "Fel Imp (Olive)", 8, 20104),                    # the road to Outland
    ("imp", "Fel Imp (Ashen)", 8, 21048),
    # Voidwalker: the Outland voidwalker and the Voidlord, skin and bracer colours
    ("voidwalker", "Outland Voidwalker (Blue and Purple)", 8, 17081),
    ("voidwalker", "Voidlord (Purple)", 9, 16635),           # Karazhan, Gruul, Magtheridon
    ("voidwalker", "Voidlord (Blue and Red)", 10, 18170),    # SSC and Tempest Keep
    # Succubus
    ("succubus", "Succubus (Magenta)", 0, 159),
    ("succubus", "Succubus (Blue)", 0, 2737),
    # Felhunter: the client's felhunter is the Legion felhound; this is the older one
    ("felhunter", "Felhound", 0, 10950),
    # Felguard: its other skins, and the Wrathguard, body and armour colours
    ("felguard", "Felguard (Blue)", 0, 5048),
    ("felguard", "Felguard (Yellow)", 0, 9015),
    ("felguard", "Felguard (Red)", 1, 18342),                # Molten Core
    ("felguard", "Felguard (White)", 2, 19901),              # Onyxia's Lair
    ("felguard", "Wrathguard (Purple)", 9, 17542),
    ("felguard", "Wrathguard (Red and Dark)", 10, 19599),
    ("felguard", "Wrathguard (Black)", 11, 19597),           # Hyjal and Black Temple
    ("felguard", "Wrathguard (Red)", 13, 20041),             # Sunwell Plateau
    ("felguard", "Wrathguard (Green)", 13, 20040),
    # Infernal
    ("infernal", "Abyssal", 8, 16874),
    # Doomguard: its blue skin, and the Outland doomguard
    ("doomguard", "Doomguard (Blue)", 0, 18311),
    ("doomguard", "Outland Doomguard (Crimson)", 8, 22809),
    ("doomguard", "Outland Doomguard (Black)", 9, 18143),
    ("doomguard", "Outland Doomguard (Blue)", 10, 17097),
    ("doomguard", "Outland Doomguard (Green)", 11, 17098),
    ("doomguard", "Outland Doomguard (Yellow)", 12, 17100),  # Zul'Aman
    ("doomguard", "Outland Doomguard (Purple)", 13, 17099),
]


def client_displays(folder):
    """Ids in the client's CreatureDisplayInfo.dbc."""
    data = open(os.path.join(folder, "CreatureDisplayInfo.dbc"), "rb").read()
    rows, _fields, size = struct.unpack_from("<3I", data, 4)
    return {struct.unpack_from("<I", data, 20 + i * size)[0] for i in range(rows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dbc", help="folder with the client's CreatureDisplayInfo.dbc, to check the display ids")
    args = ap.parse_args()

    order = [demon for demon, _own in DEMONS]
    own = {display for _demon, display in DEMONS}
    seen = set()
    for demon, name, _tier, display in CLIENT:
        if demon not in order:
            sys.exit("%s: no such demon '%s'" % (name, demon))
        if display in own:
            sys.exit("%s: display %d is a demon's own look" % (name, display))
        if display in seen:
            sys.exit("%s: display %d is listed twice" % (name, display))
        seen.add(display)
    if args.dbc:
        missing = sorted(seen - client_displays(args.dbc))
        if missing:
            sys.exit("not in the client's CreatureDisplayInfo.dbc: %s" % ", ".join(map(str, missing)))

    # In the tab a demon's looks run in unlock order.
    rows = sorted(enumerate(CLIENT), key=lambda x: (order.index(x[1][0]), x[1][2], x[0]))
    with open(LOOKS, "w", encoding="utf-8") as f:
        f.write("display\tretail_display\tvariant\tform\ttier\tmodel\tname\ttextures\tfolder\tpreview\n")
        for i, (demon, name, tier, display) in rows:
            f.write("\t".join(str(x) for x in (display, "", "", demon, tier, "", name, "", "",
                                               CLIENT_PREVIEW_BASE + i)) + "\n")
    print("%d looks (all from the client) -> %s" % (len(rows), LOOKS))


if __name__ == "__main__":
    main()
