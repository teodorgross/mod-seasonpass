# mod-battlepass — Dream Path (Traumpfad)

**A complete, free seasonal Battle Pass for AzerothCore (WotLK 3.3.5a) with a full in-game UI addon.**

🇩🇪 **[Deutsche Version → README.de.md](README.de.md)**

> ⚠️ **ALPHA TEST** — this entire project was built **in a single day** as an experiment
> (AI-pair-programming with Claude by Anthropic). It runs on our private server, but expect
> rough edges, balance quirks and the occasional dragon-sized bug. Feedback and issues are very welcome!

---

## What is this?

**Dream Path** (German: *Traumpfad*) turns your 3.3.5a private server into a season server in the spirit of
**Classic+ / Season of Discovery**: a 100-tier battle pass, cross-class ability runes, rotating world content,
mystery chests with a live quality-upgrade animation, and a Diablo-style **prestige/paragon endgame up to
Prestige 300** with enemy scaling.

Everything is **100% free** (no premium track — both reward tracks are open to everyone), all progress is
**character-bound**, and everything works through a **full click UI** — no NPCs required.
The whole UI is **bilingual (English / German)** with a persistent in-game language toggle.

Season 1: **“Call of the Nightmare Dragons”** (*Ruf der Alptraumdrachen*).

## Screenshots

| Rewards & season bar | Weekly goals | Runes |
|---|---|---|
| ![Rewards](docs/img/rewards.png) | ![Weekly goals](docs/img/weekly.png) | ![Runes](docs/img/runes.png) |

| Live events | Character | Chests |
|---|---|---|
| ![Events](docs/img/events.png) | ![Character](docs/img/character.png) | ![Chests](docs/img/chests.png) |

| Prestige (Dream Forge) | Shop | Welcome package |
|---|---|---|
| ![Prestige](docs/img/prestige.png) | ![Shop](docs/img/shop.png) | ![Welcome](docs/img/welcome.png) |

---

## Feature overview — really everything

The addon window has **11 tabs**:

| Tab | What it does |
|---|---|
| **Rewards** | 100 tiers, two parallel tracks (Adventure + Hero — **both free**), click to claim, tier-0 welcome package |
| **Weekly Goals** | 3 rotating goals out of 40 definitions, weekly reroll (“Dream Swap”), daily supply run, daily fishing contract |
| **Runes** | 12 permanent buff runes + 12 **cross-class ability runes** (SoD style), starting ability picker |
| **Class Set** | A 4-piece epic set per class that **scales from level 1 to 80** (heirloom curve), no proficiency needed |
| **Events** | Live view: event zone, bounty of the day, dungeon of the week, world boss, weekly mutator, dream storm |
| **Achievements** | 24 season achievements with progress bars |
| **Character** | Play time, gold, attributes, crit — plus 14 season statistics |
| **Collection** | Season journal: pets & cosmetics with owned-checkmarks |
| **Shop** | Season vendor with ~118 curated items on 6 category pages + the Dream Chest |
| **Chests** | Full loot preview with **exact drop chances** for every possible item |
| **Prestige** | The Dream Forge: distribute paragon points into 8 stats |

Plus: a **season bar** above the action bar (Dream Path progress + character level), a **minimap dragon button**,
level-up fanfares with banner, and a **chest-opening animation** in the middle of the screen.

### The Season Pass

- **100 tiers**, 100 points per tier. Two tracks, both free: the Adventure track (gold, chests, pets, toys,
  emblems, titles like *Jenkins* and *Kingslayer*) and the Hero track (class set pieces, tabards, bigger gold).
- **Welcome package** at tier 0 for every character: Dream Cowl of the Illidari (Black-Temple look!),
  Tabard of the Dream Crusade, Dream Orb of Deception, 5 gold starting capital.
- **Points come from everything**: quests, kills, elites, rares, dungeon bosses, level-ups, duels, discoveries
  (18 lost places), daily login (with streak bonus), weekly goals, world bosses, deliveries, fishing — and
  every opened chest.
- Point multipliers: **bonus weekend** (Sat+Sun), **event zone** (x2), **dream storm** (x3 for 15 minutes),
  weekly **mutators** (8 rotating weekly modifiers like “quest points x2”), prestige **season legacy** bonus.

### Dream Chests 📦

There is **one** chest: the **Dream Chest**. When you open it, its quality is rolled live with a
screen-center animation (colors cycle, then lock in):

- 🔵 **Blue** (50%) → 2 pulls &nbsp; 🟣 **Mythic** (35%) → 3 pulls &nbsp; 🟠 **Golden** (15%) → 4 pulls
- **Chest Fever** (pity system): every chest without an epic raises upgrade *and* epic chances for the next one.
- Curated **100-entry loot pool** in 4 rarities: consumables & fun items (including deliberate duds like a
  fishing pole), pets, flasks, bags, iconic cosmetics (Orb of Deception, Don Carlos' hat, Flag of Ownership,
  Arcanite Fishing Pole …), gold up to 500g jackpots, the **Lost Rune** (instantly teaches a random unknown
  ability rune) — and the **only source of mounts**: ultra-rare no-requirement clones of Invincible,
  Mimiron's Head, Ashes of Al'ar, the Nightmare Drake and more. Legendary pulls are announced server-wide!
- Opening a chest always grants **+10 season points** and counts toward 2 chest achievements.
- Chests drop from mobs in the endgame/prestige mode, come from the pass, the shop (100g), and the daily
  fishing contract. The **Chests tab** shows every possible drop with its exact percentage.

### Seasonal Runes (SoD style)

- **12 permanent buff runes** — deliberately mild (max ~10%: Blessing of Kings +10% stats, Trueshot +10% AP,
  Leader of the Pack +5% crit, Sanctuary −3% damage taken, plus rank-1 classics). The auras never expire.
- **Rune Resonance**: every engraved buff rune additionally grants **+2% damage, +2% health, +2% healing**.
- **12 ability runes** that teach real spells to ANY class: Taunt, Righteous Fury, Fear Ward, Blink, Sprint,
  Stealth, Astral Recall, Water Walking, Water Breathing, Lay on Hands, Eagle Eye, Bloodlust.
- 3 rune slots, +1 at tier 25 / 50 / 75. Engraving costs gold, removing is free.
- **Starting ability**: every character picks one free cross-class ability once.

### Prestige & the Dream Forge (paragon endgame)

- Reach tier 100 → prestige. From then on **every 100 points = +1 prestige level directly** (no more tiers),
  up to **Prestige 300**.
- Every prestige: **+2 Dream Forge points**, gold, **+3% permanent XP** — and a fanfare.
- **8 paragon stats** (cap 75 each — you can't max everything, choose a build!): melee damage, spell damage,
  **AoE damage**, **poison/DoT damage**, max health, max mana, healing done, experience. Free respec anytime.
- **Enemies scale with you**: per prestige level monsters deal +1% damage and have +1% effective health.
  At P300 they are 4× as tough — your paragon build, gear and runes are the answer.
- Prestige **replaces the level display**: portrait ring, character sheet and season bar show your prestige
  level in paragon orange. Every 10th prestige is announced server-wide.

### Live world content

- **Event zone** (rotates every 3h, double points), **bounty of the day** (classic elites like Hogger with
  their own announcement), **dungeon of the week** (bonus points for boss kills).
- **World boss rotation** (6 bosses: the four Emerald dragons at their real portals, Lord Kazzak, Azuregos):
  when one dies, **the whole server** gets *Rallying Cry of the Dragonslayer*.
- **Weekly mutators** (8) and the surprise **Dream Storm** (x3 points for 15 minutes, hourly chance).
- **Daily supply runs** (Waylaid-Supplies homage, 21 rotating trade goods) and a **daily fishing contract**
  (catch 10 of the day's fish → 150 points, 10 gold and a bonus Dream Chest — counted automatically while fishing).

### Quality of life

- All custom items are **requirement-free clones** — usable at level 1, mounts without riding skill,
  class sets without armor/weapon proficiency.
- Progress is **fully character-bound** (per-GUID), new characters start at 0.
- Icon pre-warming against 3.3.5 “?”-icon cache issues, tooltips everywhere, exact chances shown.

---

## How it works (architecture)

```
gen_season.py  ──►  16 SQL files (world DB)  ──►  auto-applied by AzerothCore's module updater
      │
      └──────►  BattlePassUI/BattlePassData.lua  (addon data — always in sync with the DB)

mod-battlepass/src/   C++ module (2 scripts + header, no CMakeLists needed)
BattlePassUI/         3.3.5a client addon (pure Lua, no libraries)
```

- **One generator, one truth**: `gen_season.py` produces both the SQL content *and* the addon data file,
  so server and UI can never drift apart. Edit the season there, run it, re-deploy.
- **Server ⇄ addon sync** runs over hidden chat system messages (`BPSYNC`, `BPWK`, `BPRN`, `BPEV`, `BPACH`,
  `BPSUP`, `BPFI`, `BPPG`, `BPCHEST`) which the addon filters out of the chat frame; the addon sends
  invisible `.bp` commands back. No custom opcodes, no core edits.
- All module SQL is **idempotent** (safe for AzerothCore's automatic module updater — character tables
  self-migrate).
- Rotations (event zone, bounty, dungeon, mutator, supplies, fish, storm) are **deterministic from time** —
  restarts change nothing, every player sees the same world.

## Installation (AzerothCore)

**Requirements:** an [AzerothCore](https://github.com/azerothcore/azerothcore-wotlk) server (WotLK 3.3.5a).
Developed and tested against the [Playerbot fork](https://github.com/liyunfan1223/azerothcore-wotlk) in
July 2026 — recent master should work too (hook signatures may differ slightly; fixes are usually one-liners).

### 1. Server module

```bash
cd /path/to/azerothcore/modules
git clone https://github.com/teodorgross/mod-battlepass.git mod-battlepass
cd ../build
cmake .
make -j$(nproc) && make install
```

*(The repo also contains the addon and the generator — the server only compiles `mod-battlepass/`.)*

### 2. Database

Nothing to do 🎉 — AzerothCore's module SQL updater applies everything in
`mod-battlepass/data/sql/` automatically on the next worldserver start
(world content tables + self-migrating character tables).

### 3. Client addon

Copy the **`BattlePassUI`** folder into your 3.3.5a client:

```
World of Warcraft/Interface/AddOns/BattlePassUI
```

Log in, click the dragon button at the minimap (or the season bar) — done.

### 4. Optional configuration

All options live in your `worldserver.conf` — every key has a sane default, the module works with zero config:

| Key | Default | Meaning |
|---|---|---|
| `BattlePass.Enable` | 1 | Master switch |
| `BattlePass.PointsPerTier` | 100 | Points per tier / per prestige level |
| `BattlePass.MaxTier` | 100 | Tiers per season |
| `BattlePass.Points.Quest/Kill/EliteKill/BossKill/RareKill/LevelUp/DailyLogin` | 10/1/5/100/25/50/50 | Point sources |
| `BattlePass.Chest.Enable` | 1 | Dream chests |
| `BattlePass.Chest.PityStepPct` | 5 | Chest Fever step per chest without an epic |
| `BattlePass.Prestige.Max` | 300 | Prestige cap |
| `BattlePass.Prestige.XPPctPerLevel` | 3 | Permanent XP bonus per prestige |
| `BattlePass.Prestige.AutoGold` | 100000 | Copper per auto-prestige level |
| `BattlePass.Paragon.PointsPerPrestige` | 2 | Dream Forge points per prestige |
| `BattlePass.Paragon.CapPerStat` | 75 | Paragon cap per stat |
| `BattlePass.Paragon.MobScalePctPerPrestige` | 1 | Enemy scaling per prestige |
| `BattlePass.Runes.ResonancePct` | 2 | Rune Resonance per engraved buff rune |

### Commands

Players never need commands (the UI sends them invisibly), but they exist:
`.bp` (status), `.bp claim`, `.bp weekly`, `.bp reroll <slot>`, `.bp rune <id>`, `.bp buy <slot>`,
`.bp welcome`, `.bp deliver`, `.bp startrune <id>`, `.bp prestige ja|yes`, `.bp paragon <1-8> [n]`,
`.bp paragon reset`, `.bp lang <de|en>`, `.bp sync` — GM only: `.bp addpoints <n>`, `.bp chest <0-3>`.

### Building your own season

Edit **`gen_season.py`** (rewards, chest loot, runes, shop, bosses — every piece of content lives there), then:

```bash
python gen_season.py
```

Re-deploy the SQL folder and the addon folder. That's the whole content pipeline.
For Season 2: set `SEASON = 2` in the generator and `BattlePass.Season = 2` in the config.

---

## Alpha notes / known limitations

- Built in one day — treat it as a **playable prototype**, not a finished product.
- Collection ownership is checked via bags+bank: an already *used* pet counts as “missing”.
- A handful of TCG/anniversary item IDs may not exist on every DB — the server skips them safely at roll time.
- Balance numbers (points, prices, chances, enemy scaling) are first-pass values. Tune them in the config!

## Credits & Thanks ❤️

- **[AzerothCore](https://github.com/azerothcore/azerothcore-wotlk)** and all its contributors — the finest
  open-source WotLK core there is. This module is a guest in their house. Thank you!
- **[liyunfan1223](https://github.com/liyunfan1223)** and the
  **[mod-playerbots](https://github.com/liyunfan1223/mod-playerbots)** community — the playerbot fork this
  was built and tested on. Thank you!
- The **Classic+ / Season of Discovery** community, whose wishlists inspired half of these features.
- Built in a single day together with **Claude (Anthropic)** as an AI-pair-programming experiment.
- World of Warcraft® and Blizzard Entertainment® are trademarks of Blizzard Entertainment, Inc.
  This is a non-commercial fan project for private/educational servers.

## License

Released under the **GNU AGPL v3** — the same license as AzerothCore. See [LICENSE](LICENSE).
