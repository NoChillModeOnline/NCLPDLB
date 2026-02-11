# ⚡ Tera Captain System - Complete Guide

The Tera Captain system is a strategic layer that adds depth to team building and battle tactics in the Pokémon Draft League.

---

## 📋 Table of Contents

- [What are Tera Captains?](#-what-are-tera-captains)
- [Tera Captain Rules](#-tera-captain-rules)
- [Setting Up Tera Captains](#-setting-up-tera-captains)
- [All 19 Tera Types](#-all-19-tera-types)
- [Command Reference](#-command-reference)
- [Strategy Guide](#-strategy-guide)
- [Validation & Error Messages](#-validation--error-messages)
- [FAQ](#-faq)

---

## 🎯 What are Tera Captains?

**Tera Captains** are special designated Pokémon on your team that can **Terastallize** during battles. Terastallizing changes a Pokémon's type, which can:

- **Cover weaknesses** (e.g., Dragon Tera on a Fairy-weak Pokémon)
- **Boost STAB** (Same Type Attack Bonus)
- **Create surprise matchups** (e.g., Water-type using Ground Tera to counter Electric)
- **Gain defensive advantages** (e.g., Ghost Tera to avoid Fighting moves)

### Key Points
- ✅ You must have **exactly 3 Tera Captains**
- ✅ Choose from **19 different Tera types**
- ✅ Only **lower-cost Pokémon** can be Tera Captains
- ✅ Change Tera types **between weeks** (not during matches)
- ✅ **One Terastallization per battle** (standard VGC rules)

---

## 📏 Tera Captain Rules

### 1. Exactly 3 Tera Captains Required

You **must** designate exactly 3 Pokémon as Tera Captains. Not 2, not 4—exactly 3.

```
❌ 2 Tera Captains → INVALID (need 3)
✅ 3 Tera Captains → VALID
❌ 4 Tera Captains → INVALID (max is 3)
```

### 2. Individual Point Cost Limit: ≤13 Points

Only Pokémon that cost **13 points or less** can be designated as Tera Captains.

**Examples:**
```
✅ Pikachu (8 points) → Can be Tera Captain
✅ Rotom (11 points) → Can be Tera Captain
✅ Marowak (13 points) → Can be Tera Captain
❌ Charizard (15 points) → Cannot be Tera Captain (too expensive)
❌ Garchomp (14 points) → Cannot be Tera Captain (over 13 limit)
```

**Why this restriction?**
This prevents coaches from making their strongest Pokémon even more versatile. It encourages strategic use of mid-tier Pokémon as Tera Captains.

### 3. Total Point Cost Limit: ≤25 Points

The **combined cost** of all 3 Tera Captains must be **25 points or less**.

**Valid Examples:**
```
✅ Pikachu (8) + Rotom (11) + Marowak (6) = 25 points → VALID
✅ Talonflame (10) + Arcanine (9) + Tauros (5) = 24 points → VALID
✅ Sylveon (11) + Clefable (12) + Azumarill (2) = 25 points → VALID
```

**Invalid Examples:**
```
❌ Rotom (11) + Sylveon (11) + Marowak (6) = 28 points → TOO HIGH
❌ Arcanine (13) + Talonflame (13) + Pikachu (8) = 34 points → TOO HIGH
```

**Pro Tip:** Plan your draft with Tera Captain restrictions in mind! Draft a mix of high-cost stars and lower-cost Tera Captain candidates.

### 4. Valid Tera Types: 19 Options

Each Tera Captain can Terastallize to **any of 19 types**:

#### 18 Standard Types
Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy

#### 1 Special Type
**Stellar** ✨ - The 19th type introduced in Pokémon Scarlet & Violet

**Note:** The Stellar type has unique mechanics in-game. Check Bulbapedia or Serebii for details on how Stellar Tera works in VGC battles.

---

## 🛠️ Setting Up Tera Captains

### When to Set Tera Captains

- ✅ **After the draft completes** - Once you have your 10-12 Pokémon
- ✅ **Before Week 1 battles** - Set them before your first match
- ✅ **Between weeks** - Change Tera types strategically based on matchups
- ❌ **During a match** - Cannot change once the week's battles start

### Step-by-Step Setup

**1. Check your team roster:**
```
!roster
```
This shows all your drafted Pokémon with their point costs.

**2. View valid Tera types:**
```
!tera types
```
Shows all 19 types with their emojis for reference.

**3. Designate your first Tera Captain:**
```
!tera set Pikachu Dragon
```
Makes Pikachu a Dragon-type Tera Captain.

**4. Designate your second Tera Captain:**
```
!tera set Rotom Steel
```
Makes Rotom a Steel-type Tera Captain.

**5. Designate your third Tera Captain:**
```
!tera set Marowak Fire
```
Makes Marowak a Fire-type Tera Captain.

**6. View your Tera Captains:**
```
!tera show
```
or just:
```
!tera
```
Displays all 3 of your Tera Captains with their types and emojis.

**7. Scout opponents:**
```
!tera show @OpponentName
```
View another player's Tera Captains (if set).

**8. View all league Tera Captains:**
```
!tera list
```
Shows all Tera Captains grouped by player.

---

## 🌈 All 19 Tera Types

| Type | Emoji | Strengths | Weaknesses | Immunities |
|------|-------|-----------|------------|------------|
| **Normal** | ⚪ | None | Fighting | Ghost |
| **Fire** | 🔥 | Grass, Ice, Bug, Steel | Water, Ground, Rock | None |
| **Water** | 💧 | Fire, Ground, Rock | Electric, Grass | None |
| **Electric** | ⚡ | Water, Flying | Ground | None |
| **Grass** | 🌿 | Water, Ground, Rock | Fire, Ice, Poison, Flying, Bug | None |
| **Ice** | ❄️ | Grass, Ground, Flying, Dragon | Fire, Fighting, Rock, Steel | None |
| **Fighting** | 🥊 | Normal, Ice, Rock, Dark, Steel | Flying, Psychic, Fairy | None |
| **Poison** | ☠️ | Grass, Fairy | Ground, Psychic | None |
| **Ground** | 🌍 | Fire, Electric, Poison, Rock, Steel | Water, Grass, Ice | Electric |
| **Flying** | 🦅 | Grass, Fighting, Bug | Electric, Ice, Rock | Ground |
| **Psychic** | 🔮 | Fighting, Poison | Bug, Ghost, Dark | None |
| **Bug** | 🐛 | Grass, Psychic, Dark | Fire, Flying, Rock | None |
| **Rock** | 🪨 | Fire, Ice, Flying, Bug | Water, Grass, Fighting, Ground, Steel | None |
| **Ghost** | 👻 | Psychic, Ghost | Ghost, Dark | Normal, Fighting |
| **Dragon** | 🐉 | Dragon | Ice, Dragon, Fairy | None |
| **Dark** | 🌑 | Psychic, Ghost | Fighting, Bug, Fairy | Psychic |
| **Steel** | ⚙️ | Ice, Rock, Fairy | Fire, Fighting, Ground | Poison |
| **Fairy** | 🧚 | Fighting, Dragon, Dark | Poison, Steel | Dragon |
| **Stellar** | ✨ | Special Mechanics | Special Mechanics | None |

**Note:** Stellar type has unique battle mechanics. It provides a one-time power boost to moves of all types. Consult official VGC resources for detailed Stellar Tera mechanics.

---

## 🎮 Command Reference

### View Commands

#### `!tera` or `!tera show`
View your own Tera Captains.

**Output:**
```
⚡ Your Tera Captains
━━━━━━━━━━━━━━━━━━━━
🔥 Pikachu → 🐉 Dragon Tera (8 pts)
⚙️ Rotom → ⚙️ Steel Tera (11 pts)
🦴 Marowak → 🔥 Fire Tera (6 pts)
━━━━━━━━━━━━━━━━━━━━
Total Points: 25/25
```

#### `!tera show @Player`
View another player's Tera Captains.

**Example:**
```
!tera show @Alice
```

#### `!tera list`
View all Tera Captains in the league, grouped by player.

**Output:**
```
🌟 All Tera Captains in the League
━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎮 Alice (Fire Fighters)
  • Pikachu → 🐉 Dragon (8 pts)
  • Rotom → ⚙️ Steel (11 pts)
  • Marowak → 🔥 Fire (6 pts)

🎮 Bob (Water Warriors)
  • Sylveon → 💧 Water (11 pts)
  • Arcanine → 🌿 Grass (9 pts)
  • Tauros → ⚡ Electric (5 pts)
```

#### `!tera types`
Display all 19 valid Tera types with emojis.

**Output:**
```
🌈 Valid Tera Types (19 total)
━━━━━━━━━━━━━━━━━━━━━━━━━
⚪ Normal    🔥 Fire      💧 Water
⚡ Electric  🌿 Grass     ❄️ Ice
🥊 Fighting  ☠️ Poison    🌍 Ground
🦅 Flying    🔮 Psychic   🐛 Bug
🪨 Rock      👻 Ghost     🐉 Dragon
🌑 Dark      ⚙️ Steel     🧚 Fairy
✨ Stellar
━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Management Commands

#### `!tera set <pokemon> <type>`
Designate a Pokémon as a Tera Captain with a specific type.

**Examples:**
```
!tera set Pikachu Dragon
!tera set Rotom Steel
!tera set Marowak Stellar
```

**Validation:**
- ✅ Pokémon must be on your roster
- ✅ Pokémon cost must be ≤13 points
- ✅ You must have less than 3 Tera Captains already set
- ✅ Total Tera Captain points must be ≤25
- ✅ Type must be one of the 19 valid types

#### `!tera change <pokemon> <new_type>`
Change an existing Tera Captain's type.

**Examples:**
```
!tera change Pikachu Fire
!tera change Rotom Ghost
```

**Use Cases:**
- Adapt to upcoming opponent matchups
- Counter specific strategies
- Change between weeks based on meta

#### `!tera remove <pokemon>`
Remove Tera Captain designation from a Pokémon.

**Examples:**
```
!tera remove Pikachu
```

**Use Cases:**
- Free up a slot to designate a different Pokémon
- Adjust after a trade
- Rebalance point allocation

### Help Command

#### `!tera help`
Show detailed help for all Tera Captain commands.

**Output:** Full command reference with examples and descriptions.

---

## 🧠 Strategy Guide

### 1. Defensive Tera Typing

Use Tera types to **cover your Pokémon's weaknesses**.

**Example:**
- **Garchomp** (Dragon/Ground) is 4x weak to Ice
- Use **Fire Tera** to resist Ice moves and threaten Ice-types back

**More Examples:**
```
Pokémon         | Weakness        | Defensive Tera | Benefit
----------------|-----------------|----------------|------------------
Salamence       | Ice (4x)        | Steel Tera     | Resists Ice
Charizard       | Rock (4x)       | Water Tera     | Resists Rock
Tyranitar       | Fighting (4x)   | Ghost Tera     | Immune to Fighting
```

### 2. Offensive Tera Typing

Use Tera types to **gain offensive coverage** your team lacks.

**Example:**
- Your team has no Electric coverage
- Give **Pikachu Electric Tera** to boost its STAB moves to nuclear levels

**More Examples:**
```
Situation                  | Solution
---------------------------|----------------------------------
Team weak to Water         | Ground Tera on a physical attacker
Need Fairy coverage        | Fairy Tera on a special attacker
Struggling vs Dragons      | Ice Tera on a fast Pokémon
```

### 3. STAB Amplification

Terastallizing to a Pokémon's **existing type** boosts that type's moves significantly.

**Example:**
- **Pikachu** (Electric) with **Electric Tera**
- Thunderbolt becomes extremely powerful with double STAB

**Formula:**
- Normal STAB: 1.5x damage
- Tera STAB (same type): 2x damage
- **The boost is MASSIVE**

### 4. Surprise Factor

Use **unexpected Tera types** to catch opponents off-guard.

**Examples:**
```
Pokémon    | Expected Tera | Surprise Tera | Why It Works
-----------|---------------|---------------|---------------------------
Gyarados   | Water/Dragon  | Ground Tera   | Beats Electric-types
Dragonite  | Dragon        | Flying Tera   | Immune to Ground
Gengar     | Ghost/Poison  | Normal Tera   | Immune to Fighting/Ghost
```

### 5. Meta Adaptation

Change Tera types **between weeks** to adapt to the meta or specific opponents.

**Week-by-Week Strategy:**
```
Week 1: Set balanced defensive Tera types
Week 2: Scout opponents' teams with !tera list
Week 3: Adjust Tera types to counter common threats
Week 4: Use surprise Tera types for playoffs
```

### 6. Point Budget Planning

When drafting, **reserve 25 points** for Tera Captain candidates.

**Sample Draft Strategy:**
```
Budget Allocation:
- 60 points: 4 "star" Pokémon (15 pts each)
- 25 points: 3 Tera Captain candidates (≤13 pts each)
- 35 points: 4-5 role players (7-9 pts each)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 120 points, 11-12 Pokémon
```

### 7. Stellar Type Strategy

The **Stellar type** has unique mechanics:
- One-time boost to ALL move types
- Best used on **mixed attackers** (use both physical and special moves)
- Great for Pokémon with wide move pools

**Best Stellar Tera Candidates:**
- Mixed attackers (Attack + Sp. Attack)
- Pokémon with diverse coverage moves
- Support Pokémon that use multiple move types

---

## ⚠️ Validation & Error Messages

The bot automatically validates all Tera Captain operations. Here are common errors and how to fix them:

### Error: "Pokémon not on your roster"

**Message:**
```
❌ Pikachu is not on your roster!
Use !roster to see your drafted Pokémon.
```

**Fix:** Check your roster with `!roster` and use the correct Pokémon name.

### Error: "Pokémon too expensive"

**Message:**
```
❌ Charizard costs 15 points!
Only Pokémon with ≤13 points can be Tera Captains.
```

**Fix:** Choose a Pokémon that costs 13 points or less.

### Error: "Already have 3 Tera Captains"

**Message:**
```
❌ You already have 3 Tera Captains!
Use !tera remove <pokemon> to free up a slot first.
```

**Fix:** Remove one of your existing Tera Captains before adding a new one.

### Error: "Total points exceed 25"

**Message:**
```
❌ Adding Rotom (11 pts) would make your total 28 points!
Tera Captain total must be ≤25 points.
Current: Pikachu (8 pts), Marowak (9 pts) = 17 pts
```

**Fix:** Choose a lower-cost Pokémon or remove/replace existing Tera Captains.

### Error: "Invalid Tera type"

**Message:**
```
❌ 'Shadow' is not a valid Tera type!
Use !tera types to see all 19 valid types.
```

**Fix:** Use `!tera types` to see valid types and correct your spelling.

### Error: "Not a Tera Captain"

**Message:**
```
❌ Pikachu is not currently a Tera Captain!
Use !tera show to see your Tera Captains.
```

**Fix:** Check your current Tera Captains with `!tera show`.

### Error: "Need exactly 3 Tera Captains"

**Message:**
```
⚠️ You only have 2 Tera Captains set!
You must have exactly 3 before battles can start.
Use !tera set <pokemon> <type> to add another.
```

**Fix:** Designate one more Tera Captain to reach the required 3.

---

## ❓ FAQ

### Q: Can I change my Tera Captain types during the season?
**A:** Yes! You can change Tera types between weeks using `!tera change <pokemon> <new_type>`. You cannot change during active battle weeks.

### Q: What happens if I trade away a Tera Captain?
**A:** The bot automatically removes the Tera Captain designation when you trade that Pokémon. You'll need to designate a new Tera Captain to maintain exactly 3.

### Q: Can I have two Tera Captains with the same type?
**A:** Yes! You can have multiple Tera Captains with the same Tera type. For example, all 3 could be Dragon Tera if you want.

### Q: Do I have to use my Tera Captain's designated type in battle?
**A:** In-game, once you Terastallize, you use the type you've designated. You cannot change it mid-battle. Plan your Tera types strategically!

### Q: Can I Terastallize multiple Pokémon in one battle?
**A:** No. Standard VGC rules apply: **one Terastallization per battle**. Choose wisely!

### Q: What if I don't have 3 Pokémon under 13 points?
**A:** This is a drafting mistake! Always ensure you draft at least 3 Pokémon with ≤13 points. The bot will warn you during the draft if you're at risk of violating Tera Captain requirements.

### Q: Is Stellar type better than other types?
**A:** Stellar has unique mechanics that can be powerful in specific situations, but it's not strictly "better." It depends on your team composition and strategy.

### Q: Can I see my opponent's Tera Captains before battling them?
**A:** Yes! Use `!tera show @OpponentName` to see their Tera Captains and types. This is public information and allows for strategic preparation.

### Q: What happens if I don't set Tera Captains before Week 1?
**A:** The bot will prevent battles from starting until all coaches have set exactly 3 Tera Captains. Make sure to complete this step!

### Q: Can I use the same Tera type on all 3 Tera Captains?
**A:** Yes, there's no restriction on using the same type multiple times. However, diversity often provides better strategic options.

---

## 📚 Additional Resources

- **LEAGUE_RULES.md** - Complete league rules and systems
- **README.md** - Bot setup and command reference
- **QUICK_START.md** - Get started in 10 minutes
- **Bulbapedia Terastal Guide** - https://bulbapedia.bulbagarden.net/wiki/Terastal_phenomenon
- **Serebii VGC Rules** - https://www.serebii.net/games/vgc.shtml

---

**Built with ❤️ for strategic Pokémon battles!** ⚡🎮
