# Feature Landscape

**Domain:** Competitive Pokemon RL — knowledge injection into existing self-play bot
**Researched:** 2026-03-17
**Overall confidence:** MEDIUM (core encoding guidance HIGH; BC pipeline MEDIUM; ROI ranking LOW-MEDIUM)

---

## Table Stakes

Features users expect in a competitive Pokemon RL agent. Missing = agent plays obviously suboptimally.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Type effectiveness per move | Core damage multiplier; without it agent cannot distinguish STAB super-effective from resisted | Low | Already planned — 4 floats |
| HP fractions (both sides) | Primary survival signal | Low | Already present |
| Active species IDs | Determines typing, stat spread, learnset | Low | Already present |
| Status conditions | Burn/para/sleep materially change action value | Low | Already present |
| Stat boosts (+/-6) | Dragon Dance, Swords Dance, Intimidate — large EV on offense/defense calc | Low | Already present |
| Weather / terrain | Affects type power, speed, damage; e.g. rain doubles Water | Low | Already present |

---

## Differentiators (High-ROI Next Steps After Type Effectiveness)

Ranked by expected sample-efficiency gain vs encoding cost.

### 1. Speed Tier Comparison (HIGH confidence recommendation)

**Value:** Determines whether your active mon moves first. Speed determines whether you KO before taking damage — arguably the most impactful single unknown in current obs.

**Encoding:**
```
speed_tier_flag = clamp(own_speed / opp_speed, 0.25, 4.0)
then log2(speed_tier_flag) → range [-2, +2], normalize to [0, 1] via (val + 2) / 4
```
This gives 1 float. A simpler alternative: `own_faster = 1.0 if own_speed > opp_speed else 0.0` (binary).

Recommended: binary flag + raw ratio as two floats. Total: 2 floats.

**Why before abilities/items:** Speed is observable from game state without hidden info. No lookup needed — poke-env exposes `base_stats["spe"]` directly.

---

### 2. STAB Flag Per Move (HIGH confidence)

**Value:** Agent currently cannot distinguish same-type attack bonus. STAB is +50% damage and is deterministic once species is known.

**Encoding:** 4 binary floats (one per move slot): `1.0 if move.type == mon.type1 or move.type == mon.type2 else 0.0`

Cost: 4 floats. Pairs naturally with type effectiveness already planned.

---

### 3. Remaining Team Size (Both Sides) (MEDIUM confidence)

**Value:** 6v6 vs 6v1 are entirely different strategic situations. Already partially present via team HP slots, but an explicit `alive_count / 6` float is more learnable than inferring from HP array.

**Encoding:** `alive_own = sum(1 for hp in team_hp_own if hp > 0) / 6.0` — 1 float each side. Total: 2 floats.

---

### 4. Opponent Boosts (MEDIUM confidence)

**Value:** Knowing opponent has +2 Atk means you should switch, not attack. Current obs has own boosts but not opponent boosts. Opponent's 6 stat boosts encoded identically to own: `(boost + 6) / 12.0` each.

**Encoding:** 6 floats, normalized to [0, 1]. Total: 6 floats.

**Note:** May already be visible in poke-env `battle.opponent_active_pokemon.boosts` dict.

---

### 5. Fainted Slot Indicators (MEDIUM confidence)

**Value:** More direct signal than HP=0 in the team HP array. Helps agent reason about late-game scenarios.

**Encoding:** Already inferrable from team HP array. Skip — zero-ROI duplicate.

---

### 6. Ability Flags (LOW confidence, deferred)

**Value:** Abilities like Intimidate, Levitate, Sand Rush, Prankster significantly alter damage calc and speed. However, encoding is complex:

- ~300 relevant abilities in Gen 9
- Need per-ability binary flags or learned embeddings
- Self-play agent may not observe opponent ability reliably without damage inference

**Recommendation:** Defer until after type effectiveness + speed tier + STAB are validated. Revisit with embedding approach (ability_id → 8-dim embedding) rather than one-hot.

---

### 7. Item Awareness (LOW confidence, deferred)

**Value:** Choice Band, Life Orb, Leftovers, Eviolite change effective bulk/power. Items are often hidden.

**Problem:** Items are unknown until revealed via damage calc or move lock. Encoding unknown items as 0.0 creates false confidence. Better to use a revealed-flag pattern:

```
item_id (0 = unknown), item_revealed (binary)
```

**Recommendation:** Defer. Item inference from BC data is feasible but requires significant engineering.

---

## Anti-Features

Features to explicitly NOT build in this milestone.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Full damage calculator in obs | Adds 4+ floats of redundancy once type_eff + STAB + boosts are present; DNN learns this implicitly | Trust the network to combine type_eff * base_power * STAB |
| Species one-hot encoding | 1000-dim sparse vector; catastrophic dimensionality for small net | Keep species_id as integer ID, use embedding lookup if needed |
| Move PP tracking | Rarely decisive in competitive; adds 4 floats of low-signal noise | Omit until analysis shows PP-relevant scenarios are common |
| Weather turn counter | Already implicit in weather flag + turn counter interaction | No new float needed |
| Megaform / Z-move / Tera flags before core features | Complex state management; only relevant after core obs is solid | Add after speed tier and STAB validated |

---

## Type Effectiveness Normalization (Current Sprint)

**Question:** Raw multiplier (0/0.25/0.5/1/2/4) vs log scale vs clamped 0–1?

### Recommendation: Log2 normalized to [0, 1] — MEDIUM confidence

**Rationale:** Raw multipliers have unequal spacing: the gap 1→2 and 2→4 are identical in log space but 3x different in raw space. Neural nets with ReLU activations learn better from uniformly-spaced inputs.

**Encoding:**
```python
MULT_TO_LOG_NORM = {
    0.0:  0.0,   # immune — special case, encode as 0 (hard floor)
    0.25: 0.125, # log2(0.25) = -2, mapped via (log2 + 3) / 6
    0.5:  0.25,  # log2(0.5)  = -1
    1.0:  0.5,   # log2(1.0)  =  0
    2.0:  0.75,  # log2(2.0)  = +1
    4.0:  1.0,   # log2(4.0)  = +2
}
```

Formula: `0.0 if mult == 0 else (log2(mult) + 2) / 4` maps [-2, +2] → [0, 1], with immunity hard-coded to 0.

**Why not raw multiplier:** Range 0–4 with unequal spacing. Network must learn that 4.0 is special.

**Why not clamped 0–1:** Loses the distinction between 2x and 4x, which is strategically critical (4x = OHKO territory).

**Alternative (simpler, acceptable):** Two binary flags per move: `is_super_effective` (mult >= 2), `is_resisted` (mult <= 0.5). 8 floats total. Lower information density but very learnable. Use if log norm causes training instability.

**poke-env API:**
```python
from poke_env.data import GenData
type_chart = GenData.from_gen(9).type_chart
effectiveness = battle.opponent_active_pokemon.damage_multiplier(move)
```
`damage_multiplier()` already accounts for dual typing and returns the combined float.

---

## Behavioral Cloning from Showdown Replays

### Replay Log → Obs+Action Mapping

**Source:** Pokemon Showdown `.log` format. The Metamon paper (arxiv 2504.04395) reconstructed 475k+ first-person demonstrations from spectator replay logs going back to 2014.

**Key extraction challenge:** Replays are spectator-perspective (both sides visible). You must reconstruct the first-person view — agent knows only what it could observe during its turn.

**Obs features that map cleanly from replay logs:**

| Replay Data | Obs Field | Notes |
|-------------|-----------|-------|
| `|switch|p1a: Garchomp` | species_id | Direct species name → dex ID lookup |
| `|-damage|p2a: Charizard|50/100` | hp_pct | Parse `current/max` |
| `|move|p1a: Garchomp|Earthquake` | Action label (move slot index) | Must map move name → slot in team's moveset |
| `|-status|p2a: Chansey|brn` | opponent_status | Direct |
| `|-weather|SunnyDay` | weather_id | Direct |
| `|-boost|p1a: Dragapult|atk|2` | own_boosts[atk] | Direct |
| `|turn|5` | turn | Direct |
| `|switch|p1a: ...` as action | Action label (switch slot) | Switch actions need separate label space |

**Features NOT reliably extractable from replays:**

- Items (only revealed if KO'd or activated — partial)
- Abilities (only revealed if triggered — partial)
- Full team composition before reveal (switch-in order reveals gradually)

**Action space mapping for BC:**

The current bot's action space likely maps move slots 0-3 and switch slots 4-9. Replay actions need the same mapping. The move name in the log must match to the slot in the *agent's current team loadout*, which requires knowing the team. Showdown replays include team info in `|teampreview` lines.

**Recommended BC pipeline:**

1. Parse replays with `showdown-replay-parser` or custom log parser
2. Reconstruct per-turn obs vector using only information visible to player 1 at that turn
3. Extract action as (move_slot or switch_slot) integer
4. Filter: only include turns where the agent made a choice (skip forced switches, struggle)
5. Store as `(obs_vector, action_int)` pairs in numpy arrays
6. BC training: supervised cross-entropy on action logits, same network as RL agent
7. Curriculum: BC pretrain for N steps, then switch to self-play PPO/DQN with BC regularization

**Confidence:** MEDIUM. The Metamon paper validates this pipeline at scale. The specific mapping to a 44-dim obs requires careful implementation. The main risk is replay parser correctness — wrong turn reconstruction will produce poisoned training data.

---

## MaxDamagePlayer Curriculum

**Role:** Bridge between random-agent curriculum (too easy) and self-play (too hard early). MaxDamagePlayer always picks the highest base-power move, ignoring type effectiveness.

**Obs features needed:** No change to obs required. MaxDamagePlayer exposes weaknesses in the agent's type-effectiveness reasoning — exactly what the new 4 floats are designed to address.

**Sequencing recommendation:**

```
Stage 1: vs MaxDamagePlayer (no type eff obs)    — teaches HP management, switching basics
Stage 2: vs MaxDamagePlayer (with type eff obs)  — validates type eff floats are learnable
Stage 3: BC pretraining on replays               — injects human strategy priors
Stage 4: Self-play PPO                           — refines via competitive pressure
```

Stage 2 is a useful ablation: if win-rate vs MaxDamagePlayer doesn't improve with type_eff obs added, the encoding is wrong or the network isn't using it.

---

## Feature Dependencies

```
species_id → type_effectiveness (need species type to calc multiplier)
species_id → STAB flag (need species type)
species_id → speed_tier_comparison (need base speed stat)
type_effectiveness + STAB + base_power → implicit damage estimate (no extra float needed)
team HP slots → alive_count (derivable, low-ROI to add separately)
```

---

## MVP Recommendation for This Milestone

Prioritize (in order):

1. **Type effectiveness (4 floats, log2 normalized)** — already planned, highest ROI, unblocked
2. **STAB flag per move (4 floats, binary)** — pairs naturally, trivial to add alongside type_eff
3. **Speed tier comparison (2 floats: binary + ratio)** — highest-ROI feature not yet planned
4. **MaxDamagePlayer curriculum** — no obs change, validates type_eff encoding

Defer to next milestone:

- **BC from replays** — correct but requires replay parser infrastructure; don't block on it
- **Opponent boosts** — medium ROI, add after speed tier validated
- **Ability/item awareness** — low confidence, high complexity

**Total obs delta for MVP:** 44 + 4 (type_eff) + 4 (STAB) + 2 (speed) = OBS_DIM=54

---

## Published Results on Pokemon RL Observation Space

| Paper / Source | Key Finding | Confidence |
|----------------|-------------|------------|
| Metamon (arxiv 2504.04395, 2025) | 475k human replays + offline RL + BC → top 10% ladder on Showdown. Used Transformer, not fixed obs vector. Key: first-person replay reconstruction. | HIGH |
| poke-env official example | SimpleRLPlayer baseline uses move base_power + damage_multiplier (combined type_eff + STAB) as obs features. Validates both as essential. | HIGH |
| Ivison 2021 blog | Small PPO agent with type effectiveness in obs outperforms without in early training. Anecdotal but consistent with theory. | LOW |
| drubinstein/pokerl docs | Game-version RL (Gen 1 walkthrough), not competitive — not directly applicable | N/A |

**Gap:** No published ablation study specifically measuring type_eff vs STAB vs speed_tier contribution to sample efficiency in Gen 8/9 competitive format. ROI ranking above is based on domain knowledge + poke-env community practice, not measured results.

---

## Sources

- [Human-Level Competitive Pokemon via Scalable Offline RL with Transformers (Metamon, 2025)](https://arxiv.org/abs/2504.04395)
- [poke-env RL with Gymnasium wrapper — official example](https://poke-env.readthedocs.io/en/stable/examples/rl_with_gymnasium_wrapper.html)
- [poke-env GitHub](https://github.com/hsahovic/poke-env)
- [Metamon project page](https://metamon.tech/)
- [Reinforcement Learning with Pokemon — Hamish Ivison 2021](https://ivison.id.au/2021/08/02/pokerl.html)
