# 🎮 Pokémon Draft League - Rules & Guide

Welcome to the Pokémon Draft League! This guide will help you understand all the rules, systems, and commands for participating in the league.

---

## 📋 Table of Contents

- [Welcome & Overview](#-welcome--overview)
- [Draft System](#-draft-system)
- [Tera Captain System](#-tera-captain-system)
- [Team Management & Trades](#-team-management--trades)
- [Battle Rules](#️-battle-rules)
- [Discord Commands Reference](#-discord-commands-reference)
- [FAQ](#-faq)

---

## 👋 Welcome & Overview

The Pokémon Draft League is a competitive format where coaches draft their own team of Pokémon and compete against each other throughout a season. Here's what makes it special:

- **Point-Based Draft**: You have a budget to build your team strategically
- **Tera Captains**: Special Pokémon that can change their type
- **Weekly Battles**: Compete for wins and climb the standings
- **Trading System**: Improve your team throughout the season

### Getting Started

1. **Register**: Use `!league register "Your Team Name" <logo_url>` to join
2. **Draft**: Participate in the draft to build your team (10-12 Pokémon)
3. **Set Tera Captains**: Choose your 3 Tera Captains and their types
4. **Battle**: Face off against other coaches each week
5. **Trade**: Make strategic trades to improve your roster

---

## 🎲 Draft System

### Point Budget

- **Total Points**: Each coach has **120 points** to spend
- **Team Size**: You must draft between **10-12 Pokémon**
- **Pokémon Costs**: Each Pokémon has a point cost based on their tier/strength
- **Strategy**: Balance powerful expensive Pokémon with budget-friendly options

### Draft Format

**Snake Draft** (Default):
- Draft order reverses each round
- Example: Round 1 (1→8), Round 2 (8→1), Round 3 (1→8), etc.

**Draft Rules**:
- Each pick has a **5-minute timer** ⏱️
- If you miss your turn, the next player can pick (you can pick later when you return)
- Once a Pokémon is picked, no one else can draft it
- You cannot exceed your 120-point budget

### Species Clause

You **cannot have two Pokémon with the same National Pokédex number** on your team. This means:
- ✅ You can have Pikachu
- ❌ You cannot have both Pikachu AND Raichu (same evolution line is fine, just not duplicates)

### Form-Variant Pokémon

These Pokémon have multiple forms, and you can access **ALL forms** but can only bring **1 form per battle**:

- Pikachu (various cap forms)
- Basculin (Red-Striped, Blue-Striped, White-Striped)
- Oricorio (Baile, Pom-Pom, Pa'u, Sensu)
- Toxtricity (Amped, Low Key)
- Indeedee (Male, Female)
- Basculegion (Male, Female)
- Oinkologne (Male, Female)
- Squawkabilly (Green, Blue, Yellow, White)
- Tatsugiri (Curly, Droopy, Stretchy)
- Meowstic (Male, Female)

**Example**: If you draft Oricorio, you can use any of its 4 forms, but you must choose 1 form for each battle.

---

## ⚡ Tera Captain System

### What are Tera Captains?

Tera Captains are special designated Pokémon on your team that can **Terastallize** to any type you choose during battles. This is a powerful strategic tool!

### Tera Captain Rules

You must have **exactly 3 Tera Captains** on your team with these restrictions:

1. **Point Restriction**: Only Pokémon with **13 points or less** can be Tera Captains
   - ✅ Pikachu (8 pts) can be a Tera Captain
   - ❌ Charizard (15 pts) cannot be a Tera Captain

2. **Total Points Cap**: The combined cost of all 3 Tera Captains must be **≤ 25 points**
   - ✅ Pikachu (8) + Rotom (11) + Talonflame (10) = 29 pts ❌ TOO HIGH
   - ✅ Pikachu (8) + Rotom (11) + Marowak (6) = 25 pts ✅ PERFECT

3. **Tera Type**: Each Tera Captain can Terastallize to any of the **19 Tera types**:
   - 18 Standard Types: Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy
   - 1 Special Type: **Stellar** ✨ (introduced in Scarlet/Violet)

### Setting Tera Captains

Use the `!tera` commands to manage your Tera Captains:

```
!tera set Pikachu Dragon     → Makes Pikachu a Dragon Tera Captain
!tera change Pikachu Steel   → Changes Pikachu's Tera type to Steel
!tera remove Pikachu         → Removes Pikachu as a Tera Captain
!tera show                   → View your Tera Captains
!tera show @Player           → View another player's Tera Captains
!tera list                   → View all Tera Captains in the league
!tera types                  → See all 19 valid Tera types
```

### Strategy Tips

- **Coverage**: Choose Tera types that cover your team's weaknesses
- **Surprise Factor**: Unexpected Tera types can catch opponents off-guard
- **STAB Bonus**: Terastallizing to a Pokémon's existing type boosts that type's moves
- **Stellar Type**: The Stellar type is unique and works differently than standard types

---

## 🔄 Team Management & Trades

### Viewing Teams

```
!team @Player       → View another player's team
!roster             → View your own team (shortcut)
!teams all          → List all teams in the league
```

### Trading System

You can trade Pokémon with other coaches throughout the season, with some restrictions:

#### Trade Limits by Week

- **Week 1**: **Unlimited trades** allowed 🔓
  - Build your ideal team through multiple trades
  - Great time to fix draft mistakes or try new strategies

- **Weeks 2-5**: **Maximum 5 total trades** per coach 🔒
  - Make your trades count!
  - Each coach can only make 5 trades during this period

#### Trade Timing

When a trade takes effect depends on **which day you propose it**:

**Immediate Trades** (Sunday, Monday, Tuesday):
- Trade takes effect **immediately**
- You can use your new Pokémon right away

**Delayed Trades** (Wednesday, Thursday, Friday, Saturday):
- Trade takes effect **next week**
- Prevents last-minute roster changes before matches

### Trade Commands

```
!trade propose @Player YourPokemon for TheirPokemon
   → Example: !trade propose @Alice Pikachu for Charizard

!trade accept      → Accept a pending trade offer
!trade reject      → Reject a pending trade offer
!trade history     → View your trade history
!trade history @Player  → View another player's trades
```

### Trade Validation

The bot will automatically check:
- ✅ Both players own the Pokémon being traded
- ✅ Trade limits haven't been exceeded (Weeks 2-5)
- ✅ Point totals remain valid after trade
- ✅ Both players still meet 10-12 Pokémon requirement

---

## ⚔️ Battle Rules

### Battle Format

- **Format**: Double Battles (2v2), Best-of-Three sets
- **Team Submission**: Bring **6 Pokémon**, choose **4 for each battle**
- **Platform**: Nintendo Switch ONLY (no Pokémon Showdown battles allowed)
- **Consistency**: You must use the same 6 Pokémon for all 3 battles in a set

### Pre-Battle Requirements

1. **Submit Builds**: Before each week's battle, submit your team builds via **Pokémon Showdown** to the judges
   - Include: Pokémon, nature, items, IVs/EVs, abilities, shiny status
   - Use the same build for all 3 battles

2. **Record Preparation**: Have pen/paper, phone notes, or video recording ready to track KOs

### During Battle

- You can change which 4 Pokémon you bring for each of the 3 battles
- You must use your designated Tera Captains if you want to Terastallize
- Tera Captains can Terastallize to their chosen Tera type
- Record all KOs (which Pokémon KO'd which opponent)

### After Battle

1. **Record Results**: Use `!record @Opponent 2-1` to log your match result
2. **Post Replay**: Share battle replay link in the appropriate Discord channel
3. **Report KOs**: Submit KO data (who KO'd whom) for stats tracking

### Battle Clauses

These clauses are enforced in all battles:

- **Species Clause**: No duplicate National Dex numbers
- **Sleep Clause**: Only one opponent Pokémon asleep at a time
- **Evasion Clause**: No evasion-boosting items/moves/abilities
- **OHKO Clause**: No Fissure, Guillotine, Horn Drill, Sheer Cold
- **Moody Clause**: Moody ability banned
- **Endless Battle Clause**: No infinite stalling tactics
- **Baton Pass Clause**: Baton Pass move banned
- **Item Clause**: Each Pokémon must hold different items

### Banned Items

- All unreleased Scarlet/Violet items

### Penalties

**Discrepancy in Records**: If there's a mismatch between what you submitted and what you used:
- Result: Match **disqualification** + removal from competition
- This is taken very seriously to maintain competitive integrity!

---

## 💬 Discord Commands Reference

### League Commands

#### Setup & Initialization
```
!league init "League Name"           → Initialize new league (admin)
!league register "Team Name" <url>   → Register as a coach
!league start                        → Start season & create channels (admin)
```

#### Coach Management
```
!league addcoach @User               → Add coach to league (admin)
!league removecoach @User            → Remove coach (preserves history) (admin)
```

#### Maintenance
```
!league diagnose                     → Run error diagnostics (admin)
!league reset                        → Reset entire league (admin)
```

### Draft Commands

```
!draft start                         → Start a new draft (admin)
!draft pick PokemonName              → Make your draft pick
!draft budget                        → Check your remaining points
!draft budget @Player                → Check another player's points
!draft status                        → View current draft status
!draft undo                          → Undo last pick (admin)
!draft end                           → End the draft (admin)
```

### Tera Captain Commands

```
!tera set PokemonName Type           → Designate a Tera Captain
!tera change PokemonName NewType     → Change Tera type
!tera remove PokemonName             → Remove Tera Captain status
!tera show                           → View your Tera Captains
!tera show @Player                   → View another player's Tera Captains
!tera list                           → View all league Tera Captains
!tera types                          → Show all 19 valid Tera types
```

### Team Commands

```
!team @Player                        → View a player's team
!roster                              → View your own team
!teams all                           → List all teams
```

### Trade Commands

```
!trade propose @Player Your for Their → Propose a trade
!trade accept                        → Accept pending trade
!trade reject                        → Reject pending trade
!trade history                       → View your trades
!trade history @Player               → View another player's trades
```

### Battle Commands

```
!record @Opponent Score              → Record match result
   Example: !record @Alice 2-1       → You won 2-1

!schedule                            → View your scheduled matches
!schedule Week                       → View matchups for a week
!standings                           → View league standings
!matchups Week                       → View all matchups for a week
```

### Stats Commands

```
!stats PokemonName                   → View Pokémon usage stats
!usage                               → View most/least used Pokémon
!tiers                               → View Pokémon tier breakdown
!playerstats @Player                 → View player statistics
```

---

## ❓ FAQ

### Draft Questions

**Q: What happens if I go over 120 points?**
A: The bot won't let you pick a Pokémon that would exceed your budget. You'll get an error message.

**Q: Can I draft fewer than 10 Pokémon?**
A: No, you must draft at least 10 Pokémon. The bot will enforce this.

**Q: What if I miss my pick during the draft?**
A: The draft moves to the next player. You can make your pick later when you return, and the current player's turn will pause.

### Tera Captain Questions

**Q: Can I have fewer than 3 Tera Captains?**
A: No, you must have exactly 3 Tera Captains. Not 2, not 4 - exactly 3.

**Q: My Pokémon costs 14 points. Can it be a Tera Captain?**
A: No, only Pokémon with 13 points or less can be Tera Captains.

**Q: Can I change my Tera Captains after the season starts?**
A: You can change Tera types anytime, but changing which Pokémon are Tera Captains may have restrictions (ask admin).

**Q: What's the difference between Stellar and other types?**
A: Stellar is a special Tera type introduced in Scarlet/Violet. It works differently than the 18 standard types. Check Bulbapedia or Serebii for details!

### Trading Questions

**Q: Can I trade during Week 1?**
A: Yes! Week 1 has unlimited trades.

**Q: I'm in Week 3 and already made 5 trades. Can I trade again?**
A: No, you've reached the maximum of 5 trades for Weeks 2-5.

**Q: When does my trade take effect?**
A: If you trade Sunday-Tuesday, it's immediate. If you trade Wednesday-Saturday, it takes effect next week.

**Q: Can I trade a Tera Captain?**
A: Yes, but you'll need to designate a new Tera Captain if you do (you must always have exactly 3).

### Battle Questions

**Q: Can I battle on Pokémon Showdown?**
A: No, all battles must be on Nintendo Switch.

**Q: What happens if I bring the wrong Pokémon to a battle?**
A: If it doesn't match your submitted build, you could be disqualified and removed from the league.

**Q: Do I have to record KOs?**
A: Yes, KO data is required for stats tracking. Use pen/paper, phone notes, or video recording.

**Q: Can I change my team between battles in a set?**
A: You can change which 4 of your 6 Pokémon you bring, but you must use the same 6 Pokémon for all 3 battles.

### Technical Questions

**Q: How do I get my private channel?**
A: After the draft is complete, the admin uses `!league start` and you'll automatically get a private channel with your roster.

**Q: Can I see other players' teams?**
A: Yes! Use `!team @Player` to view anyone's roster (no secrets here!).

**Q: What if the bot isn't responding?**
A: Check that you're using the correct command prefix (`!`). If it still doesn't work, contact an admin.

**Q: Where is my team data stored?**
A: All data is stored in a Google Sheet that admins can access. This makes it easy to view and edit if needed.

---

## 🎯 Quick Reference

### Must-Know Numbers
- **120 points** - Your draft budget
- **10-12 Pokémon** - Required team size
- **3 Tera Captains** - Exactly 3, no more, no less
- **≤13 points** - Max cost for Tera Captains
- **≤25 points** - Max total for all 3 Tera Captains
- **5 trades** - Max trades in Weeks 2-5
- **6 Pokémon** - Bring to battle
- **4 Pokémon** - Actually use in battle

### Important Reminders
- ✅ Submit builds to judges BEFORE battles
- ✅ Record KOs during battles
- ✅ Post replays after battles
- ✅ Use the bot to record results
- ❌ No Showdown battles
- ❌ No switching builds mid-match
- ❌ No exceeding trade limits

---

## 📞 Support

If you have questions not covered in this guide:
1. Ask in the league Discord server
2. Contact a league admin
3. Use `!help` to see available commands

Good luck, and may the best coach win! 🏆

---

*This guide was created for the Pokémon Draft League Bot. Last updated: 2026*
