# Domain Pitfalls

**Domain:** RL Pokemon battle bot — type effectiveness obs, curriculum opponent, BC pre-training
**Researched:** 2026-03-17
**Milestone scope:** SUBSEQUENT — adding to existing poke-env PPO bot

---

## Critical Pitfalls

Mistakes that cause rewrites, silent training failures, or irrecoverable model state.

---

### Pitfall 1: OBS_DIM Checkpoint Mismatch After Obs Expansion

**What goes wrong:** Loading a saved SB3 PPO `.zip` checkpoint after expanding the observation
vector (adding type effectiveness features) raises a shape mismatch error or silently loads
wrong weights because the first-layer weight tensor no longer matches the new input dimension.
SB3's `model.load()` does NOT gracefully handle observation space changes — it will either
crash or load a model that produces garbage outputs.

**Why it happens:** SB3 serializes the `observation_space` shape into the checkpoint. When you
change `OBS_DIM` (e.g., from 10 to 26), the saved network's input layer has the old width.
`OBS_DIM_DOUBLES` is a separate constant and will also be wrong if doubles obs are derived from
the same feature expansion.

**Consequences:** Training appears to start but the policy is randomly initialized (old
checkpoint silently discarded) or crashes immediately. Hours of prior training lost if not
caught.

**Prevention:**
1. Never change `OBS_DIM` in-place on a live checkpoint. Branch the experiment.
2. Use `custom_objects` in `PPO.load()` to override the observation space:
   ```python
   model = PPO.load(
       "checkpoint.zip",
       env=new_env,
       custom_objects={"observation_space": new_env.observation_space}
   )
   ```
   This loads all shared weights and randomly initializes only the first layer — better than
   starting from scratch.
3. For a cleaner transfer: extract policy network weights manually, zero-pad the first-layer
   weight matrix to the new input size, then inject via `model.policy.load_state_dict()`.
4. Update `OBS_DIM_DOUBLES` in the same commit as `OBS_DIM` — search for every constant that
   derives from it before merging.

**Detection:** Add an assertion at env instantiation time:
```python
assert env.observation_space.shape[0] == OBS_DIM, \
    f"OBS_DIM mismatch: env={env.observation_space.shape[0]} constant={OBS_DIM}"
```

---

### Pitfall 2: Unknown Opponent Type Producing NaN / Wrong Effectiveness

**What goes wrong:** When the opponent's Pokemon has not revealed its type (e.g., first turn,
before any identifying moves), `opponent_active_pokemon.types` in poke-env returns `(None,)`
or a partial tuple. Passing `None` into a type-effectiveness lookup crashes or returns 0,
which is indistinguishable from a genuine immunity (0x). The observation vector then contains
either NaN or a false immunity signal.

**Why it happens:** poke-env's `Pokemon.types` is populated from the move used or the species
data. In formats where the species is known (standard OU), the type is available immediately
from the Pokedex. In Random Battle or when a Pokemon has not yet been sent out, types may be
partially unknown. The real trap is **Tera type**: after Terastallization, the defensive type
changes entirely and `types` will reflect the new Tera type, not the original.

**Consequences:** The agent learns a biased policy that exploits false immunities or avoids
moves that are actually effective.

**Prevention:**
1. Always guard the lookup:
   ```python
   def get_type_effectiveness(move_type, defender):
       if defender is None or any(t is None for t in defender.types):
           return 1.0  # neutral fallback — least biased unknown encoding
       return calculate_effectiveness(move_type, defender.types)
   ```
2. Encode "unknown" as a dedicated sentinel value distinct from neutral (1.0) and immunity
   (0.0). Use a separate binary feature `type_known: bool` in the obs vector so the policy
   can learn to discount effectiveness estimates when type is unknown.
3. For species-revealed-but-Tera-unrevealed: check `pokemon.terastallized` and
   `pokemon.tera_type`. If Tera is active and tera_type is known, use tera_type for defense
   calc; otherwise fall back to base types.

---

### Pitfall 3: Stellar Tera Type Breaks Effectiveness Lookup

**What goes wrong:** The Stellar type (Gen 9 Tera type) has no defensive type chart row — a
Stellar-Tera Pokemon retains its original defensive typing. But offensively, Stellar Tera Blast
is super effective against ALL Terastallized targets regardless of type. A naive type chart
lookup treating Stellar as a 19th type will return "neutral vs everything" (correct for defense,
wrong for offense) and miss the conditional super-effective case.

**Why it happens:** Stellar is not in the standard 18-type effectiveness matrix. Implementations
that look up `effectiveness[STELLAR][defender_type]` will either KeyError or return a default.

**Consequences:** Agent never learns to exploit Stellar Tera Blast correctly; may also
misidentify a Stellar-Tera defender as having a Stellar defensive type and compute wrong
resistances.

**Prevention:**
1. Handle Stellar as a special case before the matrix lookup:
   ```python
   if move_type == PokemonType.STELLAR:
       # Offensive: 1x normally, but 2x vs any Terastallized target
       return 2.0 if defender.terastallized else 1.0
   if defender.terastallized and defender.tera_type == PokemonType.STELLAR:
       # Defensive: use base types, not Stellar
       use_types = defender.base_types
   else:
       use_types = defender.types
   ```
2. Add a unit test covering Stellar attacker vs Tera and non-Tera defenders.

---

### Pitfall 4: Dual-Type Immunity Overridden by Effectiveness

**What goes wrong:** Ghost/Normal immunity (and similar: Ground/Flying, Electric/Ground,
Psychic/Dark, etc.) must short-circuit the dual-type multiplication. If calculated as
`eff_type1 * eff_type2`, an immunity on one type correctly gives 0x. But if the code iterates
types and sums instead of multiplying, or uses `max()` instead of `product()`, immunities
are lost.

**Why it happens:** Dual-type effectiveness is `product(effectiveness[move][t] for t in types)`.
Any deviation — averaging, summing, taking max — breaks immunities and 4x weaknesses.

**Consequences:** Agent learns to use Normal moves into Ghost types and gets 0 damage; reward
signal misleads training since no damage = turn wasted.

**Prevention:**
1. Use multiplicative combination, never additive:
   ```python
   effectiveness = 1.0
   for t in defender_types:
       if t is not None:
           effectiveness *= TYPE_CHART[move_type][t]
   ```
2. Explicitly test: Normal vs Ghost/Flying (should be 0x), Ground vs Water/Flying (should be
   0x), Rock vs Fire/Flying (should be 4x).

---

### Pitfall 5: 4x vs 0x Normalization Asymmetry Hurts Learning

**What goes wrong:** If you normalize type effectiveness to [0, 1] by dividing by 4, the
values become: 0x → 0.0, 0.5x → 0.125, 1x → 0.25, 2x → 0.5, 4x → 1.0. Immunities (0.0)
and super-effective (1.0) are correctly at extremes but the neutral point (1x = 0.25) is far
from center, making it hard for the network to learn "this move is average."

**Why it happens:** Linear normalization of a multiplicative scale.

**Prevention:** Use log2 encoding or a discrete 5-class encoding instead:
```python
def encode_effectiveness(e: float) -> float:
    # Maps: 0->-2, 0.5->-1, 1->0, 2->1, 4->2, then normalize to [-1,1]
    if e == 0.0:
        return -1.0   # immunity — hardest negative signal
    return math.log2(e) / 2.0  # -1, -0.5, 0, 0.5, 1
```
This centers neutral at 0.0 and treats 4x and 0x symmetrically as extreme signals.
Alternatively, use 5 one-hot bins: [immune, resisted, neutral, super, quad].

---

## Moderate Pitfalls

---

### Pitfall 6: MaxBasePowerPlayer Ignores Type — Curriculum Opponent Too Easy Early, Wrong Signal

**What goes wrong:** `MaxBasePowerPlayer` picks the highest base-power move with zero type
awareness. Against the agent's team, it will often hit into resistances or immunities, making
it an artificially weak opponent that doesn't teach the agent to play around super-effective
hits. Graduating to `MaxDamagePlayer` (if used) or self-play too early flips this: the agent
suddenly faces optimal play and win rate collapses, causing sparse reward and policy drift.

**Prevention:**
1. Use MaxBasePowerPlayer as Stage 1 only. Define explicit win-rate thresholds before
   graduating (e.g., >70% win rate over 500 episodes).
2. Confirm `MaxBasePowerPlayer` works with your custom teambuilder: it operates on
   `battle.available_moves` which is populated regardless of how the team was built, so
   `RotatingTeambuilder` (or equivalent) is compatible — no special wiring needed.
3. For the curriculum transition, anneal rather than hard-switch. Mix opponents:
   ```python
   # 80% easy, 20% hard at transition boundary; shift over 10k steps
   ```

---

### Pitfall 7: RotatingTeambuilder Desync Between Agent and Opponent

**What goes wrong:** If both the training agent and the curriculum opponent use separate
`RotatingTeambuilder` instances rotating independently, the matchups become non-uniform. One
side may always see Team A vs Team B while Team C vs Team D is never played, creating coverage
gaps in the obs distribution.

**Prevention:**
1. Seed both teambuilders or use a shared shuffle sequence to ensure full matchup coverage.
2. Alternatively, give the curriculum opponent a fixed team or `ConstantTeambuilder` — the
   agent's team rotates, the opponent's does not, which is simpler and still provides
   generalization pressure.

---

### Pitfall 8: BC Policy Entropy Collapse Stalls Early RL

**What goes wrong:** A BC-pretrained policy that saw consistent expert actions in specific
game states will assign very low entropy (high confidence) to those states. When RL fine-tuning
begins, PPO's entropy bonus is insufficient to overcome this, and the policy fails to explore
alternatives. Training loss decreases but win rate plateaus because the agent never discovers
moves the BC demonstrations never made.

**Why it happens:** BC training via cross-entropy minimization directly encourages low entropy.
PPO's default `ent_coef=0.01` is calibrated for randomly initialized policies, not pre-trained
high-confidence ones.

**Consequences:** RL appears to converge in 10k steps but to a suboptimal policy that mirrors
BC with only marginal improvement.

**Prevention:**
1. Increase `ent_coef` for the first N RL steps after BC init (e.g., `ent_coef=0.05` for
   first 100k steps, then anneal to 0.01).
2. Add a KL divergence penalty against the BC policy to prevent the RL policy from drifting
   too far from known-good behavior while still allowing exploration:
   ```python
   # Proximal approach: add KL(pi_rl || pi_bc) * beta to loss
   ```
3. Monitor policy entropy as a training metric. If entropy < 0.5 nats in first 50k RL steps,
   increase `ent_coef`.

---

### Pitfall 9: BC Action Space Mismatch — Move Slot vs Move Name

**What goes wrong:** Pokemon Showdown battle replays record which move was used (by name, e.g.,
"Thunderbolt") and which Pokemon switched in. poke-env's action space uses integer indices into
`battle.available_moves` and `battle.available_switches` — lists that vary in length and order
each turn. Mapping "Thunderbolt" to action index 2 on turn 5 requires knowing the exact order
of available moves at that turn, which the replay does not directly encode.

**Why it happens:** Replays are log-format, not state-format. The available_moves list is
reconstructed from game state, and its order (move slot 0–3) is deterministic per-Pokemon but
the available subset changes with PP depletion, disable, encore, etc.

**Consequences:** Incorrect action labels in BC training data cause the policy to learn to
"use action index 1" when it should learn "use the super-effective move." This is silent —
no crash, just wrong supervision signal.

**Prevention:**
1. Reconstruct the full poke-env battle state at each turn during replay parsing, then call
   `env.action_to_move()` / `env.available_moves` to find the correct index. The Metamon
   project (UT Austin RPL) has solved this for Random Battle — examine their
   `ParsedReplayDataset` implementation as reference.
2. For switch actions: poke-env encodes switches as `len(available_moves) + switch_slot`.
   Map "switched in Charizard" to the correct switch index by matching species name in
   `battle.available_switches`.
3. Log and inspect the mismatch rate during BC data prep. If >5% of turns produce unmappable
   actions, the parsing logic is wrong.

---

### Pitfall 10: BC Overfits to Specific Team Compositions Not Seen in RL Env

**What goes wrong:** If BC training data comes from high-ladder replays of specific archetypes
(e.g., Sun teams, Hyper Offense), the pretrained policy learns move patterns that are only
correct in those team contexts. When RL begins with a different/rotating team composition, the
policy applies the BC-learned patterns incorrectly (e.g., always clicking Fire move because
Sun team data always had Drought active).

**Prevention:**
1. Filter BC replay data to match the team pool used in RL training. If RL uses a rotating
   6-team pool, BC data should come from replays featuring at least some of those same Pokemon.
2. Apply format filtering: collect only replays from the same format (e.g., Gen9OU) and
   season/ruleset used in training.
3. Rate filtering for data quality: discard replays below 1500 ELO. Low-rated games teach
   suboptimal patterns (not switching on obvious forced switches, using status into Substitute).
   Smogon ladder publishes ELO alongside replay metadata.

---

## Minor Pitfalls

---

### Pitfall 11: Type Chart Hardcoded vs poke-env's GenData

**What goes wrong:** Manually hardcoding the 18x18 type chart as a Python dict and forgetting
to update it for Gen 9 changes (Fairy type added in Gen 6; Poison/Steel rebalanced). If the
RL env uses Gen 9 but the effectiveness table is Gen 5, a handful of matchups are wrong.

**Prevention:** Use poke-env's `GenData.from_format(format).type_chart` which is version-aware.
Do not hardcode — derive from the same data source the env uses.

---

### Pitfall 12: Missing Ability Modifiers in Effectiveness Calc

**What goes wrong:** Type effectiveness alone ignores ability modifiers that change effective
multipliers: Levitate (Ground immunity), Flash Fire (Fire immunity), Volt Absorb (Electric
immunity), Wonder Guard (only super effective hits land), etc. A "correct" type calc returning
2x for Ground vs a Levitate Pokemon is wrong.

**Prevention:** Encode raw type effectiveness as the obs feature (without ability mods) but
train the agent to learn ability interactions from battle outcomes. Do not attempt to embed full
ability-aware effectiveness — the state space explodes and abilities are often unrevealed.
Alternatively, add a separate binary obs feature `has_known_immunity` populated from
`opponent_active_pokemon.ability` when ability has been revealed.

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Adding type obs features | OBS_DIM checkpoint mismatch | Add assertion; use `custom_objects` on load |
| Type effectiveness encoding | Unknown/None type crashes | Guard with neutral fallback + `type_known` flag |
| Stellar Tera handling | Missing conditional super-effective | Special-case before matrix lookup |
| Curriculum opponent setup | MaxBasePower too easy / dense reward | Win-rate threshold gating for stage graduation |
| Teambuilder for opponent | RotatingTeambuilder desync | Seed or use ConstantTeambuilder for opponent |
| BC pre-training | Action index mismatch from replay | Reconstruct env state per turn; reference Metamon |
| BC pre-training | Data quality — low-ELO bad habits | Filter to >1500 ELO; format-match to RL env |
| RL fine-tuning after BC | Entropy collapse / no exploration | Increase ent_coef for first 100k steps |
| Doubles obs expansion | OBS_DIM_DOUBLES not updated | Update both constants atomically; add assertion |

---

## Sources

- poke-env baselines.py: https://github.com/hsahovic/poke-env/blob/master/src/poke_env/player/baselines.py
- poke-env teambuilder docs: https://poke-env.readthedocs.io/en/latest/examples/using_a_custom_teambuilder.html
- Metamon (UT Austin RPL — BC from Showdown replays): https://github.com/UT-Austin-RPL/metamon
- Metamon parsed replay dataset: https://huggingface.co/datasets/jakegrigsby/metamon-parsed-replays
- Bulbapedia type chart / Stellar type: https://bulbapedia.bulbagarden.net/wiki/Type/Type_chart
- Stellar type mechanics: https://bulbapedia.bulbagarden.net/wiki/Type
- BC distributional shift theory: https://leeyngdo.github.io/blog/reinforcement-learning/2024-02-20-imitation-learning/
- Compounding errors in BC: https://arxiv.org/html/2407.15007v1
- Posterior BC (entropy-aware warm start): https://arxiv.org/html/2512.16911
- Entropy collapse in PPO fine-tuning: https://arxiv.org/html/2405.00662v1
- SB3 PPO docs (custom_objects on load): https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html
- Curriculum RL survey: https://arxiv.org/abs/2003.04960
