# 🏆 Competitive Pokémon Resources

This bot is designed around competitive Pokémon battling principles used in VGC (Video Game Championships) and Smogon formats. Understanding these resources will help you build better teams and make strategic decisions.

---

## 📚 Official VGC Resources

### What is VGC?

**VGC (Video Game Championships)** is the official competitive Pokémon format used in The Pokémon Company International's tournaments. Our draft league uses VGC rules as the foundation.

**Official VGC Website:**
- https://www.pokemon.com/us/play-pokemon/pokemon-events/pokemon-tournaments/vgc/

**Key VGC Rules Used in This Bot:**
- ✅ Double Battles format (2v2)
- ✅ Bring 6, Pick 4 per battle
- ✅ Best-of-Three sets
- ✅ Terastallization mechanics (Gen 9)
- ✅ Species Clause enforcement
- ✅ Standard battle clauses

### Current VGC Format

**VGC 2025 (Regulation H)** - As of February 2026:
- Pokémon Scarlet & Violet format
- Terastallization allowed (one per battle)
- Restricted Pokémon rules vary by regulation
- Paldean Pokédex + DLC Pokémon

**Learn More:**
- https://www.pokemon.com/us/play-pokemon/pokemon-events/pokemon-tournaments/vgc/
- https://bulbapedia.bulbagarden.net/wiki/VGC

---

## 🎓 Smogon University Resources

### What is Smogon?

**Smogon University** is the premier competitive Pokémon community, providing:
- Tier lists and usage statistics
- Strategy guides for every Pokémon
- Move set recommendations
- Team building resources
- Competitive analysis

**Smogon Homepage:**
- https://www.smogon.com/

### Essential Smogon Resources

#### 1. **Strategy Pokédex**
Comprehensive guides for every Pokémon:
- https://www.smogon.com/dex/

**What You'll Find:**
- Recommended move sets
- EV (Effort Value) spreads
- Item choices
- Team synergy recommendations
- Common counters and checks

**Example:** Want to know the best Charizard build?
→ https://www.smogon.com/dex/sv/pokemon/charizard/

#### 2. **Damage Calculator**
Calculate exact damage for any matchup:
- https://calc.pokemonshowdown.com/

**Features:**
- Exact damage ranges
- Speed tier comparisons
- Defensive calculations
- Multi-target damage (for doubles)

**Use Cases:**
- "Can my Pikachu OHKO that Gyarados?"
- "Will I survive this attack?"
- "Do I outspeed after Tailwind?"

#### 3. **Team Builder**
Visual team composition tool:
- https://play.pokemonshowdown.com/teambuilder

**Features:**
- Type coverage visualization
- Weakness checker
- Import/export teams
- Share team codes

#### 4. **Viability Rankings**
Competitive tier lists:
- https://www.smogon.com/forums/forums/smogon-metagames.206/

**Formats:**
- VGC tier lists
- Usage statistics
- Meta analysis

---

## 🔍 Type Chart & Effectiveness

### Official Type Chart Reference

**Bulbapedia Type Chart:**
- https://bulbapedia.bulbagarden.net/wiki/Type/Type_chart

**This Bot's TYPE_CHART** is based on official Gen 9 type effectiveness:
- Super Effective: 2.0x damage
- Not Very Effective: 0.5x damage
- No Effect: 0.0x damage (immune)

**Dual-Type Calculations:**
- Multiply both type effectiveness values
- Example: Ice move vs Dragon/Flying → 2.0 × 2.0 = 4.0x (4x super effective!)

### Terastallization Mechanics

**What is Terastallization?**
- Gen 9 mechanic from Scarlet & Violet
- Changes Pokémon's type mid-battle
- One use per battle
- Provides STAB (Same Type Attack Bonus) boost

**Official Resources:**
- https://bulbapedia.bulbagarden.net/wiki/Terastal_phenomenon
- https://www.serebii.net/scarletviolet/terastallise.shtml

**Tera Type Strategy:**
- **Defensive Tera:** Cover weaknesses (e.g., Ground Tera on Electric-weak team)
- **Offensive Tera:** Boost STAB damage (e.g., Fire Tera on Fire-type for massive Flamethrower)
- **Utility Tera:** Change resistances (e.g., Ghost Tera for Fighting immunity)

**Stellar Tera Type:**
- Unique Gen 9 Tera type
- Powers up all move types once each
- Complex mechanics - see Bulbapedia link above

---

## 📊 Team Building Principles

### Core Team Composition

Based on Smogon and VGC team building philosophy:

#### 1. **FWG Core (Fire-Water-Grass)**
Classic balanced core:
- Fire beats Grass, Steel, Bug, Ice
- Water beats Fire, Ground, Rock
- Grass beats Water, Ground, Rock
- Covers many common types

**Example:** Charizard + Blastoise + Venusaur

#### 2. **Offensive Core**
Focus on speed and power:
- Fast attackers (Speed ≥ 100)
- Strong coverage moves
- Momentum control (U-turn, Volt Switch)

**Example:** Dragapult + Kingamra + Rillaboom

#### 3. **Balanced Core**
Mix of offense and defense:
- Bulky attackers
- Speed control (Tailwind, Trick Room)
- Support moves (Fake Out, Follow Me)

**Example:** Incineroar + Amoonguss + Garchomp

### VGC Team Archetypes

#### **Hyper Offense**
- 6 offensive threats
- High speed or priority moves
- Overwhelm opponent quickly
- **Risk:** Fragile to status and weather

#### **Bulky Offense**
- Mix of power and bulk
- Can take hits while dealing damage
- Most common VGC archetype
- **Balance:** Offensive pressure + survivability

#### **Semi-Trick Room**
- Both fast and slow Pokémon
- Can adapt to opponent's speed
- Trick Room option for slow mode
- **Flexibility:** Multiple win conditions

#### **Weather Teams**
- Sun, Rain, Sand, or Snow-focused
- Weather setters + abusers
- Strong in favorable matchups
- **Commitment:** Requires team dedication

**Learn More:**
- https://www.smogon.com/forums/threads/vgc-team-archetypes.3710891/
- https://victoryroadvgc.com/pokemon-team-archetypes/

---

## 🎯 Usage Statistics & Meta Analysis

### Smogon Usage Stats

**Monthly usage statistics:**
- https://www.smogon.com/stats/

**What to Check:**
- Most used Pokémon
- Move set trends
- Item distribution
- Teammate relationships

**How to Apply:**
- Identify meta threats
- Prepare counters
- Predict opponent strategies

### Pikalytics (VGC-Specific)

**Real VGC tournament data:**
- https://pikalytics.com/

**Features:**
- Usage rates by ranking tier
- Move set statistics
- Tera type trends
- Team compositions

**Use Cases:**
- "What's the most common Charizard set?"
- "Which Tera types are popular for Dragonite?"
- "What items do top players use on Incineroar?"

---

## 🛠️ How This Bot Uses Competitive Data

### 1. **Type Coverage Analysis**

Our `!analyze` command evaluates teams using VGC principles:

```
Offensive Coverage = Can you hit all 18 types super-effectively?
Defensive Synergy = Are your resistances overlapping well?
```

**Based on Smogon's "6 Attacks" principle:**
- A balanced team can threaten most opponents
- Coverage gaps = exploitable weaknesses

**Reference:**
- https://www.smogon.com/dp/articles/intro_comp_pokemon

### 2. **Tera Captain Suggestions**

Our AI suggests Tera types using:
- Common weakness analysis
- VGC meta trends
- Type synergy optimization

**Inspired by:**
- Pikalytics Tera type usage data
- Smogon strategy recommendations

### 3. **Speed Tier Analysis**

Speed tiers matter in VGC:
- **Fast (≥100):** Outspeed most threats
- **Medium (60-99):** Bulk + decent speed
- **Slow (<60):** Trick Room candidates

**Reference:**
- https://www.smogon.com/dex/sv/formats/vgc/
- Speed tier lists by generation

### 4. **Team Efficiency Scoring**

Our 0-100 score considers:
- Point usage optimization (draft efficiency)
- Type coverage (offensive pressure)
- Weakness management (defensive stability)
- Stat balance (versatility)

**Based on VGC Team Building:**
- Balanced teams score higher
- One-dimensional teams score lower

---

## 📖 Recommended Learning Resources

### Beginner Guides

**VGC Beginner's Guide (Official):**
- https://www.pokemon.com/us/strategy/getting-started-in-pokemon-vgc/

**Smogon Introduction to Competitive Pokémon:**
- https://www.smogon.com/dp/articles/intro_comp_pokemon

**YouTube Channels:**
- **CybertronVGC** - World Champion player and analyst
- **WolfeyVGC** - World Champion with detailed guides
- **Moxie Boosted** - Beginner-friendly tutorials

### Advanced Resources

**Smogon Strategy Articles:**
- https://www.smogon.com/articles/

**VGC Analysis:**
- https://victoryroadvgc.com/
- https://trainertower.com/

**Tournament Coverage:**
- https://play.limitlesstcg.com/pokemon (Tournament results)
- https://www.pokemon.com/us/play-pokemon/ (Official events)

---

## 🎮 Applying Resources to Your Draft

### Step 1: Research Your Pokémon

For each Pokémon you draft:

1. **Check Smogon Strategy Dex:**
   ```
   https://www.smogon.com/dex/sv/pokemon/[pokemon-name]/
   ```
   Example: https://www.smogon.com/dex/sv/pokemon/pikachu/

2. **Look at Pikalytics:**
   ```
   https://pikalytics.com/pokedex/ss/[pokemon-name]
   ```

3. **Check Usage Stats:**
   - How popular is this Pokémon?
   - What's the standard set?

### Step 2: Build Your Core

Use team building principles:
- FWG core for balance
- Offensive synergy
- Speed control options
- Support Pokémon

**Tool:** Smogon Team Builder
- https://play.pokemonshowdown.com/teambuilder

### Step 3: Test Coverage

Use our `!analyze` command:
```
!analyze
```

Check for:
- ⚠️ Critical weaknesses (fix with Tera types)
- ⚠️ Coverage gaps (add missing types)
- ⚠️ Speed issues (add fast threats or Trick Room)

### Step 4: Set Tera Captains

Use our `!tera` suggestions:
```
!tera set [pokemon] [type]
```

Consider:
- Smogon strategy recommendations
- Pikalytics Tera type trends
- Your team's specific weaknesses

---

## 🔗 Quick Reference Links

### Official Resources
- **Pokémon VGC:** https://www.pokemon.com/us/play-pokemon/
- **Serebii VGC Rules:** https://www.serebii.net/games/vgc.shtml
- **Bulbapedia Types:** https://bulbapedia.bulbagarden.net/wiki/Type

### Smogon Resources
- **Homepage:** https://www.smogon.com/
- **Strategy Dex:** https://www.smogon.com/dex/
- **Damage Calculator:** https://calc.pokemonshowdown.com/
- **Team Builder:** https://play.pokemonshowdown.com/teambuilder

### Data & Statistics
- **Pikalytics:** https://pikalytics.com/
- **Smogon Usage Stats:** https://www.smogon.com/stats/
- **Trainer Tower:** https://trainertower.com/

### Learning Resources
- **VGC Beginner Guide:** https://www.pokemon.com/us/strategy/getting-started-in-pokemon-vgc/
- **Victory Road VGC:** https://victoryroadvgc.com/
- **CybertronVGC (YouTube):** https://www.youtube.com/@CybertronVGC
- **WolfeyVGC (YouTube):** https://www.youtube.com/@WolfeyVGC

---

## 💡 Bot Features Based on Competitive Theory

| Bot Feature | Competitive Basis | Reference |
|-------------|-------------------|-----------|
| Type Coverage Analysis | Smogon 6 Attacks principle | [Smogon Intro](https://www.smogon.com/dp/articles/intro_comp_pokemon) |
| Tera Captain Suggestions | VGC Tera type optimization | [Pikalytics](https://pikalytics.com/) |
| Speed Tier Analysis | VGC speed control theory | [Smogon Dex](https://www.smogon.com/dex/) |
| Weakness Detection | Competitive team building | [VGC Team Building](https://www.pokemon.com/us/strategy/) |
| Efficiency Scoring | Draft optimization theory | Multiple sources |
| Offensive Coverage | Type chart effectiveness | [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Type) |

---

## 📝 Example: Using Smogon for Team Building

### Scenario: You drafted Charizard

**Step 1:** Check Smogon Strategy Dex
```
URL: https://www.smogon.com/dex/sv/pokemon/charizard/
```

**What You Learn:**
- Common sets: Special Attacker, Tera Blast
- Weaknesses: 4x Rock, 2x Water, 2x Electric
- Counters: Gyarados, Rotom-W, Tyranitar
- Tera types: Grass (removes 4x Rock), Dragon, Ground

**Step 2:** Check Pikalytics
```
URL: https://pikalytics.com/pokedex/ss/charizard
```

**What You Learn:**
- Most common item: Choice Specs
- Most common moves: Heat Wave, Air Slash, Solar Beam
- Most common Tera type: Grass (32%), Dragon (18%)
- Common partners: Torkoal (Sun synergy), Venusaur

**Step 3:** Use Bot Analysis
```
!analyze
```

**Bot Shows:**
- ⚠️ Team is weak to Rock (Charizard + 2 others)
- 💡 Suggested Tera: Grass or Water to cover Rock weakness
- ✅ Good Fire coverage for team

**Step 4:** Make Informed Decision
```
!tera set Charizard Grass
```

**Why:** Removes 4x Rock weakness, adds Grass STAB option

---

## 🎉 Conclusion

This bot combines:
- ✅ Official VGC rules and mechanics
- ✅ Smogon competitive theory
- ✅ Real tournament data (Pikalytics)
- ✅ Automated analysis tools

**Use these resources to:**
- Research Pokémon before drafting
- Optimize your team composition
- Set strategic Tera Captains
- Counter opponent strategies
- Improve your competitive skills

**Remember:** Competitive Pokémon is about knowledge, strategy, and adaptation. Use these resources to stay informed and make better decisions!

---

**Built with competitive Pokémon theory in mind!** 🏆
