# mod-retail-warlock-pets

Demon looks for the warlocks of a 3.3.5a realm: 74 looks for the seven demons (imp, voidwalker,
succubus, felhunter, felguard, infernal, doomguard), picked per demon in the Demons tab of the
Transmogrify window.

It is a look pack for [wow-mod-transmog-plus](https://github.com/buildthehomelab/wow-mod-transmog-plus),
which has the tab, remembers what each character picked and swaps the model. A pack is two things:

- a small server module: its world SQL lists the looks (`data/sql/db-world/mod_retail_warlock_pets.sql`).
  There is no code to run and nothing to configure.
- a client patch, `patch-Y.MPQ`, with the new displays, textures and models. Everyone with the
  patch sees everyone's looks, with no client hacks.

Both are built from this repo's list of looks with
[wow-mod-retail-creatures](https://github.com/buildthehomelab/wow-mod-retail-creatures), the
converter the packs share.

## The demons

`data/demons.tsv` lists the looks. A warlock picks one per demon; "Default" is the demon's own.
A look changes what the demon looks like and nothing else: its reach, its hitbox and its
abilities stay the pet's own, and everyone sees it.

The list was made for a client with Project Reforged HD, which already gives each demon an HD
model, and those models are retail's own. So most looks sit on the client's models and keep
their effects:

| Kind | Looks | What the patch carries |
| --- | --- | --- |
| The client's own displays, at the pet's size | 26 | nothing |
| Client displays it only has at boss sizes (Observers, Shivarra, Voidcallers, the Illidari Abyssal) | 22 | a display row at the pet's size |
| Retail colours the client lacks (imps, felhunters, Darkglares, a Wrathguard, a Doomguard) | 13 | the textures, and a display row on the client's model |
| Retail models the client lacks (Incubus, Fel Succubus, Tyrant, Greater Observer, the older Felhound's colours, Infernal colours) | 13 | the converted model and its textures |

| Phase | Unlocks |
| --- | --- |
| 0 | Imp (Jade, Red), Succubus (Magenta, Blue), Felhound, Felguard (Blue, Yellow), Doomguard (Blue) |
| 1 Molten Core | Felguard (Red), Infernal (Fire) |
| 2 Onyxia | Felhound (Green), Felguard (White) |
| 3 Blackwing Lair | Imp (Blue) |
| 4 Zul'Gurub | Imp (Purple), Felhound (Dark), Doomguard (Yellow) |
| 5 AQ War Effort | Imp (Yellow), Felhunter (Purple) |
| 6 Ahn'Qiraj | Imp (White), Doom Lord |
| 7 Naxxramas | Felhunter (Violet), Infernal (Shadow), Doom Lord (Classic) |
| 8 Road to Outland | Fel Imp (Olive, Ashen), Outland Voidwalker (Blue), Felbeast (Red), Abyssal, Outland Doomguard (Crimson) |
| 9 Karazhan / Gruul / Magtheridon | Fel Imp (Red), Voidlord (Purple), Felbeast (Green), Wrathguard (Purple), Outland Doomguard (Black) |
| 10 SSC / Tempest Keep | Fel Imp (Purple), Voidlord (Blue), Observer (Blue, Green), Wrathguard (Red), Abyssal (Pale), Outland Doomguard (Blue) |
| 11 Hyjal / Black Temple | Outland Voidwalker (Purple), Shivarra (Blue), Observer (Red, Beige), Wrathguard (Black), Illidari Abyssal, Outland Doomguard (Green) |
| 12 Zul'Aman | Voidlord (Red), Fel Succubus, Observer (Black), Outland Doomguard (Yellow) |
| 13 Sunwell | Voidcaller (Blue), Shivarra (Black), Observer (Gray), Wrathguard (Green), Outland Doomguard (Purple) |
| 14 Naxxramas (80) / Eye of Eternity / Obsidian Sanctum | Voidcaller (Purple), Incubus, Darkglare (Purple), Demonic Tyrant |
| 15 Ulduar | Imp (Hologram), Darkglare (Green), Wrathguard (Yellow), Tyrant (Blue) |
| 16 Trial of the Crusader | Voidcaller (Red), Darkglare (Blue), Tyrant (Green) |
| 17 Icecrown Citadel | Incubus (Pale), Darkglare (Brown), Tyrant (Purple) |
| 18 Ruby Sanctum | Darkglare (Albino), Greater Observer, Tyrant (Red) |

Observers and Darkglares are felhunter looks, and Tyrants doomguard looks: 3.3.5a has no such
pets of their own.

The looks, their sources and their phases are listed in `tools/inventory.py`. To move a look,
change its phase there and rerun it.

Every look stands at about the pet's own height (a little more for demons that are bigger by
nature): the server swaps the display, not the scale. The sizes were measured from the models,
not seen in a client: if one is off, change its scale in `tools/inventory.py` and rebuild.

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
3. Build the client patch (below) and give it to every player. It has to be required: a player
   without it sees nothing where one of the patch's looks stands.

Without this module the realm is plain transmog for warlocks: no looks, no tab.

## Building the client patch

Clone the converter next to this repo (as `mod-retail-creatures`), or point `RETAIL_CREATURES` at it.

```bash
python3 tools/inventory.py --cache ~/retail-cache --dbc <dbc dir>
```

```bash
python3 ../mod-retail-creatures/tools/build_patch.py --pack . --dbc <dbc dir> --cache ~/retail-cache --work ~/mod_retail_warlock_pets-work --out patch-Y.MPQ --sql data/sql/db-world/mod_retail_warlock_pets.sql
```

`inventory.py` writes `data/demons.tsv` from the looks listed in it, and checks the client
display ids against the client's table. Display ids already given out never move. Run it only
after adding a look or moving one to another phase.

`--dbc` needs `CreatureDisplayInfo.dbc`, `CreatureModelData.dbc` and `AnimationData.dbc` as the
players' client has them. A patch replaces whole files, and the other packs' patches ship the
same two creature DBCs. The later letter wins, so each patch has to carry the rows of the ones
before it: on our realm the chain is R (druid forms), V (shaman totems), Y (this one), Z
(companion pets). Build Y with `--dbc` holding the two DBCs from the finished patch-V, and
rebuild patch-Z on Y's whenever Y changes.

The client has to be the Reforged HD one: 35 looks are rows on its models, and the retail
textures only fit those. On a stock 3.3.5a client the 26 own displays and the 13 converted
models still work; the resized and retextured ones would land on the classic models.

The build rewrites `data/sql/db-world/mod_retail_warlock_pets.sql` to match the patch: commit
it with the patch you ship. Ids: CreatureDisplayInfo and CreatureModelData from 98000, preview
creatures in 9502500-9502999 (subname `Demon Look`); `pack.json` has them all.

Nothing from Blizzard is stored in this repo; the files come from wago.tools at build time.

## Uninstalling

Remove the module folder, rebuild, and run
`data/sql/uninstall/mod_retail_warlock_pets_uninstall.sql` by hand. Players can keep the patch:
unused displays do nothing.

## Requirements

- AzerothCore with [wow-mod-transmog-plus](https://github.com/buildthehomelab/wow-mod-transmog-plus).
- A client with Project Reforged HD, for the looks on its models.
- To build the patch: [wow-mod-retail-creatures](https://github.com/buildthehomelab/wow-mod-retail-creatures)
  and what it needs (Python 3.10+, StormLib).

## Troubleshooting

- **No Demons tab**: mod-transmog-plus is older than the tab, `Transmog.Demons.Enable` is 0, or
  this module's SQL hasn't applied. At startup the worldserver log says whether it found warlock
  demon looks ("warlock demons: yes" or "no pack").
- **Other packs' looks vanish after adding patch-Y**: it was built on DBCs without their rows.
  Build it with `--dbc` from the patch before it in the chain.
- **Companion pets from a later patch vanish, or demon looks do**: the later patch wasn't
  rebuilt on patch-Y's DBCs.
- **A look is far bigger or smaller than the pet**: change its scale in `tools/inventory.py` and
  rebuild the patch.
- **A converted model has no flames or sparks**: those are particle effects, which the converter
  drops. Only the 13 converted looks are affected; the rest are the client's own models.
- Anything about the converted models themselves (black or tiny previews, white armour on other
  creatures): see the converter's
  [troubleshooting](https://github.com/buildthehomelab/wow-mod-retail-creatures#troubleshooting).

## Credits

- Model and table data: Blizzard Entertainment, downloaded at build time from
  [wago.tools](https://wago.tools); file names from the
  [wowdev community listfile](https://github.com/wowdev/wow-listfile).
- The HD demon models most looks sit on: Project Reforged HD.
- M2 format notes: [wowdev.wiki](https://wowdev.wiki/M2) and
  [whoa](https://github.com/thunderbrewhq/whoa).

## Patch Notes: Warlock Demon Looks

Category: Classes / Warlock

- Warlocks can now choose a look for each demon, from the new Demons tab of the Transmogrify
  window (`/transmog`): imp, voidwalker, succubus, felhunter, felguard, infernal and doomguard.
- Open from the start: Jade and Red imps, Magenta and Blue succubi, the older Felhound, Blue and
  Yellow felguards and the Blue doomguard.
- Every raid tier you clear unlocks more, 74 looks in all: Fel Imps, Voidlords and Voidcallers,
  Shivarra, the Incubus and the Fel Succubus, Observers and Darkglares, Wrathguards, Abyssals
  and fire and shadow Infernals, Doom Lords and Tyrants.
- A look only changes how the demon appears. Everyone sees it, and the demon fights exactly as
  before.

> Most looks are the client's own HD demons in new sizes and colours, with all their effects.
> Thirteen are converted retail models, which lose their particle effects on the way.

## License

MIT. See [LICENSE](LICENSE).
