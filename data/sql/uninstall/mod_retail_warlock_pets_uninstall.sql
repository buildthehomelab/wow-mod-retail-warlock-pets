-- Removes this pack's looks. Run by hand (the server never applies data/sql/uninstall), on
-- acore_world and acore_characters as marked. Players can keep patch-Y: unused displays do nothing.

-- acore_world
DELETE FROM `mod_transmog_plus_forms` WHERE `Form` IN ('imp', 'voidwalker', 'succubus', 'felhunter', 'felguard', 'infernal', 'doomguard');
DELETE m FROM `creature_template_model` m JOIN `creature_template` t ON t.`entry` = m.`CreatureID`
WHERE t.`entry` BETWEEN 9502500 AND 9502999 AND t.`subname` = 'Demon Look';
DELETE t FROM `creature_template` t WHERE t.`entry` BETWEEN 9502500 AND 9502999 AND t.`subname` = 'Demon Look';
DELETE FROM `creature_model_info` WHERE `DisplayID` BETWEEN 98000 AND 98499;
DELETE FROM `creaturedisplayinfo_dbc` WHERE `ID` BETWEEN 98000 AND 98499;
DELETE FROM `creaturemodeldata_dbc` WHERE `ID` BETWEEN 98000 AND 98499;
-- creaturemodeldata_dbc 90008 (the Reforged client's felhunter model, which two looks sit on) stays:
-- it is the client's own row, and harmless without the looks.

-- acore_characters: the looks characters picked from this pack
-- DELETE FROM `mod_transmog_plus_form_choice` WHERE `Form` BETWEEN 11 AND 17;
