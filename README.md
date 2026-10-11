# mod-retail-warlock-pets

Demon looks for the warlocks of a 3.3.5a realm: 27 looks for the seven demons (imp, voidwalker,
succubus, felhunter, felguard, infernal, doomguard), picked per demon in the Demons tab of the
Transmogrify window.

It is a look pack for [wow-mod-transmog-plus](https://github.com/buildthehomelab/wow-mod-transmog-plus),
which has the tab, remembers what each character picked and swaps the model. This pack is a small
server module: its world SQL lists the looks (`data/sql/db-world/mod_retail_warlock_pets.sql`).
There is no code to run and nothing to configure.

There is no client patch yet. Every look so far is a display the realm's client already has:
Project Reforged HD gives each demon an HD model, effects and all. Looks that need new client data (retail models the
client lacks, and client models it only has at boss sizes) come with a patch later, built like
the other packs' with [wow-mod-retail-creatures](https://github.com/buildthehomelab/wow-mod-retail-creatures).

## The demons

`data/demons.tsv` lists the looks. A warlock picks one per demon; "Default" is the demon's own.
A look changes what the demon looks like and nothing else: its reach, its hitbox and its
abilities stay the pet's own, and everyone sees it.

| Phase | Unlocks |
| --- | --- |
| 0 | Imp (Jade, Red), Succubus (Magenta, Blue), Felhound, Felguard (Blue, Yellow), Doomguard (Blue) |
| 1 Molten Core | Felguard (Red) |
| 2 Onyxia | Felguard (White) |
| 8 Road to Outland | Fel Imp (Olive, Ashen), Outland Voidwalker, Abyssal, Outland Doomguard (Crimson) |
| 9 Karazhan / Gruul / Magtheridon | Voidlord (Purple), Wrathguard (Purple), Outland Doomguard (Black) |
| 10 SSC / Tempest Keep | Voidlord (Blue and Red), Wrathguard (Red and Dark), Outland Doomguard (Blue) |
| 11 Hyjal / Black Temple | Wrathguard (Black), Outland Doomguard (Green) |
| 12 Zul'Aman | Outland Doomguard (Yellow) |
| 13 Sunwell | Wrathguard (Red, Green), Outland Doomguard (Purple) |

The looks, their client display ids and their phases are listed in `tools/inventory.py`. To move
a look, change its phase there and rerun it.

A display only makes a look if it shows the demon at about the pet's own size. The client has
most of these models at boss sizes too (a Voidlord eight times a voidwalker's height), and the
server swaps the display, not the scale. The looks here stand within 40% of the pet's own
height; the rest wait for the patch, which can add a display at the right size.

## Installing

1. Install [wow-mod-transmog-plus](https://github.com/buildthehomelab/wow-mod-transmog-plus)
   (a version with the Demons tab).
2. Add this module and rebuild. The SQL applies on the next start, and the warlocks' Demons tab
   appears.

   ```bash
   cd azerothcore/modules
   git clone https://github.com/buildthehomelab/wow-mod-retail-warlock-pets.git mod-retail-warlock-pets
   ```

   Clone into `mod-retail-warlock-pets` exactly: AzerothCore derives the module's loader function
   from the folder name.

Without this module the realm is plain transmog for warlocks: no looks, no tab.

The list was made on a Reforged HD client. On a stock 3.3.5a client the same display ids are the
classic models of the same demons, so the looks still work, in their classic shape.

## Rebuilding the look list

```bash
python3 tools/inventory.py --dbc <dbc dir>
```

Then, with the converter cloned next to this repo (as `mod-retail-creatures`):

```bash
python3 ../mod-retail-creatures/tools/build_patch.py --pack . --dbc <dbc dir> --cache ~/retail-cache --work ~/mod_retail_warlock_pets-work --out ~/mod_retail_warlock_pets-work/unused.MPQ --sql data/sql/db-world/mod_retail_warlock_pets.sql
```

`inventory.py` writes `data/demons.tsv` from the looks listed in it; with `--dbc` it checks each
display id against the client's `CreatureDisplayInfo.dbc`. The second command writes the SQL.
While every look is the client's own, the patch file it also writes holds nothing new: throw it
away.

Ids: preview creatures in 9502500-9502999 (subname `Demon Look`), and CreatureDisplayInfo and
CreatureModelData from 98000 for the looks the patch will add; `pack.json` has them all.

## Uninstalling

Remove the module folder, rebuild, and run
`data/sql/uninstall/mod_retail_warlock_pets_uninstall.sql` by hand.

## Requirements

- AzerothCore with [wow-mod-transmog-plus](https://github.com/buildthehomelab/wow-mod-transmog-plus).
- To rebuild the list: [wow-mod-retail-creatures](https://github.com/buildthehomelab/wow-mod-retail-creatures)
  and what it needs (Python 3.10+, StormLib).

## Troubleshooting

- **No Demons tab**: mod-transmog-plus is older than the tab, `Transmog.Demons.Enable` is 0, or
  this module's SQL hasn't applied. At startup the worldserver log says whether it found warlock
  demon looks ("warlock demons: yes" or "no pack").
- **A look is far bigger or smaller than the pet**: that client's table has the display at
  another size than the Reforged one the list was made on. Take the look out of
  `tools/inventory.py`, or pick another display of the same model.

## Patch Notes: Warlock Demon Looks

Category: Classes / Warlock

- Warlocks can now choose a look for each demon, from the new Demons tab of the Transmogrify
  window (`/transmog`): imp, voidwalker, succubus, felhunter, felguard, infernal and doomguard.
- Open from the start: Jade and Red imps, Magenta and Blue succubi, the older Felhound, Blue and
  Yellow felguards and the Blue doomguard.
- Clearing raid tiers unlocks more: Fel Imps, the Outland Voidwalker and Voidlords, Wrathguards,
  the Abyssal and the Outland Doomguards.
- A look only changes how the demon appears. Everyone sees it, and the demon fights exactly as
  before.

## License

MIT. See [LICENSE](LICENSE).
