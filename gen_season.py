# -*- coding: utf-8 -*-
"""
gen_season.py v4 — Eine Datenquelle für den kompletten Saison-Content von
mod-battlepass v4 (Community-Pass, zweisprachig Deutsch/Englisch).

Neu in v4: echte Umlaute, alle Namen zweisprachig (name/name_en, Items über
item_template_locale), Zufallskisten (Pool per SELECT aus item_template,
800+ Items), Wochen-Mutatoren, Kisten-Belohnungsstufen.

Aufruf:  python gen_season.py
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))
SQL_WORLD = os.path.join(BASE, "mod-battlepass", "data", "sql", "db-world")
ADDON = os.path.join(BASE, "BattlePassUI")

SEASON = 1
SEASON_NAME = "Ruf der Alptraumdrachen"
SEASON_NAME_EN = "Call of the Nightmare Dragons"
MAX_TIER = 100
TIER_COST = 100

CLASSES = {
    1:  ("WARRIOR",     0x001, "Krieger"),
    2:  ("PALADIN",     0x002, "Paladin"),
    3:  ("HUNTER",      0x004, "Jäger"),
    4:  ("ROGUE",       0x008, "Schurke"),
    5:  ("PRIEST",      0x010, "Priester"),
    6:  ("DEATHKNIGHT", 0x020, "Todesritter"),
    7:  ("SHAMAN",      0x040, "Schamane"),
    8:  ("MAGE",        0x080, "Magier"),
    9:  ("WARLOCK",     0x100, "Hexenmeister"),
    11: ("DRUID",       0x400, "Druide"),
}

# Klassensets: (slot, Slotname, Klonquelle, Name DE, Name EN)
CLASS_SETS = {
    1:  [(1, "Waffe",     44096, "Alptraumklinge", "Nightmare Blade"),
         (2, "Schultern", 42949, "Schulterwacht des Alptraumwandlers", "Shoulderguard of the Nightmare Walker"),
         (3, "Brust",     48677, "Brustplatte des Alptraumwandlers", "Breastplate of the Nightmare Walker"),
         (4, "Schmuck",   42991, "Traumsplitter des Schlachtenmeisters", "Dreamshard of the Battlemaster")],
    2:  [(1, "Waffe",     42945, "Streitkolben des geweihten Traums", "Mace of the Hallowed Dream"),
         (2, "Schultern", 42949, "Schulterplatten der Traumwacht", "Shoulderplates of the Dream Watch"),
         (3, "Brust",     48677, "Brustharnisch der Traumwacht", "Breastplate of the Dream Watch"),
         (4, "Schmuck",   42991, "Traumsplitter des Kreuzfahrers", "Dreamshard of the Crusader")],
    3:  [(1, "Waffe",     42946, "Alptraumbogen des Fernschützen", "Nightmare Bow of the Marksman"),
         (2, "Schultern", 42952, "Schulterstücke des Traumpirschers", "Spaulders of the Dream Stalker"),
         (3, "Brust",     42984, "Harnisch des Traumpirschers", "Harness of the Dream Stalker"),
         (4, "Schmuck",   42991, "Traumsplitter des Wildtierherrn", "Dreamshard of the Beast Lord")],
    4:  [(1, "Waffe",     44091, "Alptraumdolch der Schatten", "Nightmare Dagger of Shadows"),
         (2, "Schultern", 42952, "Schattengewebte Traumschultern", "Shadowwoven Dream Spaulders"),
         (3, "Brust",     42984, "Weste des Traumschleichers", "Vest of the Dream Creeper"),
         (4, "Schmuck",   42991, "Traumsplitter des Meuchlers", "Dreamshard of the Assassin")],
    5:  [(1, "Waffe",     42947, "Stab der stillen Träume", "Staff of Silent Dreams"),
         (2, "Schultern", 44098, "Mantel des Traumsehers", "Mantle of the Dream Seer"),
         (3, "Brust",     42985, "Robe des Traumsehers", "Robe of the Dream Seer"),
         (4, "Schmuck",   42992, "Traumsplitter des Lichts", "Dreamshard of the Light")],
    6:  [(1, "Waffe",     42943, "Runenklinge des ewigen Alptraums", "Runeblade of the Eternal Nightmare"),
         (2, "Schultern", 42949, "Schulterwacht des Frostträumers", "Shoulderguard of the Frost Dreamer"),
         (3, "Brust",     48677, "Brustplatte des Frostträumers", "Breastplate of the Frost Dreamer"),
         (4, "Schmuck",   42991, "Traumsplitter des Verdammten", "Dreamshard of the Damned")],
    7:  [(1, "Waffe",     42948, "Totemhammer der Traumgeister", "Totem Hammer of the Dream Spirits"),
         (2, "Schultern", 42951, "Schulterstücke des Elementartraums", "Spaulders of the Elemental Dream"),
         (3, "Brust",     48683, "Weste des Elementartraums", "Vest of the Elemental Dream"),
         (4, "Schmuck",   42992, "Traumsplitter des Sehers", "Dreamshard of the Seer")],
    8:  [(1, "Waffe",     44095, "Stab des arkanen Alptraums", "Staff of the Arcane Nightmare"),
         (2, "Schultern", 44098, "Mantel des Traumwebers", "Mantle of the Dream Weaver"),
         (3, "Brust",     42985, "Robe des Traumwebers", "Robe of the Dream Weaver"),
         (4, "Schmuck",   42992, "Traumsplitter des Gelehrten", "Dreamshard of the Scholar")],
    9:  [(1, "Waffe",     44091, "Dolch des flüsternden Alptraums", "Dagger of the Whispering Nightmare"),
         (2, "Schultern", 44098, "Mantel des Seelentraums", "Mantle of the Soul Dream"),
         (3, "Brust",     42985, "Robe des Seelentraums", "Robe of the Soul Dream"),
         (4, "Schmuck",   42992, "Traumsplitter des Beschwörers", "Dreamshard of the Summoner")],
    11: [(1, "Waffe",     44095, "Stab des Smaragdgrünen Traums", "Staff of the Emerald Dream"),
         (2, "Schultern", 42952, "Schulterstücke des Traumwandlers", "Spaulders of the Dream Walker"),
         (3, "Brust",     42984, "Wildlederweste des Traumwandlers", "Wildhide Vest of the Dream Walker"),
         (4, "Schmuck",   42992, "Traumsplitter der Wildnis", "Dreamshard of the Wilds")],
}
# Klassenset frueh im Pass: Waffe sofort (Schaden!), Schultern/Brust = +10% XP
SET_TIERS = {1: 1, 2: 5, 3: 10, 4: 15}

# Willkommenspaket (Stufe 0, wird automatisch bei der ersten Anmeldung vergeben):
# reitbares Traumross OHNE Reiten-Voraussetzung + Cosmetic-Set (nur Optik)
WELCOME = [
    (0, 900134, 1, "Traumkrone der Illidari", "Dream Cowl of the Illidari"),
    (0, 900135, 1, "Wappenrock des Traumkreuzzugs", "Tabard of the Dream Crusade"),
    (0, 900136, 1, "Traumkugel der Täuschung", "Dream Orb of Deception"),
    (1, 50000,  1, "5 Gold Startkapital", "5 gold starting capital"),
]

# Mount-Klone OHNE Anforderungen: Quelle -> (Entry, DE, EN)
# WICHTIG: 900121+ — die Bereiche 900011-900114 gehören den Klassensets
# (900000 + KlassenID*10 + Slot), sonst kollidieren Priester/DK/Schamane!
MOUNT_CLONES = {
    43952: (900121, "Zügel des azurblauen Drachen", "Reins of the Azure Drake"),
    43955: (900122, "Zügel des bronzenen Drachen", "Reins of the Bronze Drake"),
    44160: (900123, "Zügel des roten Protodrachen", "Reins of the Red Proto-Drake"),
    38576: (900124, "Großer Schlachtenbär", "Big Battle Bear"),
    33225: (900125, "Zügel des flinken Astraltigers", "Reins of the Swift Astral Tiger"),
    32458: (900126, "Asche von Al'ar", "Ashes of Al'ar"),
    50818: (900127, "Unbesiegbars Zügel", "Invincible's Reins"),
    43986: (900128, "Zügel des schwarzen Drachen", "Reins of the Black Drake"),
    49636: (900129, "Zügel des Onyxiadrachen", "Reins of the Onyxian Drake"),
    43959: (900130, "Zügel des Großen Schwarzen Kriegsmammuts", "Grand Black War Mammoth"),
    45693: (900131, "Mimirons Kopf", "Mimiron's Head"),
    46778: (900132, "Magisches Hahnenei", "Magic Rooster Egg"),
}

SPECIAL_ITEMS = [
    (900101, 43954, "Zügel des Alptraumdrachen", "Reins of the Nightmare Drake",
     "Traumpfad Saison 1 - Endbelohnung des Heldenpfads"),
    (900102, 23709, "Wappenrock des Alptraums", "Tabard of the Nightmare",
     "Traumpfad Saison 1 - Wappenrock des Heldenpfads"),
    # Willkommenspaket: Mount ohne Reit-Voraussetzung + Kult-Cosmetics
    (900133, 13335, "Zügel des Traumrosses", "Reins of the Dream Steed",
     "Traumpfad Saison 1 - Willkommensgeschenk, reitbar ohne Reitfertigkeit"),
    (900134, 32525, "Traumkrone der Illidari", "Dream Cowl of the Illidari",
     "Traumpfad Saison 1 - Kult-Cosmetic: der legendaere Illidari-Look aus dem Schwarzen Tempel"),
    (900135, 23192, "Wappenrock des Traumkreuzzugs", "Tabard of the Dream Crusade",
     "Traumpfad Saison 1 - Kult-Cosmetic: der Scharlachrote Wappenrock"),
    (900136, 1973,  "Traumkugel der Täuschung", "Dream Orb of Deception",
     "Traumpfad Saison 1 - Kult-Cosmetic: verwandle dein Spiegelbild!"),
]

def set_entry(class_id, slot):
    return 900000 + class_id * 10 + slot

def mount(orig):
    return MOUNT_CLONES[orig][0]

# ---------------------------------------------------------------------------
# Belohnungen. type: 0=Item 1=Gold(Kupfer) 2=Titel 3=Zufallskiste (id=Kistenstufe)
# track: 0=Abenteuer, 1=Helden — BEIDE KOSTENLOS.
# ---------------------------------------------------------------------------
CHEST_NAMES = {
    0: ("Traumkiste", "Dream Chest"),
    1: ("Blaue Traumkiste", "Blue Dream Chest"),
    2: ("Mythische Traumkiste", "Mythic Dream Chest"),
    3: ("Goldene Traumkiste", "Golden Dream Chest"),
}

# ---------------------------------------------------------------------------
# Zufallskisten v5: kuratierter Beutepool (100 Einträge) statt SELECT-Pool.
# CHEST_RARITY: Promille-Chancen je Kiste (Häufig, Selten, Episch, Legendär).
# Kistenfieber verstärkt Episch+Legendär multiplikativ. Kiste 2/3 garantieren
# in der 1. Ziehung mindestens Selten/Episch. Ziehungen je Kiste: 2/3/4.
# ---------------------------------------------------------------------------
# Zeile 0 = Qualitäts-Chancen der Traumkiste beim Öffnen (Blau/Mythisch/Golden, Promille)
CHEST_RARITY = { 0: (500, 350, 150, 0),
                 1: (700, 240, 55, 5), 2: (450, 380, 150, 20), 3: (250, 450, 250, 50) }

# (Rarität 1-4, kind 0=Item/1=Gold(id=Kupfer)/2=Verlorene Rune, id, Anzahl,
#  DE, EN, Gewichte je Kiste (K1,K2,K3) — 0 = kommt in dieser Kiste nicht vor)
CHEST_LOOT = [
    # ---- Häufig (Tränke, Essen, Spaßkram, Nieten) ----
    (1, 0, 929,    1, "Heiltrank", "Healing Potion", (12, 8, 5)),
    (1, 0, 1710,   2, "Großer Heiltrank", "Greater Healing Potion", (12, 8, 5)),
    (1, 0, 3928,   2, "Vorzüglicher Heiltrank", "Superior Healing Potion", (10, 8, 5)),
    (1, 0, 13446,  3, "Bedeutender Heiltrank", "Major Healing Potion", (10, 10, 8)),
    (1, 0, 33447,  5, "Runenverzierter Heiltrank", "Runic Healing Potion", (8, 10, 10)),
    (1, 0, 3827,   2, "Manatrank", "Mana Potion", (10, 8, 5)),
    (1, 0, 13444,  3, "Bedeutender Manatrank", "Major Mana Potion", (10, 10, 8)),
    (1, 0, 33448,  5, "Runenverzierter Manatrank", "Runic Mana Potion", (8, 10, 10)),
    (1, 0, 2459,   2, "Flinkheitstrank", "Swiftness Potion", (8, 8, 8)),
    (1, 0, 5634,   2, "Trank der ungehinderten Aktion", "Free Action Potion", (6, 8, 8)),
    (1, 0, 8529,   5, "Noggenfoggerelixier", "Noggenfogger Elixir", (8, 8, 8)),
    (1, 0, 6522,   5, "Abweichlerfisch", "Deviate Fish", (8, 8, 6)),
    (1, 0, 4536,   5, "Glänzender roter Apfel", "Shiny Red Apple", (10, 5, 3)),
    (1, 0, 117,    5, "Zähes Dörrfleisch", "Tough Jerky", (10, 5, 3)),
    (1, 0, 1179,   5, "Eiskalte Milch", "Ice Cold Milk", (10, 5, 3)),
    (1, 0, 8952,   5, "Gebratene Wachtel", "Roasted Quail", (8, 6, 4)),
    (1, 0, 21215,  3, "Graccus Hackfleisch-Früchtekuchen", "Graccu's Mince Meat Fruitcake", (6, 6, 6)),
    (1, 0, 17202, 10, "Schneeball", "Snowball", (8, 6, 6)),
    (1, 0, 21557,  5, "Kleine rote Rakete", "Small Red Rocket", (6, 6, 6)),
    (1, 0, 21558,  5, "Kleine blaue Rakete", "Small Blue Rocket", (6, 6, 6)),
    (1, 0, 21559,  5, "Kleine grüne Rakete", "Small Green Rocket", (6, 6, 6)),
    (1, 0, 10305,  3, "Schriftrolle des Schutzes IV", "Scroll of Protection IV", (6, 6, 4)),
    (1, 0, 10307,  3, "Schriftrolle der Ausdauer IV", "Scroll of Stamina IV", (6, 6, 4)),
    (1, 0, 10308,  3, "Schriftrolle der Intelligenz IV", "Scroll of Intellect IV", (6, 6, 4)),
    (1, 0, 10309,  3, "Schriftrolle der Stärke IV", "Scroll of Strength IV", (6, 6, 4)),
    (1, 0, 10310,  3, "Schriftrolle der Beweglichkeit IV", "Scroll of Agility IV", (6, 6, 4)),
    (1, 0, 14530,  5, "Schwerer Runenstoffverband", "Heavy Runecloth Bandage", (8, 6, 4)),
    (1, 0, 21991,  5, "Schwerer Netherstoffverband", "Heavy Netherweave Bandage", (6, 8, 6)),
    (1, 0, 34722,  5, "Schwerer Frostgewebeverband", "Heavy Frostweave Bandage", (6, 8, 8)),
    (1, 0, 2589,  20, "Leinenstoff", "Linen Cloth", (10, 4, 2)),
    (1, 0, 14047, 20, "Runenstoff", "Runecloth", (8, 6, 3)),
    (1, 0, 21877, 20, "Netherstoff", "Netherweave Cloth", (6, 8, 4)),
    (1, 0, 33470, 20, "Frostgewebe", "Frostweave Cloth", (6, 8, 8)),
    (1, 1, 10000,  1, "1 Gold", "1 gold", (10, 6, 4)),
    (1, 1, 30000,  1, "3 Gold", "3 gold", (6, 8, 6)),
    (1, 0, 6256,   1, "Angel (Niete!)", "Fishing Pole (dud!)", (5, 3, 2)),
    (1, 0, 2901,   1, "Spitzhacke (Niete!)", "Mining Pick (dud!)", (5, 3, 2)),
    (1, 0, 7005,   1, "Häutemesser (Niete!)", "Skinning Knife (dud!)", (5, 3, 2)),
    # ---- Selten (Taschen, Fläschchen, Haustiere, Gold) ----
    (2, 0, 21841,  1, "Netherstofftasche (16 Plätze)", "Netherweave Bag (16 slots)", (10, 10, 8)),
    (2, 0, 41599,  1, "Frostgewebetasche (20 Plätze)", "Frostweave Bag (20 slots)", (5, 8, 10)),
    (2, 0, 4500,   1, "Reiserucksack", "Traveler's Backpack", (10, 6, 4)),
    (2, 0, 46376,  2, "Fläschchen des Frostwyrms", "Flask of the Frost Wyrm", (6, 8, 10)),
    (2, 0, 46377,  2, "Fläschchen der endlosen Wut", "Flask of Endless Rage", (6, 8, 10)),
    (2, 0, 46379,  2, "Fläschchen des Steinbluts", "Flask of Stoneblood", (6, 8, 10)),
    (2, 0, 9206,   3, "Elixier der Riesen", "Elixir of Giants", (8, 6, 4)),
    (2, 0, 20749,  3, "Brillantes Zauberöl", "Brilliant Wizard Oil", (6, 6, 4)),
    (2, 0, 18262,  3, "Elementarschleifstein", "Elemental Sharpening Stone", (6, 6, 4)),
    (2, 0, 6657,   3, "Wohlschmeckende Abweichlerköstlichkeit", "Savory Deviate Delight", (8, 8, 6)),
    (2, 0, 8410,   3, "R.O.I.D.S.", "R.O.I.D.S.", (6, 6, 4)),
    (2, 0, 34754,  5, "Mega-Mammut-Mahl", "Mega Mammoth Meal", (5, 8, 8)),
    (2, 1, 100000, 1, "10 Gold", "10 gold", (10, 10, 8)),
    (2, 1, 200000, 1, "20 Gold", "20 gold", (5, 8, 10)),
    (2, 0, 8485,   1, "Katzentrage (Bombaykatze)", "Cat Carrier (Bombay)", (6, 6, 5)),
    (2, 0, 8486,   1, "Katzentrage (Cornish-Rex-Katze)", "Cat Carrier (Cornish Rex)", (6, 6, 5)),
    (2, 0, 8487,   1, "Katzentrage (Orange getigert)", "Cat Carrier (Orange Tabby)", (6, 6, 5)),
    (2, 0, 8488,   1, "Katzentrage (Silbern getigert)", "Cat Carrier (Silver Tabby)", (6, 6, 5)),
    (2, 0, 8489,   1, "Katzentrage (Weißes Kätzchen)", "Cat Carrier (White Kitten)", (6, 6, 5)),
    (2, 0, 8490,   1, "Katzentrage (Siamkatze)", "Cat Carrier (Siamese)", (6, 6, 5)),
    (2, 0, 4401,   1, "Mechanisches Eichhörnchen", "Mechanical Squirrel Box", (6, 6, 5)),
    (2, 0, 11026,  1, "Baumfroschbox", "Tree Frog Box", (6, 6, 5)),
    (2, 0, 11027,  1, "Waldfroschbox", "Wood Frog Box", (6, 6, 5)),
    (2, 0, 10393,  1, "Kakerlake", "Cockroach", (6, 6, 5)),
    (2, 0, 8495,   1, "Papageienkäfig (Grünflügelara)", "Parrot Cage (Green Wing Macaw)", (6, 6, 5)),
    (2, 0, 44228,  1, "Baby-Blizzardbär", "Baby Blizzard Bear", (4, 5, 6)),
    # ---- Episch (Kult-Cosmetics, TCG-Spaß, Gold, Verlorene Rune) ----
    (3, 0, 1973,   1, "Kugel der Täuschung", "Orb of Deception", (8, 8, 8)),
    (3, 0, 13379,  1, "Piccoloflöte des flammenden Feuers", "Piccolo of the Flaming Fire", (8, 8, 8)),
    (3, 0, 18660,  1, "Weltvergrößerer", "World Enlarger", (8, 8, 8)),
    (3, 0, 38506,  1, "Don Carlos' berühmter Hut", "Don Carlos' Famous Hat", (6, 8, 8)),
    (3, 0, 38578,  1, "Die Flagge des Besitzanspruchs", "The Flag of Ownership", (6, 8, 8)),
    (3, 0, 36863,  1, "Dekaedrischer Zwergenwürfel", "Decahedral Dwarven Dice", (6, 8, 8)),
    (3, 0, 19970,  1, "Arkanitangelrute", "Arcanite Fishing Pole", (5, 6, 8)),
    (3, 0, 23705,  1, "Wappenrock der Flamme", "Tabard of Flame", (6, 6, 6)),
    (3, 0, 23709,  1, "Wappenrock des Frosts", "Tabard of Frost", (6, 6, 6)),
    (3, 0, 43154,  1, "Wappenrock des Argentumkreuzzugs", "Tabard of the Argent Crusade", (6, 6, 6)),
    (3, 0, 43157,  1, "Wappenrock des Kirin Tor", "Tabard of the Kirin Tor", (6, 6, 6)),
    (3, 0, 8494,   1, "Hyazinthara", "Hyacinth Macaw", (4, 6, 8)),
    (3, 0, 8491,   1, "Katzentrage (Schwarz getigert)", "Cat Carrier (Black Tabby)", (5, 6, 6)),
    (3, 0, 38658,  1, "Vampirfledermausjunges", "Vampiric Batling", (5, 6, 6)),
    (3, 0, 23713,  1, "Hippogryphjunges", "Hippogryph Hatchling", (5, 6, 6)),
    (3, 0, 38628,  1, "Netherrochenbaby", "Nether Ray Fry", (5, 6, 6)),
    (3, 0, 34499,  1, "Papierzeppelin-Bausatz", "Paper Zeppelin Kit", (5, 6, 6)),
    (3, 1, 500000, 1, "50 Gold", "50 gold", (8, 8, 8)),
    (3, 1, 1000000, 1, "100 Gold", "100 gold", (4, 6, 8)),
    (3, 2, 0,      1, "Verlorene Rune", "Lost Rune", (8, 10, 12)),
    # ---- Legendär (die verdammt seltenen Mounts + Jackpots) ----
    (4, 0, 900133, 1, "Zügel des Traumrosses", "Reins of the Dream Steed", (30, 20, 12)),
    (4, 0, 900124, 1, "Großer Schlachtenbär", "Big Battle Bear", (20, 18, 12)),
    (4, 0, 900125, 1, "Zügel des flinken Astraltigers", "Reins of the Swift Astral Tiger", (18, 16, 12)),
    (4, 0, 900122, 1, "Zügel des bronzenen Drachen", "Reins of the Bronze Drake", (14, 14, 12)),
    (4, 0, 900128, 1, "Zügel des schwarzen Drachen", "Reins of the Black Drake", (12, 14, 12)),
    (4, 0, 900121, 1, "Zügel des azurblauen Drachen", "Reins of the Azure Drake", (10, 12, 12)),
    (4, 0, 900123, 1, "Zügel des roten Protodrachen", "Reins of the Red Proto-Drake", (8, 10, 10)),
    (4, 0, 900129, 1, "Zügel des Onyxiadrachen", "Reins of the Onyxian Drake", (6, 9, 10)),
    (4, 0, 900130, 1, "Großes Schwarzes Kriegsmammut", "Grand Black War Mammoth", (6, 9, 10)),
    (4, 0, 900132, 1, "Magisches Hahnenei", "Magic Rooster Egg", (4, 7, 8)),
    (4, 0, 900126, 1, "Asche von Al'ar", "Ashes of Al'ar", (0, 4, 6)),
    (4, 0, 900131, 1, "Mimirons Kopf", "Mimiron's Head", (0, 3, 5)),
    (4, 0, 900127, 1, "Unbesiegbars Zügel", "Invincible's Reins", (0, 2, 4)),
    (4, 0, 900101, 1, "Zügel des Alptraumdrachen", "Reins of the Nightmare Drake", (0, 0, 3)),
    (4, 1, 2500000, 1, "250 Gold Jackpot", "250 gold jackpot", (15, 12, 8)),
    (4, 1, 5000000, 1, "500 Gold Jackpot", "500 gold jackpot", (0, 8, 8)),
]

FREE_SPECIALS = {
    5:   (0, 6657,  5,  "Wohlschmeckende Abweichlerköstlichkeit x5", "Savory Deviate Delight x5"),
    10:  (0, 40752, 10, "10x Emblem des Heldentums", "10x Emblem of Heroism"),
    13:  (0, 18660, 1,  "Weltvergrößerer", "World Enlarger"),
    15:  (0, 23705, 1,  "Wappenrock der Flamme", "Tabard of Flame"),
    22:  (0, 8500,  1,  "Papageienkäfig (Nymphensittich)", "Parrot Cage (Cockatiel)"),
    20:  (0, 40753, 10, "10x Emblem der Ehre", "10x Emblem of Valor"),
    25:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    30:  (0, 8491,  1,  "Katzentrage (Schwarz getigert)", "Cat Carrier (Black Tabby)"),
    33:  (2, 143,   1,  "Titel: Jenkins", "Title: Jenkins"),
    35:  (0, 23709, 1,  "Wappenrock des Frosts", "Tabard of Frost"),
    40:  (0, 45624, 10, "10x Emblem der Eroberung", "10x Emblem of Conquest"),
    42:  (0, 10360, 1,  "Schwarze Königsnatter", "Black Kingsnake"),
    45:  (0, 13379, 1,  "Piccoloflöte des flammenden Feuers", "Piccolo of the Flaming Fire"),
    50:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    55:  (0, 38658, 1,  "Vampirfledermausjunges", "Vampiric Batling"),
    60:  (0, 47241, 15, "15x Emblem des Triumphs", "15x Emblem of Triumph"),
    62:  (0, 8494,  1,  "Hyazinthara", "Hyacinth Macaw"),
    65:  (0, 43154, 1,  "Wappenrock des Argentumkreuzzugs", "Tabard of the Argent Crusade"),
    66:  (2, 168,   1,  "Titel: der Geduldige", "Title: the Patient"),
    70:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    75:  (1, 2000000, 1, "200 Gold", "200 gold"),
    78:  (0, 21540, 1,  "Elunes Laterne", "Elune's Lantern"),
    80:  (0, 49426, 15, "15x Emblem des Frosts", "15x Emblem of Frost"),
    85:  (0, 43157, 1,  "Wappenrock des Kirin Tor", "Tabard of the Kirin Tor"),
    90:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    95:  (1, 5000000, 1, "500 Gold", "500 gold"),
    99:  (2, 175,   1,  "Titel: Königsmörder", "Title: Kingslayer"),
    100: (3, 0, 2, "2x Traumkiste", "2x Dream Chest"),
}

# Zusätzliche Kisten-Zeilen auf dem Abenteuerpfad (slot=1 in der PK)
FREE_CHESTS = { 10: 0, 30: 0, 50: 0, 70: 0, 90: 0 }

EPIC_TRACK = {
    1:   "CLASS",
    4:   (1, 500000,  1,  "50 Gold extra", "50 extra gold"),
    5:   "CLASS",
    8:   (0, 21841,   1,  "Netherstofftasche (16 Plätze)", "Netherweave Bag (16 slots)"),
    10:  "CLASS",
    12:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    15:  "CLASS",
    16:  (0, 45624,   10, "10x Emblem der Eroberung", "10x Emblem of Conquest"),
    20:  (0, 23713,   1,  "Hippogryphjunges", "Hippogryph Hatchling"),
    24:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    28:  (1, 1000000, 1,  "100 Gold extra", "100 extra gold"),
    32:  (0, 47241,   10, "10x Emblem des Triumphs", "10x Emblem of Triumph"),
    36:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    40:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    44:  (0, 900102,  1,  "Wappenrock des Alptraums", "Tabard of the Nightmare"),
    48:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    52:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    56:  (0, 41599,   1,  "Frostgewebetasche (20 Plätze)", "Frostweave Bag (20 slots)"),
    60:  (0, 38628,   1,  "Netherrochenbaby", "Nether Ray Fry"),
    64:  (0, 49426,   10, "10x Emblem des Frosts", "10x Emblem of Frost"),
    68:  (1, 2000000, 1,  "200 Gold extra", "200 extra gold"),
    72:  (1, 3000000, 1, "300 Gold extra", "300 extra gold"),
    76:  (1, 2500000, 1,  "250 Gold extra", "250 extra gold"),
    80:  (0, 49426,   15, "15x Emblem des Frosts", "15x Emblem of Frost"),
    84:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    88:  (1, 5000000, 1, "500 Gold extra", "500 extra gold"),
    92:  (3, 0, 1, "Traumkiste", "Dream Chest"),
    96:  (1, 3000000, 1,  "300 Gold extra", "300 extra gold"),
    100: (3, 0, 2, "2x Traumkiste", "2x Dream Chest"),
}

def free_reward(tier):
    if tier in FREE_SPECIALS:
        return FREE_SPECIALS[tier]
    copper = (tier + 2) * 10000
    g = copper // 10000
    return (1, copper, 1, "%d Gold" % g, "%d gold" % g)

# ---------------------------------------------------------------------------
# Wochenziele (id, type, goal, points, DE, EN)
# type: 0=Kills 1=Elite 2=Bosse 3=Quests 4=Levelups 5=PvP 6=Duelle 7=Rares
# 8=Punkte 9=Entdeckungen 10=Eventzone 11=Kopfgeld 12=Weltboss
# ---------------------------------------------------------------------------
WEEKLY = [
    (1,  0, 150,  150, "Schlachtfest: Besiege 150 Gegner", "Slaughterfest: Slay 150 enemies"),
    (2,  1, 30,   150, "Elitejäger: Besiege 30 Elitegegner", "Elite Hunter: Slay 30 elites"),
    (3,  2, 5,    200, "Bosskiller: Besiege 5 Bosse", "Boss Killer: Slay 5 bosses"),
    (4,  3, 25,   150, "Fleißiger Held: Schließe 25 Quests ab", "Diligent Hero: Complete 25 quests"),
    (5,  4, 3,    150, "Aufsteiger: Steige 3 Stufen auf", "Climber: Gain 3 levels"),
    (6,  5, 10,   200, "Ehrenjagd: Besiege 10 Spieler", "Honor Hunt: Defeat 10 players"),
    (7,  6, 3,    100, "Duellant: Gewinne 3 Duelle", "Duelist: Win 3 duels"),
    (8,  7, 3,    250, "Rarejäger: Besiege 3 seltene Gegner", "Rare Hunter: Slay 3 rare enemies"),
    (9,  8, 500,  150, "Punktesammler: Verdiene 500 Punkte", "Point Collector: Earn 500 points"),
    (10, 0, 300,  300, "Massenschlacht: Besiege 300 Gegner", "Mass Battle: Slay 300 enemies"),
    (11, 1, 60,   300, "Elitetrupp: Besiege 60 Elitegegner", "Elite Squad: Slay 60 elites"),
    (12, 2, 10,   400, "Bossmarathon: Besiege 10 Bosse", "Boss Marathon: Slay 10 bosses"),
    (13, 3, 50,   300, "Questheld: Schließe 50 Quests ab", "Quest Hero: Complete 50 quests"),
    (14, 4, 5,    250, "Powerleveler: Steige 5 Stufen auf", "Power Leveler: Gain 5 levels"),
    (15, 5, 25,   400, "Schlachtenruhm: Besiege 25 Spieler", "Battle Glory: Defeat 25 players"),
    (16, 6, 10,   250, "Duellmeister: Gewinne 10 Duelle", "Duel Master: Win 10 duels"),
    (17, 7, 5,    400, "Legendenjäger: Besiege 5 seltene Gegner", "Legend Hunter: Slay 5 rare enemies"),
    (18, 8, 1000, 300, "Großsammler: Verdiene 1000 Punkte", "Grand Collector: Earn 1000 points"),
    (19, 0, 500,  500, "Wochenpensum: Besiege 500 Gegner", "Weekly Quota: Slay 500 enemies"),
    (20, 3, 75,   500, "Weltenbummler: Schließe 75 Quests ab", "Globetrotter: Complete 75 quests"),
    (21, 9, 2,    200, "Traumwanderer: Entdecke 2 verlorene Orte", "Dream Wanderer: Discover 2 lost places"),
    (22, 9, 5,    400, "Kartograph: Entdecke 5 verlorene Orte", "Cartographer: Discover 5 lost places"),
    (23, 10, 50,  200, "Zonenherrscher: 50 Gegner in der Eventzone", "Zone Ruler: 50 enemies in the event zone"),
    (24, 10, 150, 400, "Eventmarathon: 150 Gegner in der Eventzone", "Event Marathon: 150 enemies in the event zone"),
    (25, 11, 1,   200, "Kopfgeldjäger: Erlege ein Tagesziel", "Bounty Hunter: Claim a daily bounty"),
    (26, 11, 3,   500, "Steckbriefsammler: 3 Kopfgelder diese Woche", "Wanted Poster Collector: 3 bounties this week"),
    (27, 12, 1,   300, "Drachenwache: Besiege einen Saison-Weltboss", "Dragon Watch: Defeat a season world boss"),
    (28, 12, 3,   600, "Alptraumbezwinger: 3 Saison-Weltbosse", "Nightmare Conqueror: 3 season world bosses"),
    (29, 0, 1000, 600, "Schlachtenlegende: Besiege 1000 Gegner", "Battle Legend: Slay 1000 enemies"),
    (30, 3, 100,  600, "Questmarathon: Schließe 100 Quests ab", "Quest Marathon: Complete 100 quests"),
    (31, 1, 100,  400, "Eliteschlächter: Besiege 100 Elitegegner", "Elite Slayer: Slay 100 elites"),
    (32, 2, 20,   500, "Bosstour: Besiege 20 Bosse", "Boss Tour: Slay 20 bosses"),
    (33, 4, 10,   400, "Aufstiegswoche: Steige 10 Stufen auf", "Ascension Week: Gain 10 levels"),
    (34, 5, 50,   500, "Kriegstreiber: Besiege 50 Spieler", "Warmonger: Defeat 50 players"),
    (35, 6, 20,   350, "Duellfürst: Gewinne 20 Duelle", "Duel Lord: Win 20 duels"),
    (36, 7, 10,   600, "Rarelegende: Besiege 10 seltene Gegner", "Rare Legend: Slay 10 rare enemies"),
    (37, 8, 2000, 500, "Punkteflut: Verdiene 2000 Punkte", "Point Flood: Earn 2000 points"),
    (38, 8, 3000, 700, "Punktelawine: Verdiene 3000 Punkte", "Point Avalanche: Earn 3000 points"),
    (39, 0, 750,  550, "Heerscharen: Besiege 750 Gegner", "Legions: Slay 750 enemies"),
    (40, 3, 150,  700, "Questgott: Schließe 150 Quests ab", "Quest God: Complete 150 quests"),
]

# Runen (id, kind 0=Buff/1=Fähigkeit, spell, cost, DE, EN, BeschrDE, BeschrEN, icon)
RUNES = [
    # Dauerbuffs bewusst mild (max ~10% — Userwunsch): Rang-1-Buffs bzw. Prozent-Auren
    (1,  0, 1126,  500000,  "Rune der Wildnis", "Rune of the Wild",
     "Dauerbuff: etwas Rüstung (Mal der Wildnis, Rang 1)", "Permanent: a little armor (Mark of the Wild, rank 1)",
     "Interface\\\\Icons\\\\Spell_Nature_Regeneration"),
    (2,  0, 1243,  500000,  "Rune der Seelenstärke", "Rune of Fortitude",
     "Dauerbuff: etwas Ausdauer (Machtwort: Seelenstärke, Rang 1)", "Permanent: a little stamina (Power Word: Fortitude, rank 1)",
     "Interface\\\\Icons\\\\Spell_Holy_WordFortitude"),
    (3,  0, 1459,  500000,  "Rune der Intelligenz", "Rune of Intellect",
     "Dauerbuff: etwas Intelligenz (Arkane Intelligenz, Rang 1)", "Permanent: a little intellect (Arcane Intellect, rank 1)",
     "Interface\\\\Icons\\\\Spell_Holy_MagicalSentry"),
    (4,  0, 14752, 500000,  "Rune des Willens", "Rune of Spirit",
     "Dauerbuff: etwas Willenskraft (Göttlicher Wille, Rang 1)", "Permanent: a little spirit (Divine Spirit, rank 1)",
     "Interface\\\\Icons\\\\Spell_Holy_DivineSpirit"),
    (5,  0, 20217, 1000000, "Rune der Könige", "Rune of Kings",
     "Dauerbuff: +10% auf alle Werte (Segen der Könige)", "Permanent: +10% all stats (Blessing of Kings)",
     "Interface\\\\Icons\\\\Spell_Magic_MageArmor"),
    (6,  0, 19740, 1000000, "Rune der Macht", "Rune of Might",
     "Dauerbuff: etwas Angriffskraft (Segen der Macht, Rang 1)", "Permanent: a little attack power (Blessing of Might, rank 1)",
     "Interface\\\\Icons\\\\Spell_Holy_FistOfJustice"),
    (7,  0, 19742, 1000000, "Rune der Weisheit", "Rune of Wisdom",
     "Dauerbuff: etwas Manaregeneration (Segen der Weisheit, Rang 1)", "Permanent: a little mana regen (Blessing of Wisdom, rank 1)",
     "Interface\\\\Icons\\\\Spell_Holy_SealOfWisdom"),
    (8,  0, 467,   750000,  "Rune der Dornen", "Rune of Thorns",
     "Dauerbuff: Angreifer erleiden etwas Naturschaden (Dornen, Rang 1)", "Permanent: attackers take a little nature damage (Thorns, rank 1)",
     "Interface\\\\Icons\\\\Spell_Nature_Thorns"),
    (9,  0, 976,   750000,  "Rune des Schattenschutzes", "Rune of Shadow Protection",
     "Dauerbuff: etwas Schattenwiderstand (Rang 1)", "Permanent: a little shadow resistance (rank 1)",
     "Interface\\\\Icons\\\\Spell_Shadow_AntiShadow"),
    (10, 0, 20911, 1500000, "Rune des Refugiums", "Rune of Sanctuary",
     "Dauerbuff: -3% erlittener Schaden, +10% Stärke & Ausdauer (Segen des Refugiums)", "Permanent: -3% damage taken, +10% strength & stamina (Blessing of Sanctuary)",
     "Interface\\\\Icons\\\\Spell_Holy_SealOfProtection"),
    (11, 0, 19506, 1500000, "Rune des Scharfschützen", "Rune of Trueshot",
     "Dauerbuff: +10% Angriffskraft (Zielsicherheitsaura)", "Permanent: +10% attack power (Trueshot Aura)",
     "Interface\\\\Icons\\\\Ability_TrueShot"),
    (12, 0, 24932, 1500000, "Rune des Rudels", "Rune of the Pack",
     "Dauerbuff: +5% kritische Trefferchance (Anführer des Rudels)", "Permanent: +5% critical strike chance (Leader of the Pack)",
     "Interface\\\\Icons\\\\Ability_Mount_JungleTiger"),
    (13, 1, 355,   1000000, "Rune des Spotts", "Rune of Taunt",
     "Fähigkeit: Spott — tanke mit JEDER Klasse!", "Ability: Taunt — tank on ANY class!",
     "Interface\\\\Icons\\\\Spell_Nature_Reincarnation"),
    (14, 1, 25780, 1000000, "Rune des rechtschaffenen Zorns", "Rune of Righteous Fury",
     "Fähigkeit: +Bedrohung (an-/abschaltbar)", "Ability: +threat (toggle on/off)",
     "Interface\\\\Icons\\\\Spell_Holy_SealOfFury"),
    (15, 1, 6346,  1000000, "Rune der Furchtabwehr", "Rune of Fear Ward",
     "Fähigkeit: schützt ein Ziel vor dem nächsten Furchteffekt", "Ability: wards a target against the next fear",
     "Interface\\\\Icons\\\\Spell_Holy_ExcorcismInfusion"),
    (16, 1, 1953,  1500000, "Rune des Blinzelns", "Rune of Blink",
     "Fähigkeit: Blinzeln — teleportiert dich 20 Meter nach vorn", "Ability: Blink — teleport 20 yards forward",
     "Interface\\\\Icons\\\\Spell_Arcane_Blink"),
    (17, 1, 11305, 1500000, "Rune des Sprints", "Rune of Sprint",
     "Fähigkeit: Sprint — kurzzeitig +70% Lauftempo", "Ability: Sprint — burst of +70% run speed",
     "Interface\\\\Icons\\\\Ability_Rogue_Sprint"),
    (18, 1, 1787,  2000000, "Rune des Schleichens", "Rune of Stealth",
     "Fähigkeit: Schleichen wie ein Schurke", "Ability: Stealth like a rogue",
     "Interface\\\\Icons\\\\Ability_Stealth"),
    (19, 1, 556,   1000000, "Rune des astralen Rückrufs", "Rune of Astral Recall",
     "Fähigkeit: zweiter Ruhestein (15 min Abklingzeit)", "Ability: second hearthstone (15 min cooldown)",
     "Interface\\\\Icons\\\\Spell_Nature_AstralRecal"),
    (20, 1, 546,   750000,  "Rune des Wasserwandelns", "Rune of Water Walking",
     "Fähigkeit: über Wasser laufen", "Ability: walk on water",
     "Interface\\\\Icons\\\\Spell_Frost_WindWalkOn"),
    (21, 1, 5697,  750000,  "Rune der Unterwasseratmung", "Rune of Water Breathing",
     "Fähigkeit: unbegrenzt unter Wasser atmen", "Ability: breathe underwater indefinitely",
     "Interface\\\\Icons\\\\Spell_Shadow_DemonBreath"),
    (22, 1, 48788, 2000000, "Rune der Handauflegung", "Rune of Lay on Hands",
     "Fähigkeit: Not-Vollheilung (lange Abklingzeit)", "Ability: emergency full heal (long cooldown)",
     "Interface\\\\Icons\\\\Spell_Holy_LayOnHands"),
    (23, 1, 6197,  750000,  "Rune des Adlerauges", "Rune of Eagle Eye",
     "Fähigkeit: Fernsicht — späh entfernte Orte aus", "Ability: far sight — scout distant places",
     "Interface\\\\Icons\\\\Ability_Hunter_EagleEye"),
    (24, 1, 2825,  2500000, "Rune des Kampfrauschs", "Rune of Bloodlust",
     "Fähigkeit: Kampfrausch — +30% Tempo für die Gruppe!", "Ability: Bloodlust — +30% haste for the party!",
     "Interface\\\\Icons\\\\Spell_Nature_BloodLust"),
]

WORLDBOSSES = [
    (1, 14890, 0,  -10432.0, -392.0,  43.0, 0.0, "Taerar",   "Düsterwald (Zwielichthain)", "Duskwood (Twilight Grove)"),
    (2, 14888, 0,  815.0,    -510.0,  180.0, 0.0, "Lethon",   "Hinterland (Seradane)", "The Hinterlands (Seradane)"),
    (3, 14887, 1,  -2882.0,  1930.0,  60.0,  0.0, "Ysondre",  "Feralas (Traumzweig)", "Feralas (Dream Bough)"),
    (4, 14889, 1,  3050.0,   -3460.0, 140.0, 0.0, "Emeriss",  "Eschental (Schattenast)", "Ashenvale (Bough Shadow)"),
    (5, 12397, 0,  -11800.0, -3190.0, 6.0,   0.0, "Lord Kazzak", "Verwüstete Lande", "Blasted Lands"),
    (6, 6109,  1,  2550.0,   -5670.0, 100.0, 0.0, "Azuregos", "Azshara", "Azshara"),
]

ZONES = [
    (1,  33,  "Schlingendorntal (Blutmond!)", "Stranglethorn Vale (Blood Moon!)"),
    (2,  331, "Eschental (Schlacht um Eschental!)", "Ashenvale (Battle for Ashenvale!)"),
    (3,  40,  "Westfall", "Westfall"),
    (4,  267, "Vorgebirge von Hügelsbrunn", "Hillsbrad Foothills"),
    (5,  490, "Krater von Un'Goro", "Un'Goro Crater"),
    (6,  618, "Winterquell", "Winterspring"),
    (7,  3,   "Ödland", "Badlands"),
    (8,  47,  "Hinterland", "The Hinterlands"),
    (9,  400, "Tausend Nadeln", "Thousand Needles"),
    (10, 139, "Östliche Pestländer", "Eastern Plaguelands"),
    (11, 357, "Feralas", "Feralas"),
    (12, 65,  "Drachenöde", "Dragonblight"),
]

BOUNTIES = [
    (1, 448,  150, "Hogger", "Hogger", "Elwynn", "Elwynn Forest"),
    (2, 522,  150, "Mor'Ladim", "Mor'Ladim", "Düsterwald", "Duskwood"),
    (3, 5828, 150, "Humar der Stolzherr", "Humar the Pridelord", "Brachland", "The Barrens"),
    (4, 5827, 150, "Der Rechen", "The Rake", "Mulgore", "Mulgore"),
    (5, 6584, 200, "König Mosh", "King Mosh", "Un'Goro", "Un'Goro Crater"),
    (6, 3581, 150, "Kanalkrokilisk", "Sewer Beast", "Sturmwind", "Stormwind"),
    (7, 7846, 250, "Teremus der Verschlinger", "Teremus the Devourer", "Verwüstete Lande", "Blasted Lands"),
    (8, 14445,200, "Riesengrizzly", "Giant Grizzly", "Dun Morogh", "Dun Morogh"),
]

DUNGEONS = [
    (1,  389, 300, "Der Flammenschlund", "Ragefire Chasm"),
    (2,  36,  300, "Die Todesminen", "The Deadmines"),
    (3,  43,  300, "Die Höhlen des Wehklagens", "Wailing Caverns"),
    (4,  33,  300, "Burg Schattenfang", "Shadowfang Keep"),
    (5,  48,  300, "Tiefschwarze Grotte", "Blackfathom Deeps"),
    (6,  90,  300, "Gnomeregan", "Gnomeregan"),
    (7,  189, 300, "Das Scharlachrote Kloster", "Scarlet Monastery"),
    (8,  209, 300, "Zul'Farrak", "Zul'Farrak"),
    (9,  109, 350, "Der Versunkene Tempel", "The Temple of Atal'Hakkar"),
    (10, 230, 350, "Schwarzfelstiefen", "Blackrock Depths"),
    (11, 329, 400, "Stratholme", "Stratholme"),
    (12, 289, 400, "Scholomance", "Scholomance"),
]

DISCOVERIES = [
    (1,  41,   "Gebirgspass der Totenwinde", "Deadwind Pass"),
    (2,  618,  "Winterquell", "Winterspring"),
    (3,  1377, "Silithus", "Silithus"),
    (4,  490,  "Krater von Un'Goro", "Un'Goro Crater"),
    (5,  361,  "Teufelswald", "Felwood"),
    (6,  16,   "Azshara", "Azshara"),
    (7,  493,  "Moonglade", "Moonglade"),
    (8,  47,   "Hinterland", "The Hinterlands"),
    (9,  357,  "Feralas", "Feralas"),
    (10, 4,    "Verwüstete Lande", "Blasted Lands"),
    (11, 51,   "Sengende Schlucht", "Searing Gorge"),
    (12, 46,   "Brennende Steppe", "Burning Steppes"),
    (13, 3,    "Ödland", "Badlands"),
    (14, 8,    "Sümpfe des Elends", "Swamp of Sorrows"),
    (15, 139,  "Östliche Pestländer", "Eastern Plaguelands"),
    (16, 28,   "Westliche Pestländer", "Western Plaguelands"),
    (17, 440,  "Tanaris", "Tanaris"),
    (18, 400,  "Tausend Nadeln", "Thousand Needles"),
]
DISCOVERY_POINTS = 25

ACHIEVEMENTS = [
    (1,  7,  10,  100, "Der Anfang: Erreiche Stufe 10", "The Beginning: Reach tier 10"),
    (2,  7,  25,  200, "Viertelmeister: Erreiche Stufe 25", "Quarter Master: Reach tier 25"),
    (3,  7,  50,  300, "Halbzeitheld: Erreiche Stufe 50", "Halftime Hero: Reach tier 50"),
    (4,  7,  75,  400, "Dranbleiber: Erreiche Stufe 75", "Persister: Reach tier 75"),
    (5,  7,  100, 500, "Vollender: Erreiche Stufe 100", "Completionist: Reach tier 100"),
    (6,  0,  1,   150, "Alptraumtaufe: Besiege 1 Saison-Weltboss", "Nightmare Baptism: Defeat 1 season world boss"),
    (7,  0,  10,  400, "Drachenschreck: Besiege 10 Saison-Weltbosse", "Dragon Terror: Defeat 10 season world bosses"),
    (8,  0,  25,  800, "Weltenretter: Besiege 25 Saison-Weltbosse", "World Savior: Defeat 25 season world bosses"),
    (9,  1,  1,   100, "Steckbrief: Erlege 1 Kopfgeld", "Wanted: Claim 1 bounty"),
    (10, 1,  10,  400, "Kopfgeldkönig: Erlege 10 Kopfgelder", "Bounty King: Claim 10 bounties"),
    (11, 2,  3,   100, "Runenlehrling: Graviere 3 Runen", "Rune Apprentice: Engrave 3 runes"),
    (12, 2,  10,  300, "Runenmeister: Graviere 10 Runen", "Rune Master: Engrave 10 runes"),
    (13, 3,  10,  200, "Wochenheld: Schließe 10 Wochenziele ab", "Weekly Hero: Complete 10 weekly goals"),
    (14, 3,  50,  600, "Wochenlegende: Schließe 50 Wochenziele ab", "Weekly Legend: Complete 50 weekly goals"),
    (15, 4,  25,  200, "Duellkönig: Gewinne 25 Duelle", "Duel King: Win 25 duels"),
    (16, 5,  25,  300, "Raritätenjäger: Besiege 25 seltene Gegner", "Rarity Hunter: Slay 25 rare enemies"),
    (17, 6,  5,   300, "Dungeonwanderer: 5x Dungeon der Woche", "Dungeon Wanderer: 5x dungeon of the week"),
    (18, 8,  1,   500, "Wiedergänger: Erreiche Prestige 1", "Revenant: Reach prestige 1"),
    (19, 9,  7,   200, "Stammgast: 7 Login-Tage in Folge", "Regular: 7 login days in a row"),
    (20, 10, 18,  500, "Entdecker Azeroths: Finde alle verlorenen Orte", "Explorer of Azeroth: Find all lost places"),
    (21, 12, 10,  200, "Lieferant: Erfülle 10 Versorgungsaufträge", "Supplier: Complete 10 supply runs"),
    (22, 12, 50,  600, "Handelsprinz: Erfülle 50 Versorgungsaufträge", "Trade Prince: Complete 50 supply runs"),
    (23, 13, 10,  200, "Kistenknacker: Öffne 10 Traumkisten", "Chest Cracker: Open 10 dream chests"),
    (24, 13, 50,  600, "Traumsammler: Öffne 50 Traumkisten", "Dream Hoarder: Open 50 dream chests"),
]

# Versorgungsaufträge (SoD "Waylaid Supplies"): täglich rotierendes Handelsgut
# abliefern -> Punkte + Gold. (id, item, Menge, Punkte, Gold in Kupfer)
SUPPLIES = [
    (1,  2589,  20, 150, 5000),   # Leinenstoff
    (2,  2592,  20, 150, 8000),   # Wollstoff
    (3,  4306,  20, 150, 12000),  # Seide
    (4,  4338,  20, 150, 16000),  # Magiestoff
    (5,  14047, 20, 150, 25000),  # Runenstoff
    (6,  21877, 20, 150, 35000),  # Netherstoff
    (7,  33470, 20, 150, 50000),  # Froststoff
    (8,  2770,  20, 150, 5000),   # Kupfererz
    (9,  2771,  20, 150, 8000),   # Zinnerz
    (10, 2772,  20, 150, 12000),  # Eisenerz
    (11, 3858,  20, 150, 20000),  # Mithrilerz
    (12, 10620, 20, 150, 30000),  # Thoriumerz
    (13, 23424, 20, 150, 40000),  # Teufelseisenerz
    (14, 36909, 20, 150, 50000),  # Kobalterz
    (15, 2318,  20, 150, 5000),   # Leichtes Leder
    (16, 2319,  20, 150, 8000),   # Mittleres Leder
    (17, 4234,  20, 150, 12000),  # Schweres Leder
    (18, 4304,  20, 150, 20000),  # Dickes Leder
    (19, 8170,  20, 150, 30000),  # Robustes Leder
    (20, 21887, 20, 150, 40000),  # Knotenhautleder
    (21, 33568, 20, 150, 50000),  # Boreanisches Leder
]

TELEPORTS = [
    (1,  "Sturmwind", "Stormwind",         0,   -8833.4, 628.6,    94.0,  1.06),
    (2,  "Eisenschmiede", "Ironforge",     0,   -4981.3, -881.5,   501.7, 5.40),
    (3,  "Darnassus", "Darnassus",         1,   9947.5,  2482.7,   1316.2,0.00),
    (4,  "Die Exodar", "The Exodar",       530, -3965.7, -11653.6, -138.8,0.85),
    (5,  "Orgrimmar", "Orgrimmar",         1,   1601.1,  -4378.7,  10.0,  2.14),
    (6,  "Unterstadt", "Undercity",        0,   1633.8,  240.2,    -43.1, 6.26),
    (7,  "Donnerfels", "Thunder Bluff",    1,   -1277.4, 124.8,    131.3, 5.22),
    (8,  "Silbermond", "Silvermoon",       530, 9738.3,  -7454.2,  13.6,  0.04),
    (9,  "Shattrath", "Shattrath",         530, -1887.6, 5359.1,   -12.4, 4.40),
    (10, "Dalaran", "Dalaran",             571, 5809.6,  448.9,    658.8, 5.26),
    (11, "Gadgetzan", "Gadgetzan",         1,   -7176.6, -3785.3,  8.4,   5.80),
    (12, "Beutebucht", "Booty Bay",        0,   -14297.2,518.0,    8.8,   3.90),
]

# Preisfaktor für den Shop: x1.5 der Basispreise — spürbar, aber im Verhältnis
# zu Pass-Gold, Levelkisten und Lieferaufträgen fair verdienbar.
def shop_price(p):
    return p * 3 // 2

# Shop-Kategorien: (DE, EN, Anzahl aufeinanderfolgender Slots) — Summe muss
# der Gesamtzahl der Shop-Slots entsprechen (Box + SHOP-Einträge)!
SHOP_CATS = [
    ("Traumkiste & Spaß", "Dream Chest & Fun", 7),
    ("Tränke & Verbände", "Potions & Bandages", 30),
    ("Essen & Getränke", "Food & Drink", 18),
    ("Elixiere & Buffs", "Elixirs & Buffs", 27),
    ("Taschen & Munition", "Bags & Ammo", 12),
    ("Reagenzien & Berufe", "Reagents & Professions", 25),
]

# Mystery-Boxen im Shop (öffnen direkt eine Zufallskiste): (Kistenstufe, Preis)
SHOP_BOXES = [
    (0, 1000000),  # Traumkiste — 100 Gold (Qualität wird beim Öffnen ausgewürfelt)
]

# Angelaufträge (täglich rotierender Fisch, Fang zählt automatisch beim Looten):
# (id, item, Menge, Punkte, Gold in Kupfer)
FISH = [
    (1,  6291,  10, 150, 100000),   # Roher glänzender Kleinfisch
    (2,  6289,  10, 150, 100000),   # Roher Grossmaulschnapper
    (3,  6308,  10, 150, 100000),   # Roher Borstenwelts
    (4,  6358,  10, 150, 100000),  # Öliger Schwarzmaul
    (5,  6359,  10, 150, 100000),  # Feuerflossenschnapper
    (6,  4603,  10, 150, 100000),  # Roher gefleckter Gelbschwanz
    (7,  6362,  10, 150, 100000),  # Roher Felsenschuppenkabeljau
    (8,  13754, 10, 150, 100000),  # Roher glänzender Machtfisch
    (9,  27422, 10, 150, 100000),  # Stachelkiemenforelle
    (10, 41800, 10, 150, 100000),  # Tiefseeungeheuerbauch
]

# Saisonhändlerin: 118 sinnvolle Items (item, Kaufmenge, Basispreis in Kupfer).
# Preise stufengerecht (x SHOP_PRICE_MULT), Mengen praktisch.
SHOP = [
    # Spaß-Klassiker
    (8529, 3, 25000), (17202, 10, 500), (18662, 1, 10000), (4365, 5, 5000),
    (4390, 5, 8000), (10646, 3, 80000),
    # Heiltränke (klein bis Runenverziert)
    (118, 5, 500), (858, 5, 2000), (929, 5, 5000), (1710, 5, 12000),
    (3928, 5, 30000), (13446, 5, 75000), (22829, 5, 150000), (33447, 5, 250000),
    # Manatränke
    (2455, 5, 500), (3385, 5, 2000), (3827, 5, 5000), (6149, 5, 12000),
    (13443, 5, 30000), (13444, 5, 75000), (22832, 5, 150000), (33448, 5, 250000),
    # Verbände (Leinen bis Froststoff)
    (1251, 5, 250), (2581, 5, 500), (3530, 5, 1000), (3531, 5, 2000),
    (6450, 5, 4000), (6451, 5, 7000), (8544, 5, 12000), (8545, 5, 20000),
    (14529, 5, 35000), (14530, 5, 50000), (21990, 5, 80000), (21991, 5, 120000),
    (34721, 5, 180000), (34722, 5, 250000),
    # Essen
    (117, 5, 100), (4540, 5, 100), (2287, 5, 300), (4541, 5, 300),
    (3770, 5, 800), (4542, 5, 800), (3771, 5, 2000), (4544, 5, 2000),
    (4599, 5, 5000), (8952, 5, 10000), (4536, 5, 150),
    # Getränke
    (159, 5, 100), (1179, 5, 300), (1205, 5, 800), (1708, 5, 2000),
    (8766, 5, 5000), (28399, 5, 10000), (33445, 5, 20000),
    # Elixiere & Kampf-Buffs
    (2454, 3, 1500), (3390, 3, 2500), (2457, 3, 2000), (5997, 3, 2500),
    (6373, 3, 5000), (3825, 3, 8000), (8949, 3, 10000), (9187, 3, 20000),
    (9206, 3, 40000), (13452, 3, 60000), (13454, 3, 60000), (9088, 3, 50000),
    (9036, 3, 15000),
    # Utility-Tränke
    (2459, 3, 20000), (5634, 3, 50000), (5631, 3, 10000), (5633, 3, 30000),
    (6049, 3, 25000), (6048, 3, 25000), (6050, 3, 25000), (4623, 3, 15000),
    (9172, 3, 60000), (3387, 1, 150000),
    # Schriftrollen
    (954, 5, 5000), (955, 5, 5000), (1180, 5, 5000), (3012, 5, 5000),
    # Taschen
    (4496, 1, 2000), (4498, 1, 6000), (4497, 1, 15000), (4499, 1, 35000),
    (21841, 1, 150000), (41599, 1, 500000),
    # Munition (200er-Pack)
    (2512, 200, 500), (3030, 200, 5000), (11285, 200, 20000),
    (2516, 200, 500), (3033, 200, 5000), (11284, 200, 20000),
    # Klassen-Reagenzien
    (17056, 10, 2000), (17057, 10, 2000), (17058, 10, 2000), (17021, 10, 5000),
    (17026, 10, 10000), (17029, 10, 15000), (17030, 3, 20000), (17031, 10, 10000),
    (17032, 10, 20000), (16583, 3, 15000), (5565, 3, 10000), (21177, 10, 15000),
    (17033, 3, 20000),
    # Berufe & Angeln
    (6529, 10, 1000), (6530, 10, 2500), (2320, 10, 500), (2321, 10, 1500),
    (4291, 10, 4000), (8343, 10, 8000), (14341, 10, 15000), (2324, 5, 1000),
    (2325, 5, 2500), (6260, 5, 2500), (2604, 5, 2500), (4340, 5, 2500),
]

# Wochen-Mutatoren (id, kind, valuePercent, DE, EN)
# kind: 0=Quest x2, 1=Elite x2, 2=Rare x2, 3=PvP/Duell x2, 4=XP-Bonus,
#       5=Kistenchance x2, 6=Wochenziel-Punkte x2, 7=Entdeckungen x2
MUTATORS = [
    (1, 0, 200, "Woche der Gelehrten: Questpunkte x2", "Week of Scholars: quest points x2"),
    (2, 1, 200, "Woche der Riesen: Elitepunkte x2", "Week of Giants: elite points x2"),
    (3, 2, 200, "Woche der Jäger: Rare-Punkte x2", "Week of Hunters: rare points x2"),
    (4, 3, 200, "Woche des Blutes: PvP- und Duellpunkte x2", "Week of Blood: PvP and duel points x2"),
    (5, 4, 125, "Woche der Weisheit: +25% Erfahrung", "Week of Wisdom: +25% experience"),
    (6, 5, 200, "Kistenwoche: doppelte Kistenchance", "Chest Week: double chest chance"),
    (7, 6, 200, "Woche der Pflicht: Wochenziel-Punkte x2", "Week of Duty: weekly goal points x2"),
    (8, 7, 200, "Woche der Wanderer: Entdeckungspunkte x2", "Week of Wanderers: discovery points x2"),
]

# ===========================================================================
#  SQL-Helfer
# ===========================================================================

def esc(s):
    return s.replace("'", "''")

def table_sql(name, columns, rows, comment):
    out = ["-- mod-battlepass v4: %s" % comment,
           "DROP TABLE IF EXISTS `%s`;" % name,
           "CREATE TABLE `%s` (" % name]
    out.append(",\n".join("  " + c for c in columns[0]))
    out.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
    out.append("INSERT INTO `%s` (%s) VALUES" % (name, ",".join("`%s`" % c for c in columns[1])))
    out.append(",\n".join(rows) + ";")
    return "\n".join(out) + "\n"

def sql_rewards():
    rows = []
    # Stufe 0 = Willkommenspaket (automatisch bei der ersten Anmeldung)
    for slot, (t, i, c, n, ne) in enumerate(WELCOME):
        rows.append("(%d,0,0,0,%d,%d,%d,%d,'%s','%s')" % (SEASON, slot, t, i, c, esc(n), esc(ne)))
    for tier in range(1, MAX_TIER + 1):
        t, i, c, n, ne = free_reward(tier)
        rows.append("(%d,%d,0,0,0,%d,%d,%d,'%s','%s')" % (SEASON, tier, t, i, c, esc(n), esc(ne)))
    for tier, chest in sorted(FREE_CHESTS.items()):
        de, en = CHEST_NAMES[chest]
        rows.append("(%d,%d,0,0,1,3,%d,1,'%s','%s')" % (SEASON, tier, chest, esc(de), esc(en)))
    for tier in sorted(EPIC_TRACK):
        r = EPIC_TRACK[tier]
        if r == "CLASS":
            slot = [s for s, tt in SET_TIERS.items() if tt == tier][0]
            for cid, (token, mask, cname) in CLASSES.items():
                piece = [p for p in CLASS_SETS[cid] if p[0] == slot][0]
                rows.append("(%d,%d,1,%d,0,0,%d,1,'%s','%s')" % (SEASON, tier, mask, set_entry(cid, slot),
                            esc("%s (%s)" % (piece[3], cname)), esc(piece[4])))
        else:
            t, i, c, n, ne = r
            rows.append("(%d,%d,1,0,0,%d,%d,%d,'%s','%s')" % (SEASON, tier, t, i, c, esc(n), esc(ne)))
    cols = (["`season` INT UNSIGNED NOT NULL DEFAULT 1",
             "`tier` SMALLINT UNSIGNED NOT NULL",
             "`track` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0=Abenteuer,1=Helden (beide frei)'",
             "`classmask` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0=alle'",
             "`slot` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'mehrere Zeilen pro Stufe'",
             "`type` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0=ITEM,1=GOLD,2=TITLE,3=KISTE'",
             "`id` INT UNSIGNED NOT NULL DEFAULT 0",
             "`count` INT UNSIGNED NOT NULL DEFAULT 1",
             "`name` VARCHAR(120) NOT NULL DEFAULT ''",
             "`name_en` VARCHAR(120) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`season`,`tier`,`track`,`classmask`,`slot`)"],
            ["season", "tier", "track", "classmask", "slot", "type", "id", "count", "name", "name_en"])
    return table_sql("battlepass_rewards", cols, rows,
                     "Belohnungen Saison %d (beide Pfade kostenlos, zweisprachig)" % SEASON), len(rows)

def clone_block(entry, source, name_en, name_de, quality, allowable_class, desc, no_reqs=False, no_prof=False):
    b = ["DROP TEMPORARY TABLE IF EXISTS `bp_tmp`;",
         "CREATE TEMPORARY TABLE `bp_tmp` AS SELECT * FROM `item_template` WHERE `entry`=%d;" % source]
    extra = ""
    if no_reqs:
        extra = ", `RequiredSkill`=0, `RequiredSkillRank`=0, `requiredspell`=0, `RequiredReputationFaction`=0, `RequiredReputationRank`=0"
    b.append("UPDATE `bp_tmp` SET `entry`=%d, `name`='%s', `Quality`=%d, `AllowableClass`=%d, "
             "`RequiredLevel`=1, `BuyPrice`=0, `SellPrice`=0, `description`='%s'%s;"
             % (entry, esc(name_en), quality, allowable_class, esc(desc), extra))
    if no_prof:
        # Keine Rüstungs-/Waffenkenntnis nötig: Rüstung -> Verschiedenes (0),
        # Nahkampfwaffen -> Verschiedenes (14). Schilde (Blocken) und
        # Distanzwaffen (Autoschuss) behalten ihre Subclass.
        b.append("UPDATE `bp_tmp` SET `subclass` = CASE"
                 " WHEN `class`=4 AND `subclass`<>6 THEN 0"
                 " WHEN `class`=2 AND `InventoryType` IN (13,17,21,22) THEN 14"
                 " ELSE `subclass` END,"
                 " `RequiredSkill`=0, `RequiredSkillRank`=0;")
    b.append("INSERT INTO `item_template` SELECT * FROM `bp_tmp`;")
    b.append("INSERT INTO `item_template_locale` (`ID`,`locale`,`Name`,`Description`) VALUES (%d,'deDE','%s','%s');"
             % (entry, esc(name_de), esc(desc)))
    return b

def sql_items():
    out = ["-- mod-battlepass v4: Custom-Items (Basisname EN, deutsche Namen via item_template_locale)",
           "DELETE FROM `item_template` WHERE `entry` BETWEEN 900001 AND 900199;",
           "DELETE FROM `item_template_locale` WHERE `ID` BETWEEN 900001 AND 900199;"]
    n = 0
    for cid in sorted(CLASS_SETS):
        token, mask, cname = CLASSES[cid]
        out.append("")
        out.append("-- ---- Klassenset %s ----" % cname)
        for slot, slotname, source, name_de, name_en in CLASS_SETS[cid]:
            desc = "Battle Pass Saison %d - Klassenset %s (%s), levelt bis 80 mit" % (SEASON, cname, slotname)
            out.extend(clone_block(set_entry(cid, slot), source, name_en, name_de, 4, mask, desc, no_prof=True))
            n += 1
    out.append("")
    out.append("-- ---- Saison-Sonderitems ----")
    for entry, source, name_de, name_en, desc in SPECIAL_ITEMS:
        out.extend(clone_block(entry, source, name_en, name_de, 4, 32767, desc, no_reqs=True))
        n += 1
    out.append("")
    out.append("-- ---- Mount-Klone ohne Anforderungen ----")
    for source, (entry, name_de, name_en) in sorted(MOUNT_CLONES.items(), key=lambda kv: kv[1][0]):
        desc = "Battle Pass Saison %d - Saisonversion ohne Anforderungen" % SEASON
        out.extend(clone_block(entry, source, name_en, name_de, 4, 32767, desc, no_reqs=True))
        n += 1
    out.append("DROP TEMPORARY TABLE IF EXISTS `bp_tmp`;")
    out.append("")
    out.append("-- Kontrolle (%d erwartet): SELECT COUNT(*) FROM item_template WHERE entry BETWEEN 900001 AND 900199;" % n)
    return "\n".join(out) + "\n", n

def sql_chest_loot():
    out = ["-- mod-battlepass v5: kuratierter Zufallskisten-Beutepool (100 Einträge).",
           "-- kind: 0=Item, 1=Gold (id=Kupfer), 2=Verlorene Rune (lehrt zufällige Runen-Fähigkeit).",
           "-- weight gilt innerhalb der Rarität je Kiste; battlepass_chest_rarity = Promille-Chancen.",
           "DROP TABLE IF EXISTS `battlepass_chest_loot`;",
           "CREATE TABLE `battlepass_chest_loot` (",
           "  `chest` TINYINT UNSIGNED NOT NULL,",
           "  `rarity` TINYINT UNSIGNED NOT NULL,",
           "  `kind` TINYINT UNSIGNED NOT NULL DEFAULT 0,",
           "  `id` INT UNSIGNED NOT NULL DEFAULT 0,",
           "  `count` INT UNSIGNED NOT NULL DEFAULT 1,",
           "  `weight` INT UNSIGNED NOT NULL DEFAULT 10,",
           "  `name` VARCHAR(120) NOT NULL DEFAULT '',",
           "  `name_en` VARCHAR(120) NOT NULL DEFAULT '',",
           "  PRIMARY KEY (`chest`,`rarity`,`kind`,`id`)",
           ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;",
           "INSERT INTO `battlepass_chest_loot` (`chest`,`rarity`,`kind`,`id`,`count`,`weight`,`name`,`name_en`) VALUES"]
    rows = []
    for rar, kind, iid, cnt, de, en, ws in CHEST_LOOT:
        for chest in (1, 2, 3):
            w = ws[chest - 1]
            if w:
                rows.append("(%d,%d,%d,%d,%d,%d,'%s','%s')" % (chest, rar, kind, iid, cnt, w, esc(de), esc(en)))
    out.append(",\n".join(rows) + ";")
    out += ["",
            "DROP TABLE IF EXISTS `battlepass_chest_rarity`;",
            "CREATE TABLE `battlepass_chest_rarity` (",
            "  `chest` TINYINT UNSIGNED NOT NULL,",
            "  `rarity` TINYINT UNSIGNED NOT NULL,",
            "  `chance` INT UNSIGNED NOT NULL COMMENT 'Promille',",
            "  PRIMARY KEY (`chest`,`rarity`)",
            ") ENGINE=InnoDB;",
            "INSERT INTO `battlepass_chest_rarity` (`chest`,`rarity`,`chance`) VALUES"]
    rrows = []
    for chest, chances in sorted(CHEST_RARITY.items()):
        for rar, ch in enumerate(chances, 1):
            rrows.append("(%d,%d,%d)" % (chest, rar, ch))
    out.append(",\n".join(rrows) + ";")
    return "\n".join(out) + "\n"

def sql_weekly():
    cols = (["`id` INT UNSIGNED NOT NULL", "`type` TINYINT UNSIGNED NOT NULL DEFAULT 0",
             "`goal` INT UNSIGNED NOT NULL DEFAULT 1", "`points` INT UNSIGNED NOT NULL DEFAULT 100",
             "`name` VARCHAR(120) NOT NULL DEFAULT ''", "`name_en` VARCHAR(120) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`id`)"],
            ["id", "type", "goal", "points", "name", "name_en"])
    rows = ["(%d,%d,%d,%d,'%s','%s')" % (i, t, g, p, esc(n), esc(ne)) for i, t, g, p, n, ne in WEEKLY]
    return table_sql("battlepass_weekly", cols, rows, "40 Wochenziel-Definitionen (zweisprachig)")

def sql_runes():
    cols = (["`id` INT UNSIGNED NOT NULL", "`classmask` INT UNSIGNED NOT NULL DEFAULT 0",
             "`kind` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0=Aura,1=Fähigkeit'",
             "`spell` INT UNSIGNED NOT NULL", "`cost` INT UNSIGNED NOT NULL DEFAULT 0",
             "`name` VARCHAR(120) NOT NULL DEFAULT ''", "`name_en` VARCHAR(120) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`id`)"],
            ["id", "classmask", "kind", "spell", "cost", "name", "name_en"])
    rows = ["(%d,0,%d,%d,%d,'%s','%s')" % (i, k, s, c, esc(n), esc(ne)) for i, k, s, c, n, ne, _, _, _ in RUNES]
    return table_sql("battlepass_runes", cols, rows, "24 Runen (12 Dauerbuffs + 12 neue Fähigkeiten)")

def sql_worldboss():
    cols = (["`id` INT UNSIGNED NOT NULL", "`entry` INT UNSIGNED NOT NULL",
             "`map` INT UNSIGNED NOT NULL DEFAULT 0",
             "`x` FLOAT NOT NULL", "`y` FLOAT NOT NULL", "`z` FLOAT NOT NULL",
             "`o` FLOAT NOT NULL DEFAULT 0",
             "`name` VARCHAR(60) NOT NULL DEFAULT ''",
             "`zone` VARCHAR(80) NOT NULL DEFAULT ''", "`zone_en` VARCHAR(80) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`id`)"],
            ["id", "entry", "map", "x", "y", "z", "o", "name", "zone", "zone_en"])
    rows = ["(%d,%d,%d,%.1f,%.1f,%.1f,%.1f,'%s','%s','%s')" % (i, e, m, x, y, z, o, esc(n), esc(zn), esc(zne))
            for i, e, m, x, y, z, o, n, zn, zne in WORLDBOSSES]
    return table_sql("battlepass_worldboss", cols, rows, "Weltboss-Rotation (Koordinaten per .gps anpassbar)")

def sql_zones():
    cols = (["`id` INT UNSIGNED NOT NULL", "`zone` INT UNSIGNED NOT NULL",
             "`name` VARCHAR(80) NOT NULL DEFAULT ''", "`name_en` VARCHAR(80) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`id`)"],
            ["id", "zone", "name", "name_en"])
    rows = ["(%d,%d,'%s','%s')" % (i, z, esc(n), esc(ne)) for i, z, n, ne in ZONES]
    return table_sql("battlepass_zones", cols, rows, "Zonen-Events")

def sql_bounty():
    cols = (["`id` INT UNSIGNED NOT NULL", "`entry` INT UNSIGNED NOT NULL",
             "`points` INT UNSIGNED NOT NULL DEFAULT 150",
             "`name` VARCHAR(80) NOT NULL DEFAULT ''", "`name_en` VARCHAR(80) NOT NULL DEFAULT ''",
             "`zone` VARCHAR(60) NOT NULL DEFAULT ''", "`zone_en` VARCHAR(60) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`id`)"],
            ["id", "entry", "points", "name", "name_en", "zone", "zone_en"])
    rows = ["(%d,%d,%d,'%s','%s','%s','%s')" % (i, e, p, esc(n), esc(ne), esc(z), esc(ze))
            for i, e, p, n, ne, z, ze in BOUNTIES]
    return table_sql("battlepass_bounty", cols, rows, "Kopfgeld des Tages")

def sql_dungeons():
    cols = (["`id` INT UNSIGNED NOT NULL", "`map` INT UNSIGNED NOT NULL",
             "`points` INT UNSIGNED NOT NULL DEFAULT 300",
             "`name` VARCHAR(80) NOT NULL DEFAULT ''", "`name_en` VARCHAR(80) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`id`)"],
            ["id", "map", "points", "name", "name_en"])
    rows = ["(%d,%d,%d,'%s','%s')" % (i, m, p, esc(n), esc(ne)) for i, m, p, n, ne in DUNGEONS]
    return table_sql("battlepass_dungeons", cols, rows, "Dungeon der Woche")

def sql_discoveries():
    cols = (["`id` INT UNSIGNED NOT NULL", "`zone` INT UNSIGNED NOT NULL",
             "`points` INT UNSIGNED NOT NULL DEFAULT 25",
             "`name` VARCHAR(80) NOT NULL DEFAULT ''", "`name_en` VARCHAR(80) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`id`)"],
            ["id", "zone", "points", "name", "name_en"])
    rows = ["(%d,%d,%d,'%s','%s')" % (i, z, DISCOVERY_POINTS, esc(n), esc(ne)) for i, z, n, ne in DISCOVERIES]
    return table_sql("battlepass_discoveries", cols, rows, "Verlorene Orte (Entdeckungs-System)")

def sql_achievements():
    cols = (["`id` INT UNSIGNED NOT NULL", "`kind` TINYINT UNSIGNED NOT NULL",
             "`goal` INT UNSIGNED NOT NULL DEFAULT 1", "`points` INT UNSIGNED NOT NULL DEFAULT 100",
             "`name` VARCHAR(120) NOT NULL DEFAULT ''", "`name_en` VARCHAR(120) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`id`)"],
            ["id", "kind", "goal", "points", "name", "name_en"])
    rows = ["(%d,%d,%d,%d,'%s','%s')" % (i, k, g, p, esc(n), esc(ne)) for i, k, g, p, n, ne in ACHIEVEMENTS]
    return table_sql("battlepass_achievements", cols, rows, "20 Saison-Erfolge")

def sql_supplies():
    cols = (["`id` INT UNSIGNED NOT NULL", "`item` INT UNSIGNED NOT NULL",
             "`count` INT UNSIGNED NOT NULL DEFAULT 20",
             "`points` INT UNSIGNED NOT NULL DEFAULT 150",
             "`gold` INT UNSIGNED NOT NULL DEFAULT 10000 COMMENT 'Kupfer'",
             "PRIMARY KEY (`id`)"],
            ["id", "item", "count", "points", "gold"])
    rows = ["(%d,%d,%d,%d,%d)" % s for s in SUPPLIES]
    return table_sql("battlepass_supplies", cols, rows, "Versorgungsauftraege (SoD Waylaid Supplies)")

def sql_fish():
    cols = (["`id` INT UNSIGNED NOT NULL", "`item` INT UNSIGNED NOT NULL",
             "`count` INT UNSIGNED NOT NULL DEFAULT 10",
             "`points` INT UNSIGNED NOT NULL DEFAULT 150",
             "`gold` INT UNSIGNED NOT NULL DEFAULT 10000 COMMENT 'Kupfer'",
             "PRIMARY KEY (`id`)"],
            ["id", "item", "count", "points", "gold"])
    rows = ["(%d,%d,%d,%d,%d)" % f for f in FISH]
    return table_sql("battlepass_fish", cols, rows, "Angelauftraege (taeglich rotierender Fisch)")

def sql_teleports():
    cols = (["`id` INT UNSIGNED NOT NULL",
             "`name` VARCHAR(60) NOT NULL DEFAULT ''", "`name_en` VARCHAR(60) NOT NULL DEFAULT ''",
             "`map` INT UNSIGNED NOT NULL DEFAULT 0",
             "`x` FLOAT NOT NULL", "`y` FLOAT NOT NULL", "`z` FLOAT NOT NULL",
             "`o` FLOAT NOT NULL DEFAULT 0", "PRIMARY KEY (`id`)"],
            ["id", "name", "name_en", "map", "x", "y", "z", "o"])
    rows = ["(%d,'%s','%s',%d,%.1f,%.1f,%.1f,%.2f)" % (i, esc(n), esc(ne), m, x, y, z, o)
            for i, n, ne, m, x, y, z, o in TELEPORTS]
    return table_sql("battlepass_teleports", cols, rows, "Teleport-Ziele der Traumpfadhüterin")

def sql_mutators():
    cols = (["`id` INT UNSIGNED NOT NULL", "`kind` TINYINT UNSIGNED NOT NULL",
             "`value` INT UNSIGNED NOT NULL DEFAULT 200 COMMENT 'Prozent'",
             "`name` VARCHAR(120) NOT NULL DEFAULT ''", "`name_en` VARCHAR(120) NOT NULL DEFAULT ''",
             "PRIMARY KEY (`id`)"],
            ["id", "kind", "value", "name", "name_en"])
    rows = ["(%d,%d,%d,'%s','%s')" % (i, k, v, esc(n), esc(ne)) for i, k, v, n, ne in MUTATORS]
    return table_sql("battlepass_mutators", cols, rows, "Wochen-Mutatoren (Open-World-Affixe)")

def shop_rows():
    """Alle Shop-Zeilen: erst die Traumkiste (kind 1), dann Items (kind 0).
    Jede Zeile bekommt ihre Kategorie (Seite im Shop-Tab) aus SHOP_CATS."""
    flat = [(1, tier, 1, price) for tier, price in SHOP_BOXES]
    flat += [(0, item, cnt, shop_price(price)) for item, cnt, price in SHOP]
    total = sum(c for _, _, c in SHOP_CATS)
    if total != len(flat):
        raise SystemExit("SHOP_CATS-Summe %d != Shop-Slots %d!" % (total, len(flat)))
    rows = []
    slot = 1
    cat_idx, cat_left = 1, SHOP_CATS[0][2]
    for kind, item, cnt, price in flat:
        while cat_left == 0:
            cat_idx += 1
            cat_left = SHOP_CATS[cat_idx - 1][2]
        rows.append((slot, kind, item, cnt, price, cat_idx))
        cat_left -= 1
        slot += 1
    return rows

def sql_vendor():
    out = ["-- mod-battlepass v4: Saisonhändlerinnen-Shop (Kauf im Fenster: .bp buy <slot>)",
           "-- kind: 0=Item (id=item_template), 1=Mystery-Box (id=Kistenstufe 1-3)",
           "DROP TABLE IF EXISTS `battlepass_shop`;",
           "CREATE TABLE `battlepass_shop` (",
           "  `slot` INT UNSIGNED NOT NULL,",
           "  `kind` TINYINT UNSIGNED NOT NULL DEFAULT 0,",
           "  `item` INT UNSIGNED NOT NULL,",
           "  `count` INT UNSIGNED NOT NULL DEFAULT 1,",
           "  `price` INT UNSIGNED NOT NULL DEFAULT 10000 COMMENT 'Kupfer',",
           "  PRIMARY KEY (`slot`)",
           ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;",
           "INSERT INTO `battlepass_shop` (`slot`,`kind`,`item`,`count`,`price`) VALUES"]
    rows = ["(%d,%d,%d,%d,%d)" % r[:5] for r in shop_rows()]
    out.append(",\n".join(rows) + ";")
    out.append("")
    out.append("-- Optionaler Deko-NPC Jinba (987002) bekommt die Items (ohne Boxen):")
    out.append("DELETE FROM `npc_vendor` WHERE `entry` = 987002;")
    out.append("INSERT INTO `npc_vendor` (`entry`,`slot`,`item`,`maxcount`,`incrtime`,`ExtendedCost`) VALUES")
    vrows = ["(987002,%d,%d,0,0,0)" % (slot, item) for slot, (item, cnt, price) in enumerate(SHOP)]
    out.append(",\n".join(vrows) + ";")
    return "\n".join(out) + "\n"

# ===========================================================================
#  Lua-Ausgabe (Addon-Daten, zweisprachig)
# ===========================================================================

def lua_pair(de, en):
    return 'name = "%s", en = "%s"' % (de, en)

def lua_data():
    out = []
    out.append("-- Automatisch generiert von gen_season.py: muss zur Server-SQL passen!")
    out.append("-- Alle Namen zweisprachig: .name = Deutsch, .en = Englisch")
    out.append("BP_TIER_COST = %d" % TIER_COST)
    out.append("BP_MAX_TIER = %d" % MAX_TIER)
    out.append("BP_SEASON = %d" % SEASON)
    out.append('BP_SEASON_NAME = "%s"' % SEASON_NAME)
    out.append('BP_SEASON_NAME_EN = "%s"' % SEASON_NAME_EN)
    out.append("")
    out.append("BP_REWARDS = {")
    for tier in range(1, MAX_TIER + 1):
        t, i, c, n, ne = free_reward(tier)
        line = '  [%d] = { free = { type = %d, id = %d, count = %d, %s }' % (tier, t, i, c, lua_pair(n, ne))
        if tier in FREE_CHESTS:
            de, en = CHEST_NAMES[FREE_CHESTS[tier]]
            line += ', chest = { tier = %d, %s }' % (FREE_CHESTS[tier], lua_pair(de, en))
        if tier in EPIC_TRACK:
            r = EPIC_TRACK[tier]
            if r == "CLASS":
                slot = [s for s, tt in SET_TIERS.items() if tt == tier][0]
                slotname = [p[1] for p in CLASS_SETS[1] if p[0] == slot][0]
                line += ', epic = { set = true, slot = "%s", name = "Klassenset: %s", en = "Class set: %s" }' % (slotname, slotname, slotname)
            else:
                et, ei, ec, en_, ene = r
                line += ', epic = { type = %d, id = %d, count = %d, %s }' % (et, ei, ec, lua_pair(en_, ene))
        line += " },"
        out.append(line)
    out.append("}")
    out.append("")
    out.append("BP_CLASS_SET = {")
    for cid in sorted(CLASS_SETS):
        token, mask, cname = CLASSES[cid]
        out.append('  ["%s"] = {' % token)
        for slot, slotname, source, name_de, name_en in CLASS_SETS[cid]:
            out.append('    [%d] = { id = %d, slot = "%s", %s },'
                       % (SET_TIERS[slot], set_entry(cid, slot), slotname, lua_pair(name_de, name_en)))
        out.append("  },")
    out.append("}")
    out.append("")
    out.append("BP_WEEKLY = {")
    for i, t, g, p, n, ne in WEEKLY:
        out.append('  [%d] = { type = %d, goal = %d, points = %d, %s },' % (i, t, g, p, lua_pair(n, ne)))
    out.append("}")
    out.append("")
    out.append("BP_RUNES = {")
    for i, k, s, c, n, ne, dd, dde, icon in RUNES:
        out.append('  [%d] = { kind = %d, spell = %d, cost = %d, %s, desc = "%s", desc_en = "%s", icon = "%s" },'
                   % (i, k, s, c, lua_pair(n, ne), dd, dde, icon))
    out.append("}")
    out.append("")
    out.append("BP_BOSSES = {")
    for _, entry, m, x, y, z, o, name, zone, zone_en in WORLDBOSSES:
        out.append('  { name = "%s", zone = "%s", zone_en = "%s" },' % (name, zone, zone_en))
    out.append("}")
    out.append("")
    out.append("BP_ZONES = {")
    for i, z, n, ne in ZONES:
        out.append('  { %s },' % lua_pair(n, ne))
    out.append("}")
    out.append("")
    out.append("BP_BOUNTIES = {")
    for i, e, p, n, ne, z, ze in BOUNTIES:
        out.append('  { %s, zone = "%s", zone_en = "%s", points = %d },' % (lua_pair(n, ne), z, ze, p))
    out.append("}")
    out.append("")
    out.append("BP_DUNGEONS = {")
    for i, m, p, n, ne in DUNGEONS:
        out.append('  { %s, points = %d },' % (lua_pair(n, ne), p))
    out.append("}")
    out.append("")
    out.append("BP_DISCOVERIES = {")
    for i, z, n, ne in DISCOVERIES:
        out.append('  [%d] = { %s, points = %d },' % (i, lua_pair(n, ne), DISCOVERY_POINTS))
    out.append("}")
    out.append("")
    out.append("BP_ACH = {")
    for i, k, g, p, n, ne in ACHIEVEMENTS:
        out.append('  [%d] = { kind = %d, goal = %d, points = %d, %s },' % (i, k, g, p, lua_pair(n, ne)))
    out.append("}")
    out.append("")
    out.append("BP_MUTATORS = {")
    for i, k, v, n, ne in MUTATORS:
        out.append('  [%d] = { kind = %d, value = %d, %s },' % (i, k, v, lua_pair(n, ne)))
    out.append("}")
    out.append("")
    out.append("BP_CHESTS = {")
    for i in sorted(CHEST_NAMES):
        de, en = CHEST_NAMES[i]
        out.append('  [%d] = { %s },' % (i, lua_pair(de, en)))
    out.append("}")
    out.append("")
    out.append("-- Kisten-Beutevorschau: Raritäts-Chancen (Promille) + kuratierter Pool")
    out.append("BP_CHEST_RARITY = {")
    for chest, chances in sorted(CHEST_RARITY.items()):
        out.append('  [%d] = { %s },' % (chest, ", ".join(str(c) for c in chances)))
    out.append("}")
    out.append("")
    out.append("BP_CHEST_LOOT = {")
    for rar, kind, iid, cnt, de, en, ws in CHEST_LOOT:
        out.append('  { rar = %d, kind = %d, id = %d, count = %d, w = { %d, %d, %d }, %s },'
                   % (rar, kind, iid, cnt, ws[0], ws[1], ws[2], lua_pair(de, en)))
    out.append("}")
    out.append("")
    out.append("-- Willkommenspaket (Stufe 0, klickbar im Fenster: .bp welcome)")
    out.append("BP_WELCOME = {")
    for t, i, c, n, ne in WELCOME:
        out.append('  { type = %d, id = %d, %s },' % (t, i, lua_pair(n, ne)))
    out.append("}")
    out.append("")
    out.append("-- Teleport-Ziele (Extras-Tab, .bp tp <index>)")
    out.append("BP_TELEPORTS = {")
    for i, n, ne, m, x, y, z, o in TELEPORTS:
        out.append('  [%d] = { %s },' % (i, lua_pair(n, ne)))
    out.append("}")
    out.append("")
    out.append("-- Versorgungsaufträge (Anzeige; aktiver Auftrag kommt per Sync)")
    out.append("BP_SUPPLIES = {")
    for i, item, cnt, pts, gold in SUPPLIES:
        out.append('  [%d] = { id = %d, count = %d, points = %d, gold = %d },' % (i, item, cnt, pts, gold))
    out.append("}")
    out.append("")
    out.append("-- Angelaufträge (Anzeige; aktiver Fisch kommt per Sync)")
    out.append("BP_FISH = {")
    for i, item, cnt, pts, gold in FISH:
        out.append('  [%d] = { id = %d, count = %d, points = %d, gold = %d },' % (i, item, cnt, pts, gold))
    out.append("}")
    out.append("")
    out.append("-- Sammlung (Journal im Sammlungs-Tab; Besitz prüft der Client selbst)")
    out.append("BP_COLLECTION = {")
    coll = []
    for entry, de, en in [(8491, "Katzentrage (Schwarz getigert)", "Cat Carrier (Black Tabby)"),
                          (38658, "Vampirfledermausjunges", "Vampiric Batling"),
                          (23713, "Hippogryphjunges", "Hippogryph Hatchling"),
                          (38628, "Netherrochenbaby", "Nether Ray Fry"),
                          (8500, "Papageienkäfig (Nymphensittich)", "Parrot Cage (Cockatiel)"),
                          (10360, "Schwarze Königsnatter", "Black Kingsnake"),
                          (8494, "Hyazinthara", "Hyacinth Macaw")]:
        coll.append((entry, de, en, 1))
    for entry, de, en in [(900134, "Traumkrone der Illidari", "Dream Cowl of the Illidari"),
                          (900135, "Wappenrock des Traumkreuzzugs", "Tabard of the Dream Crusade"),
                          (900136, "Traumkugel der Täuschung", "Dream Orb of Deception"),
                          (900102, "Wappenrock des Alptraums", "Tabard of the Nightmare"),
                          (23705, "Wappenrock der Flamme", "Tabard of Flame"),
                          (23709, "Wappenrock des Frosts", "Tabard of Frost"),
                          (43154, "Wappenrock des Argentumkreuzzugs", "Tabard of the Argent Crusade"),
                          (43157, "Wappenrock des Kirin Tor", "Tabard of the Kirin Tor"),
                          (18660, "Weltvergrößerer", "World Enlarger"),
                          (21540, "Elunes Laterne", "Elune's Lantern"),
                          (13379, "Piccoloflöte des flammenden Feuers", "Piccolo of the Flaming Fire")]:
        coll.append((entry, de, en, 2))
    for entry, de, en, cat in coll:
        out.append('  { id = %d, name = "%s", en = "%s", cat = %d },' % (entry, de, en, cat))
    out.append("}")
    out.append("")
    out.append("-- Shop der Saisonhändlerin (Shop-Tab, .bp buy <slot>; kind 1 = Mystery-Box)")
    out.append("BP_SHOP = {")
    for slot, kind, item, cnt, price, cat in shop_rows():
        out.append('  [%d] = { kind = %d, id = %d, count = %d, price = %d, cat = %d },'
                   % (slot, kind, item, cnt, price, cat))
    out.append("}")
    out.append("")
    out.append("-- Shop-Kategorien (Seiten im Shop-Tab)")
    out.append("BP_SHOP_CATS = {")
    for i, (de, en, _) in enumerate(SHOP_CATS, 1):
        out.append('  [%d] = { %s },' % (i, lua_pair(de, en)))
    out.append("}")
    return "\n".join(out) + "\n"

# ===========================================================================

def check_entry_collisions():
    """Bricht ab, wenn sich Custom-Item-Entries ueberschneiden (Serverstart-Killer!)."""
    seen = {}
    def claim(entry, what):
        if entry in seen:
            raise SystemExit("ID-KOLLISION: %d (%s vs %s) — Entry-Schema anpassen!" % (entry, seen[entry], what))
        seen[entry] = what
    for cid, pieces in CLASS_SETS.items():
        for slot, _, _, name, _ in pieces:
            claim(set_entry(cid, slot), "Set %s" % name)
    for entry, _, name, _, _ in SPECIAL_ITEMS:
        claim(entry, "Sonderitem %s" % name)
    for _, (entry, name, _) in MOUNT_CLONES.items():
        claim(entry, "Mount %s" % name)
    seen_loot = set()
    for rar, kind, iid, _, de, _, _ in CHEST_LOOT:
        key = (rar, kind, iid)
        if key in seen_loot:
            raise SystemExit("KISTEN-DUPLIKAT: %s (%s)" % (str(key), de))
        seen_loot.add(key)

def main():
    check_entry_collisions()
    os.makedirs(SQL_WORLD, exist_ok=True)
    os.makedirs(ADDON, exist_ok=True)

    rewards, n_rewards = sql_rewards()
    items, n_items = sql_items()

    files = {
        os.path.join(SQL_WORLD, "battlepass_rewards.sql"): rewards,
        os.path.join(SQL_WORLD, "battlepass_items.sql"): items,
        os.path.join(SQL_WORLD, "battlepass_chest_loot.sql"): sql_chest_loot(),
        os.path.join(SQL_WORLD, "battlepass_weekly.sql"): sql_weekly(),
        os.path.join(SQL_WORLD, "battlepass_runes.sql"): sql_runes(),
        os.path.join(SQL_WORLD, "battlepass_worldboss.sql"): sql_worldboss(),
        os.path.join(SQL_WORLD, "battlepass_zones.sql"): sql_zones(),
        os.path.join(SQL_WORLD, "battlepass_bounty.sql"): sql_bounty(),
        os.path.join(SQL_WORLD, "battlepass_dungeons.sql"): sql_dungeons(),
        os.path.join(SQL_WORLD, "battlepass_discoveries.sql"): sql_discoveries(),
        os.path.join(SQL_WORLD, "battlepass_achievements.sql"): sql_achievements(),
        os.path.join(SQL_WORLD, "battlepass_supplies.sql"): sql_supplies(),
        os.path.join(SQL_WORLD, "battlepass_fish.sql"): sql_fish(),
        os.path.join(SQL_WORLD, "battlepass_teleports.sql"): sql_teleports(),
        os.path.join(SQL_WORLD, "battlepass_mutators.sql"): sql_mutators(),
        os.path.join(SQL_WORLD, "battlepass_vendor.sql"): sql_vendor(),
        os.path.join(ADDON, "BattlePassData.lua"): lua_data(),
    }
    for path, content in files.items():
        with open(path, "w", newline="\n", encoding="utf-8") as f:
            f.write(content)
        print("geschrieben: %s (%d Zeilen)" % (os.path.relpath(path, BASE), content.count("\n")))

    print()
    print("Belohnungszeilen: %d | Custom-Items: %d | Wochenziele: %d | Runen: %d | Mutatoren: %d"
          % (n_rewards, n_items, len(WEEKLY), len(RUNES), len(MUTATORS)))

if __name__ == "__main__":
    main()
