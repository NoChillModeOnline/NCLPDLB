# 📨 Direct Message Team Analysis Guide

The bot can send comprehensive team analysis directly to your Discord DMs, keeping your strategy private while providing detailed insights.

---

## 📋 Table of Contents

- [Why Use DM Analysis?](#-why-use-dm-analysis)
- [How to Use](#-how-to-use)
- [What You'll Receive](#-what-youll-receive)
- [Privacy & Permissions](#-privacy--permissions)
- [Comparison: Public vs Private](#-comparison-public-vs-private)
- [Troubleshooting](#-troubleshooting)
- [Examples](#-examples)

---

## 🎯 Why Use DM Analysis?

### Public Analysis (`!analyze`)
- ✅ Visible to everyone in the channel
- ✅ Great for learning and discussion
- ✅ Transparency for league organizers
- ❌ Reveals your strategy to opponents
- ❌ Exposes weaknesses publicly

### Private Analysis (`!dmanalysis`)
- ✅ Sent directly to your DMs
- ✅ **Keeps strategy secret from opponents**
- ✅ Detailed insights without revealing to others
- ✅ Perfect for competitive preparation
- ✅ Includes competitive resources

**Use DM analysis when:**
- 🔒 You want to keep team strategy private
- 🎯 Preparing for a specific opponent
- 💡 Testing different Tera Captain setups
- 🏆 In competitive playoff situations

---

## 📝 How to Use

### Basic Command

```
!dmanalysis
```

**What happens:**
1. Bot confirms in channel: "📨 Preparing team analysis..."
2. Bot sends 7 detailed embeds to your DMs
3. Bot confirms in channel: "✅ Sent 7 analysis embeds via DM!"

### Admin Usage

Admins can send analysis to other players:

```
!dmanalysis @PlayerName
```

**Use cases:**
- Help new players understand their team
- Provide coaching to league members
- Review teams before tournaments

---

## 📊 What You'll Receive

You'll receive **7 detailed embeds** directly in your DMs:

### 1️⃣ Main Analysis Embed
```
📊 Team Analysis: [Your Team Name]
━━━━━━━━━━━━━━━━━━━━
🟢 Team Efficiency: 82/100
📋 Roster Size: 11 Pokémon
💰 Points Used: 118/120
```

### 2️⃣ Type Coverage Analysis
```
🌈 Type Coverage Analysis
━━━━━━━━━━━━━━━━━━━━

📊 Type Distribution:
🔥 Fire: 3x
💧 Water: 2x
⚡ Electric: 2x
...

❌ Missing Types:
Rock, Ghost, Fairy, Poison
```

### 3️⃣ Offensive Coverage
```
⚔️ Offensive Coverage
━━━━━━━━━━━━━━━━━━━━

✅ Coverage Score: 83% of types covered

🚫 Cannot Hit Super-Effectively:
🪨 Rock, 👻 Ghost, 🧚 Fairy
```

### 4️⃣ Team Weaknesses
```
🛡️ Team Weaknesses
━━━━━━━━━━━━━━━━━━━━

⚠️ Critical Weaknesses (4+ Pokémon):
🌍 Ground: Hits 5/11 Pokémon
❄️ Ice: Hits 4/11 Pokémon

⚡ Common Weaknesses (50%+ of team):
🔥 Fire: 6 Pokémon
```

### 5️⃣ Tera Captain Suggestions
```
💡 Tera Captain Suggestions
Strategic Tera types to cover your team's weaknesses
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Cover 🌍 Ground Weakness
Affects 5 Pokémon
Suggested: 💧 Water, 🌿 Grass, ❄️ Ice

🟡 Cover ❄️ Ice Weakness
Affects 4 Pokémon
Suggested: 🔥 Fire, ⚙️ Steel, 🪨 Rock
```

### 6️⃣ Speed Tier Distribution
```
⚡ Speed Tier Distribution
━━━━━━━━━━━━━━━━━━━━

💨 Fast (≥100 Speed) - 3 Pokémon:
Dragapult (142)
Weavile (125)
Jolteon (130)

⚡ Medium (60-99) - 5 Pokémon:
...

📊 Average Speed: 92.3
```

### 7️⃣ Team Summary
```
📝 Team Summary
━━━━━━━━━━━━━━━━━━━━

💪 Strengths:
✅ Excellent type coverage (83%)
✅ Good speed control - 3 fast Pokémon
✅ Balanced offensive threats

⚠️ Areas to Improve:
⚠️ 5 Pokémon weak to Ground
⚠️ Limited Rock coverage

💡 Use these insights to optimize your team!
```

### 8️⃣ Competitive Resources
```
📚 Competitive Resources:
• Smogon Dex: https://www.smogon.com/dex/
• Pikalytics: https://pikalytics.com/
• Damage Calc: https://calc.pokemonshowdown.com/

💡 Next Steps:
• Review your Tera Captain suggestions
• Check coverage gaps and consider trades
• Research matchups on Smogon
• Use !tera set <pokemon> <type> to designate captains
```

---

## 🔒 Privacy & Permissions

### User Privacy

**Your DM analysis is private:**
- ✅ Only you can see the embeds sent to your DMs
- ✅ Other players cannot intercept or view your analysis
- ✅ Bot only confirms in channel that analysis was sent
- ✅ Specific details remain private

**Public confirmation:**
```
✅ Sent 7 analysis embeds to @YourName via DM!
```

This lets others know you received analysis, but **doesn't reveal any details**.

### Discord DM Settings

For the bot to DM you, ensure:

**Settings → Privacy & Safety → Server Privacy Defaults**
- ✅ Enable "Allow direct messages from server members"

**Per-Server Settings:**
1. Right-click server icon
2. Privacy Settings
3. ✅ Enable "Direct Messages"

### Admin Permissions

**Regular users:**
- Can only use `!dmanalysis` on themselves
- Keeps competitive integrity

**Administrators:**
- Can use `!dmanalysis @Player` on anyone
- Useful for coaching and help
- Use responsibly to avoid unfair advantages

---

## ⚖️ Comparison: Public vs Private

| Feature | `!analyze` (Public) | `!dmanalysis` (Private) |
|---------|---------------------|-------------------------|
| **Visibility** | Everyone in channel | Only recipient |
| **Embeds** | 7 detailed embeds | 7 detailed embeds + resources |
| **Best For** | Learning, discussion | Competitive prep |
| **Strategy Protection** | ❌ Reveals weaknesses | ✅ Keeps secrets |
| **Tera Suggestions** | ✅ Included | ✅ Included + links |
| **Coaching** | ✅ Public teaching | ✅ Private guidance |
| **Competitive Resources** | ❌ Not included | ✅ Smogon, Pikalytics links |
| **Speed** | Instant (same channel) | Instant (via DM) |

### When to Use Each

**Use `!analyze` (public) when:**
- Teaching team building concepts
- Discussing strategy with league
- Demonstrating analysis features
- Transparency is important
- Not in competitive matches

**Use `!dmanalysis` (private) when:**
- Preparing for specific opponent
- Testing Tera Captain strategies
- Identifying weaknesses privately
- Competitive tournament prep
- Want to keep strategy secret

---

## 🐛 Troubleshooting

### Error: "Cannot send DM"

**Full message:**
```
❌ Cannot send DM to @YourName. They may have DMs disabled.
💡 @YourName, enable DMs from server members in Privacy Settings, then try again.
```

**Solution:**

1. **Open Discord Settings**
   - Click ⚙️ gear icon (bottom left)

2. **Navigate to Privacy & Safety**
   - Left sidebar → "Privacy & Safety"

3. **Enable Server DMs**
   - Scroll to "Server Privacy Defaults"
   - ✅ Check "Allow direct messages from server members"
   - Click "Done"

4. **Per-Server Override (if needed)**
   - Right-click server icon
   - "Privacy Settings"
   - ✅ Enable "Direct Messages"

5. **Try Command Again**
   ```
   !dmanalysis
   ```

### Error: "Only administrators can send analysis to other players"

**Cause:** You tried to use `!dmanalysis @OtherPlayer` without admin permissions.

**Solution:** Only use the command on yourself, or ask an admin for help:
```
!dmanalysis
```

### DMs Not Arriving

**Check:**
1. ✅ DM permissions enabled (see above)
2. ✅ Bot is online (green dot)
3. ✅ You typed command correctly
4. ✅ Not in bot's DM channel already (check DM list)

**Still not working?**
- Try `!analyze` in channel (public) as fallback
- Contact server admin
- Check bot logs for errors

---

## 📖 Examples

### Example 1: Self-Analysis

**Command:**
```
!dmanalysis
```

**Channel Response:**
```
📨 Preparing team analysis for @Alice...
✅ Sent 7 analysis embeds to @Alice via DM!
```

**Your DMs:**
```
# 📊 Your Team Analysis

Here's a comprehensive analysis of your team in **Pokémon Draft League**:

[7 detailed embeds follow]

📚 Competitive Resources:
[Links to Smogon, Pikalytics, etc.]
```

### Example 2: Admin Helping Player

**Command (by admin):**
```
!dmanalysis @NewPlayer
```

**Channel Response:**
```
📨 Preparing team analysis for @NewPlayer...
✅ Sent 7 analysis embeds to @NewPlayer via DM!
```

**NewPlayer's DMs:**
```
# 📊 Your Team Analysis

Here's a comprehensive analysis of your team...
[Full analysis follows]
```

### Example 3: Pre-Match Strategy

**Scenario:** You're facing Bob in Week 3. You want to prepare privately.

**Step 1:** Get your own analysis
```
!dmanalysis
```

**Step 2:** Review weaknesses in DMs
- Identify critical weaknesses
- Note Tera Captain suggestions
- Check speed tiers vs opponent

**Step 3:** Set strategic Tera types
```
!tera set Pikachu Water
!tera set Rotom Grass
!tera set Marowak Fire
```

**Step 4:** Scout opponent (public)
```
!team @Bob
```

**Step 5:** Plan matchup strategy
- Use Smogon/Pikalytics links from DM
- Prepare counter-picks
- Set battle plan

**Advantage:** Your strategy remains private while you gather intelligence!

---

## 🎓 Advanced Tips

### 1. Save Your Analysis

**Discord lets you save DMs:**
1. Right-click any embed
2. "Save Image"
3. Keep for future reference

**Or:**
1. Take screenshots of key embeds
2. Create strategy notes
3. Share with trusted teammates (outside Discord)

### 2. Compare Over Time

**Track improvements:**
```
Week 1: !dmanalysis → Efficiency: 62/100
[Make trades and adjustments]
Week 3: !dmanalysis → Efficiency: 78/100
```

### 3. Pre-Draft Research

**Before drafting Pokémon:**
1. Use competitive resources links
2. Research on Smogon Dex
3. Check Pikalytics usage data
4. Plan Tera Captains early

**After drafting:**
```
!dmanalysis
```

Review and adjust Tera Captains based on actual team composition.

### 4. Competitive Scouting

**Legal scouting:**
- ✅ Public team views: `!team @Opponent`
- ✅ Public Tera Captains: `!tera show @Opponent`
- ✅ Match history and standings

**Private preparation:**
- ✅ Your own `!dmanalysis`
- ✅ Counter-strategy planning
- ✅ Matchup research

**Unfair advantages (don't do this):**
- ❌ Admin abusing `!dmanalysis @Opponent` before matches
- ❌ Sharing opponent's private analysis
- ❌ Colluding with admins for intelligence

---

## 📚 Related Commands

- `!analyze` - Public team analysis
- `!tera show` - View your Tera Captains
- `!tera set <pokemon> <type>` - Designate Tera Captain
- `!team @Player` - View opponent roster (public)
- `!roster` - View your own roster

---

## 💡 Best Practices

### For Players

1. **Use DM analysis regularly**
   - Check after trades
   - Review before important matches
   - Track improvement over season

2. **Keep strategy private**
   - Don't screenshot and share your DM analysis
   - Use public `!analyze` for discussion only
   - Protect competitive advantage

3. **Act on insights**
   - Review Tera Captain suggestions
   - Address coverage gaps with trades
   - Research matchups on Smogon

### For Admins

1. **Use responsibly**
   - Only send analysis to help players learn
   - Don't abuse admin access for competitive intel
   - Maintain competitive integrity

2. **Coaching use**
   - Send DM analysis to new players
   - Help understand team building
   - Guide Tera Captain selection

3. **Transparency**
   - Document when you use admin commands
   - Avoid conflicts of interest
   - Maintain league fairness

---

## 🆘 Support

**Issues with DM analysis?**

1. Check this guide's troubleshooting section
2. Verify DM permissions
3. Try `!analyze` as fallback
4. Contact server admin
5. Report bugs on GitHub (if applicable)

**Questions?**
- Ask in league Discord server
- Check COMPETITIVE_RESOURCES.md
- Review bot documentation

---

**Built for competitive strategy and player privacy!** 🔒
