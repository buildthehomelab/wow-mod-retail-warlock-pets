#!/usr/bin/env python3
"""List the warlock demon looks and write data/demons.tsv.

    python3 inventory.py --cache <download dir> [--dbc <dir with the client's CreatureDisplayInfo.dbc>]

A client with Project Reforged HD already gives each demon an HD model, and those models are
retail's own. So a look is one of four things, listed here by hand:

- CLIENT: a display the client has at the pet's size. Nothing to build, only the SQL.
- SCALED: a display the client only has at another size (a boss's). The patch adds a copy of
  its row at the pet's size, on the client's own model.
- RETEXTURED: a colour retail has and the client lacks. The patch adds the retail textures and
  a row using them on the client's own model, which keeps the client's effects.
- RETAIL: a model the client lacks, converted from retail's.

Each look gets a name and the Individual Progression tier that unlocks it. Display ids never
change once a player may have picked them. With --dbc, the client displays are checked against
the client's table.

Sizes: the server swaps the display, not the scale, so every look stands at about the pet's own
height (a little more for the demons that are bigger by nature). Heights were measured from the
models: vertex height x the model's scale x the display's scale.
"""
import argparse
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# fetch.py comes with the converter, wow-mod-retail-creatures: clone it next to this repo, or
# point RETAIL_CREATURES at its checkout.
for _repo in (os.environ.get("RETAIL_CREATURES"), os.path.join(HERE, "..", "..", "mod-retail-creatures"),
              os.path.join(HERE, "..", "..", "wow-mod-retail-creatures")):
    if _repo and os.path.isfile(os.path.join(_repo, "tools", "fetch.py")):
        sys.path.insert(0, os.path.join(_repo, "tools"))
        break
else:
    sys.exit("wow-mod-retail-creatures not found: clone it next to this repo, or set RETAIL_CREATURES")

from fetch import db2  # noqa: E402

LOOKS = os.path.join(HERE, "..", "data", "demons.tsv")
FIRST_DISPLAY = 98000           # the patch's rows; their previews are 9502500 + (display - 98000)
CLIENT_PREVIEW_BASE = 9502900   # client's own looks: base + position in CLIENT

# The demons, in tab order, with the pet's own display (the "default look", never listed).
DEMONS = [("imp", 4449), ("voidwalker", 1132), ("succubus", 4162), ("felhunter", 850),
          ("felguard", 14255), ("infernal", 169), ("doomguard", 1912)]

# Looks the client already has: (demon, name, tier, client display id). The tier is the Individual
# Progression state that unlocks the look (n = content n cleared, 0 = from the start). Most demon
# models take one texture, the skin: displays that differ only in a second one look the same.
CLIENT = [
    # Imp: the imp's other skins, and the Outland imp (retail's remade imp)
    ("imp", "Imp (Jade)", 0, 7552),
    ("imp", "Imp (Red)", 0, 10811),
    ("imp", "Fel Imp (Olive)", 8, 20104),                    # the road to Outland
    ("imp", "Fel Imp (Ashen)", 8, 21048),
    # Voidwalker: the Outland voidwalker and the Voidlord
    ("voidwalker", "Outland Voidwalker (Blue)", 8, 17081),
    ("voidwalker", "Voidlord (Purple)", 9, 16635),           # Karazhan, Gruul, Magtheridon
    ("voidwalker", "Voidlord (Blue)", 10, 18170),            # SSC and Tempest Keep
    # Succubus
    ("succubus", "Succubus (Magenta)", 0, 159),
    ("succubus", "Succubus (Blue)", 0, 2737),
    # Felhunter: the client's felhunter is the Legion felhound; this is the older one
    ("felhunter", "Felhound", 0, 10950),
    # Felguard: its other skins, and the Wrathguard
    ("felguard", "Felguard (Blue)", 0, 5048),
    ("felguard", "Felguard (Yellow)", 0, 9015),
    ("felguard", "Felguard (Red)", 1, 18342),                # Molten Core
    ("felguard", "Felguard (White)", 2, 19901),              # Onyxia's Lair
    ("felguard", "Wrathguard (Purple)", 9, 17542),
    ("felguard", "Wrathguard (Red)", 10, 20041),
    ("felguard", "Wrathguard (Black)", 11, 19597),           # Hyjal and Black Temple
    ("felguard", "Wrathguard (Green)", 13, 20040),           # Sunwell Plateau
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

# Client displays at another size: (demon, name, tier, display, client display id, scale). Clone
# only displays whose model id the stock 3.3.5a tables have (Felstalker and the Observer King are
# Reforged's own model rows).
SCALED = [
    ("imp", "Fel Imp (Red)", 9, 98000, 16888, 0.5),
    ("imp", "Fel Imp (Purple)", 10, 98001, 16889, 0.5),
    ("imp", "Imp (Hologram)", 15, 98002, 18510, 0.5),                 # Ulduar
    ("voidwalker", "Outland Voidwalker (Purple)", 11, 98003, 18953, 1.0),
    ("voidwalker", "Voidlord (Red)", 12, 98004, 26214, 1.0),
    ("voidwalker", "Voidcaller (Blue)", 13, 98005, 17704, 0.7),
    ("voidwalker", "Voidcaller (Purple)", 14, 98006, 17746, 0.7),     # Naxxramas (80), Eye of Eternity, Obsidian Sanctum
    ("voidwalker", "Voidcaller (Red)", 16, 98007, 19884, 0.7),        # Trial of the Crusader
    ("succubus", "Shivarra (Blue)", 11, 98008, 22422, 0.5),
    ("succubus", "Shivarra (Black)", 13, 98009, 19587, 0.5),
    ("felhunter", "Felbeast (Red)", 8, 98010, 28645, 0.35),
    ("felhunter", "Felbeast (Green)", 9, 98011, 18644, 0.35),
    ("felhunter", "Observer (Blue)", 10, 98012, 19579, 0.33),
    ("felhunter", "Observer (Green)", 10, 98013, 20528, 0.33),
    ("felhunter", "Observer (Red)", 11, 98014, 19877, 0.33),
    ("felhunter", "Observer (Beige)", 11, 98015, 19878, 0.33),
    ("felhunter", "Observer (Black)", 12, 98016, 21447, 0.33),
    ("felhunter", "Observer (Gray)", 13, 98017, 20527, 0.33),
    ("infernal", "Abyssal (Pale)", 10, 98018, 20810, 1.0),
    ("infernal", "Illidari Abyssal", 11, 98019, 21145, 1.5),
    ("doomguard", "Doom Lord", 6, 98020, 27788, 0.52),                # Temple of Ahn'Qiraj
    ("doomguard", "Doom Lord (Classic)", 7, 98021, 12449, 0.27),      # Naxxramas
]

# Retail colours on the client's own models: (demon, name, tier, display, client display id it is
# copied from, scale, retail display id whose textures it takes).
RETEXTURED = [
    ("imp", "Imp (Blue)", 3, 98030, 4449, 0.5, 113639),               # Blackwing Lair
    ("imp", "Imp (Purple)", 4, 98031, 4449, 0.5, 113641),             # Zul'Gurub
    ("imp", "Imp (Yellow)", 5, 98032, 4449, 0.5, 113644),             # Ahn'Qiraj War Effort
    ("imp", "Imp (White)", 6, 98033, 4449, 0.5, 113643),
    ("felhunter", "Felhunter (Purple)", 5, 98034, 850, 0.5, 113322),
    ("felhunter", "Felhunter (Violet)", 7, 98035, 850, 0.5, 113323),
    ("felguard", "Wrathguard (Yellow)", 15, 98036, 17542, 1.0, 100514),
    ("doomguard", "Doomguard (Yellow)", 4, 98037, 1912, 1.2, 63142),
    ("felhunter", "Darkglare (Purple)", 14, 98038, 19579, 0.33, 116130),
    ("felhunter", "Darkglare (Green)", 15, 98039, 19579, 0.33, 71752),
    ("felhunter", "Darkglare (Blue)", 16, 98040, 19579, 0.33, 116321),
    ("felhunter", "Darkglare (Brown)", 17, 98041, 19579, 0.33, 71751),  # Icecrown Citadel
    ("felhunter", "Darkglare (Albino)", 18, 98042, 19579, 0.33, 71749),  # Ruby Sanctum
]

# Models the client lacks, converted from retail: (demon, name, tier, display, retail display id,
# model, scale).
RETAIL = [
    ("felhunter", "Felhound (Green)", 2, 98050, 113549, "felhound2", 0.5),
    ("felhunter", "Felhound (Dark)", 4, 98051, 113550, "felhound2", 0.5),
    ("succubus", "Incubus", 14, 98052, 105009, "incubus", 0.31),
    ("succubus", "Incubus (Pale)", 17, 98053, 105010, "incubus", 0.31),
    ("succubus", "Fel Succubus", 12, 98054, 77400, "succubus2_fel", 1.0),
    ("infernal", "Infernal (Fire)", 1, 98055, 113801, "infernal2", 1.2),
    ("infernal", "Infernal (Shadow)", 7, 98056, 113802, "infernal2", 1.2),
    ("felhunter", "Greater Observer", 18, 98057, 73459, "greaterbeholder", 0.61),
    ("doomguard", "Demonic Tyrant", 14, 98058, 76701, "tyrant", 1.05),
    ("doomguard", "Tyrant (Blue)", 15, 98059, 74888, "tyrant", 1.05),
    ("doomguard", "Tyrant (Green)", 16, 98060, 74889, "tyrant", 1.05),
    ("doomguard", "Tyrant (Purple)", 17, 98061, 74890, "tyrant", 1.05),
    ("doomguard", "Tyrant (Red)", 18, 98062, 74891, "tyrant", 1.05),
]


def client_displays(folder):
    """Ids in the client's CreatureDisplayInfo.dbc."""
    data = open(os.path.join(folder, "CreatureDisplayInfo.dbc"), "rb").read()
    rows, _fields, size = struct.unpack_from("<3I", data, 4)
    return {struct.unpack_from("<I", data, 20 + i * size)[0] for i in range(rows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--dbc", help="folder with the client's CreatureDisplayInfo.dbc, to check the client display ids")
    args = ap.parse_args()
    cdi = db2(args.cache, "CreatureDisplayInfo")

    order = [demon for demon, _own in DEMONS]
    own = {display for _demon, display in DEMONS}
    # One row per look: (demon, tier, position, columns of the data file).
    looks = []
    for i, (demon, name, tier, display) in enumerate(CLIENT):
        if display in own:
            sys.exit("%s: display %d is a demon's own look" % (name, display))
        looks.append((demon, tier, dict(display=display, name=name, preview=CLIENT_PREVIEW_BASE + i)))
    for demon, name, tier, display, source, scale in SCALED:
        looks.append((demon, tier, dict(display=display, name=name, client_display=source, display_scale=scale)))
    for demon, name, tier, display, source, scale, retail in RETEXTURED:
        if str(retail) not in cdi:
            sys.exit("retail display %d (%s) is gone" % (retail, name))
        textures = ",".join(cdi[str(retail)]["TextureVariationFileDataID_%d" % k] for k in range(3))
        looks.append((demon, tier, dict(display=display, name=name, client_display=source, display_scale=scale, textures=textures)))
    for demon, name, tier, display, retail, model, scale in RETAIL:
        if str(retail) not in cdi:
            sys.exit("retail display %d (%s) is gone" % (retail, name))
        looks.append((demon, tier, dict(display=display, name=name, retail_display=retail, model=model, display_scale=scale)))

    seen, names, used = set(), set(), set()
    for demon, _tier, look in looks:
        if demon not in order:
            sys.exit("%s: no such demon '%s'" % (look["name"], demon))
        if look["display"] in seen or look["name"] in names:
            sys.exit("%s (%d) is listed twice" % (look["name"], look["display"]))
        seen.add(look["display"])
        names.add(look["name"])
        if "preview" not in look and not FIRST_DISPLAY <= look["display"] < FIRST_DISPLAY + 400:
            sys.exit("%s: display %d is outside the patch's block" % (look["name"], look["display"]))
        used.add(look["display"] if "preview" in look else look.get("client_display", 0))
    if args.dbc:
        missing = sorted(used - {0} - client_displays(args.dbc))
        if missing:
            sys.exit("not in the client's CreatureDisplayInfo.dbc: %s" % ", ".join(map(str, missing)))

    # In the tab a demon's looks run in unlock order.
    looks.sort(key=lambda x: (order.index(x[0]), x[1]))
    columns = ["display", "retail_display", "variant", "form", "tier", "model", "name", "textures", "folder",
               "preview", "client_display", "display_scale"]
    with open(LOOKS, "w", encoding="utf-8") as f:
        f.write("\t".join(columns) + "\n")
        for demon, tier, look in looks:
            row = dict(look, form=demon, tier=tier)
            f.write("\t".join(str(row.get(c, "")) for c in columns) + "\n")
    print("%d looks (%d the client's own, %d resized, %d retextured, %d converted) -> %s" % (
        len(looks), len(CLIENT), len(SCALED), len(RETEXTURED), len(RETAIL), LOOKS))


if __name__ == "__main__":
    main()
