# Project Research Summary

**Project:** NCLPDLB ML Knowledge Injection
**Domain:** Competitive Pokemon RL -- observation expansion, curriculum training, behavioral cloning
**Researched:** 2026-03-17
**Confidence:** MEDIUM-HIGH (core mechanics HIGH; BC pipeline MEDIUM; ROI ordering MEDIUM)

---

## Executive Summary

This milestone adds three improvements to an existing poke-env 0.12.1 + SB3 PPO battle bot.
The core change -- expanding the observation space from OBS_DIM=44 to OBS_DIM=48 by adding one
type-effectiveness float per move slot -- is well-understood and low-risk in isolation. The risk
comes from the hard constraint that any prior OBS_DIM=44 checkpoints are immediately invalidated:
SB3 serializes observation space shape into .zip checkpoints and there is no automatic migration
path. Every downstream artifact (BC training data, pretrain.py, the PPO policy) must agree on
OBS_DIM=48 from the moment the constant changes. Handle this as a clean break, not an upgrade.

The curriculum opponent change is straightforward: MaxBasePowerPlayer (NOT MaxDamagePlayer --
that class does not exist in poke-env) can be dropped in as an epoch-0 opponent with a single
conditional in train_policy.py. No changes to SelfPlayCallback or BattleEnv are needed.
The BC pre-training pipeline is the highest-complexity piece: the imitation library integrates
natively with SB3 and is the only viable option (SB3 has no built-in BC in v2.x). The correct
weight-transfer pattern is a partial state dict update that overwrites only actor keys, leaving
the value head randomly initialized -- value estimation has no BC signal.

The two non-obvious failure modes to defend against at implementation time are: (1) unknown
opponent type producing a false immunity signal -- always fall back to 1.0 (neutral), never 0.0,
when type is unknown; and (2) BC entropy collapse during RL fine-tuning -- raise ent_coef from
the default 0.01 to 0.05 for the first ~100k PPO steps after BC initialization. These two issues
are silent: no crash, just a policy that trains but learns the wrong thing.

---

## Key Findings

### Recommended Stack

The existing stack requires one new dependency: pip install imitation. Everything else --
poke-env 0.12.1, SB3, aiohttp -- is already present and sufficient. The Gen 9 type chart should
be sourced from poke-env's GenData.from_gen(9).type_chart at runtime rather than a hardcoded
matrix; this guarantees version consistency with the environment's own damage calculations.
Alternatively, battle.opponent_active_pokemon.damage_multiplier(move) handles dual typing
automatically and is the simplest correct implementation.

**Core technologies:**

- poke-env 0.12.1: Battle environment + MaxBasePowerPlayer -- verified in baselines.py
- stable-baselines3: PPO training -- no version change needed
- imitation (new): BC pre-training; provides BC class and Transitions type compatible with SB3
  ActorCriticPolicy; SB3 official docs explicitly defer to this library for BC
- torch: Partial state dict operations for BC-to-PPO weight transfer
- GenData / damage_multiplier(): Type effectiveness lookup -- version-aware, handles dual types

**Critical name correction:** The curriculum opponent class is MaxBasePowerPlayer. The name
MaxDamagePlayer does not exist in poke-env and will raise ImportError at runtime.

### Expected Features

This milestone has a defined scope. The features below reflect what research says to build
now vs what to defer.

**Build in this milestone:**

- Type effectiveness (4 floats, one per move slot) -- primary OBS signal gap; validates via
  win-rate improvement against MaxBasePowerPlayer
- MaxBasePowerPlayer curriculum (epoch 0 only) -- explicit win-rate threshold gates graduation
  to self-play; prevents premature jump to harder opponent
- BC pre-training from Showdown replays -- injects human strategy priors; saves early sample
  budget; requires replay parser + action space alignment verification

**High-ROI candidates for next milestone (do not build now):**

- STAB flag per move (4 binary floats) -- pairs naturally with type_eff architecturally but
  not required to validate the current 4-float expansion
- Speed tier comparison (2 floats: binary + ratio) -- highest-ROI feature not in current scope
- Opponent boosts (6 floats) -- medium ROI; poke-env exposes via opponent_active_pokemon.boosts

**Defer to v2+:**

- Ability awareness -- ~300 abilities; use embedding approach not one-hot; often unrevealed
- Item awareness -- items hidden until activated; use revealed-flag pattern when ready
- Full damage calculator in obs -- redundant once type_eff + STAB + boosts are present

**Anti-feature to avoid now:** Expanding to OBS_DIM=54 (type_eff + STAB + speed) in a single
commit. This milestone is OBS_DIM=48 only. Validate the 4-float expansion before adding more.

### Architecture Approach

Three files change and two files are new. battle_env.py is the single source of truth for
OBS_DIM -- import it everywhere rather than redeclaring the constant. The BC-to-PPO weight
transfer uses a partial state dict update (overwrite actor keys only, leave value head at random
init) without forking SB3. The --pretrain and --resume flags in train_policy.py are mutually
exclusive: --pretrain is a custom weight init at step 0, not a checkpoint resume.

**Files changed:**

1. type_chart.py (NEW) -- effectiveness lookup via GenData.from_gen(9), not hardcoded
2. feature_extractor.py (MODIFIED) -- append type_effectiveness[0..3] to obs vector
3. battle_env.py (MODIFIED) -- OBS_DIM = 48; OBS_DIM_DOUBLES updated atomically; assertion added
4. pretrain.py (NEW) -- BC training loop; produces bc_actor_checkpoint.pt
5. train_policy.py (MODIFIED) -- --pretrain flag + epoch-0 MaxBasePowerPlayer

**Files unchanged:** SelfPlayCallback, replay_scraper.py, replay_parser.py

**Data flow after all changes:**

```
replay_parser.py  ->  BattleRecord objects
      |
      v  (uses OBS_DIM=48)
feature_extractor.py  ->  obs arrays + action labels
      |
      v
pretrain.py  ->  bc_actor_checkpoint.pt (actor weights only)
      |
      v  (--pretrain flag)
train_policy.py  ->  PPO with BC-initialized actor
      |
      v  (epoch 0)
MaxBasePowerPlayer  ->  win-rate threshold  ->  SelfPlayCallback
```

### Critical Pitfalls

1. **OBS_DIM checkpoint mismatch** -- All OBS_DIM=44 checkpoints are dead after this change.
   Add assertion at env instantiation:
   assert env.observation_space.shape[0] == OBS_DIM
   Invalidate cached checkpoints in CI. BC Transitions must be built with the OBS_DIM=48
   feature extractor. Update OBS_DIM_DOUBLES atomically in the same commit as OBS_DIM.

2. **Unknown type defaults to 0.0 (false immunity)** -- Guard every type lookup with:
   return 1.0 if any(t is None for t in defender.types) else calculate(...)
   Using 0.0 as fallback teaches the agent that unknown mons are immune to everything.
   Neutral (1.0) is the least-biased unknown encoding.

3. **BC entropy collapse blocks RL exploration** -- After BC init, the policy has low entropy on
   states seen in training data. PPO default ent_coef=0.01 will not recover. Set ent_coef=0.05
   for the first 100k PPO steps then anneal to 0.01. Monitor entropy as a training metric; if
   it drops below 0.5 nats in first 50k steps, increase ent_coef further.

4. **BC action index mismatch** -- Replay logs record move names; poke-env action space uses
   integer indices into battle.available_moves. These indices shift with PP depletion, Disable,
   Encore. Reconstruct full poke-env battle state per turn during replay parsing. Reference the
   Metamon ParsedReplayDataset. Log unmappable action rate; abort if >5% of turns fail to map.

5. **Effectiveness normalization conflict between research files** -- ARCHITECTURE.md recommends
   divide by 4.0; PITFALLS.md overrides with log2. Log2 is correct: log2(e) / 2.0 maps to
   [-1, 1], centers neutral at 0.0, treats 4x and immune as symmetric extremes. Hardcode
   immunity to -1.0. Do not use divide-by-4 (places neutral at 0.25, far from center).

---

## Implications for Roadmap

Based on research, three sequential phases are strongly indicated by implementation dependencies.
The BC pre-training phase must follow the OBS_DIM expansion because BC Transitions must be built
with the expanded feature extractor. The RL integration phase must follow BC pre-training because
--pretrain loads the BC checkpoint.

### Phase 1: Observation Space Expansion (OBS_DIM 44 to 48)

**Rationale:** All downstream work depends on the new obs shape. This is the only phase that
invalidates existing checkpoints -- isolate it cleanly before any other code change lands. This
phase also has the most encoding footguns (normalization options, Stellar Tera edge case, unknown
type handling) and warrants its own isolated phase so failures are attributable.

**Delivers:** Expanded obs vector with type effectiveness per move slot; updated OBS_DIM constant
and OBS_DIM_DOUBLES; type_chart.py module; assertion catching future shape mismatches

**Features addressed:** Type effectiveness (4 floats, log2 normalized)

**Must avoid:**
- Pitfall 1 (checkpoint mismatch) -- add OBS_DIM assertion; deprecate old checkpoints in CI
- Pitfall 2 (unknown type = false immunity) -- neutral fallback = 1.0 not 0.0
- Pitfall 3 (Stellar Tera) -- special-case before matrix lookup
- Pitfall 4 (dual-type: multiply not sum)
- Pitfall 5 (normalization) -- log2 encoding, not divide-by-4

**Does not need deeper research:** Type chart fully documented; poke-env API verified.

---

### Phase 2: Curriculum Opponent -- MaxBasePowerPlayer at Epoch 0

**Rationale:** No obs changes required and no dependencies on Phase 1 or Phase 3. Placed after
Phase 1 so the new type_eff features are in place when evaluating whether the agent exploits type
advantages against the curriculum opponent. Phase 2 is the validation mechanism for Phase 1:
if win-rate vs MaxBasePowerPlayer does not improve after adding type_eff obs, the encoding is
wrong.

**Delivers:** train_policy.py with build_opponent() function; epoch-0 MaxBasePowerPlayer
opponent; win-rate threshold gating before graduation to self-play (recommended: >70% over 500
episodes)

**Features addressed:** MaxBasePowerPlayer curriculum

**Must avoid:**
- Wrong class name -- import is: from poke_env.player import MaxBasePowerPlayer
- Pitfall 7 (RotatingTeambuilder desync) -- use ConstantTeambuilder or seeded shuffle for opponent
- Premature graduation to self-play -- enforce explicit win-rate threshold

**Does not need deeper research:** MaxBasePowerPlayer constructor call verified against source.

---

### Phase 3: Behavioral Cloning Pre-Training

**Rationale:** Depends on Phase 1 -- BC Transitions must use OBS_DIM=48 obs vectors. Placed
last because it has the most unknowns and highest complexity; replay parsing correctness, action
index alignment, and BC-to-PPO weight transfer all need careful validation.

**Delivers:** pretrain.py BC training loop; bc_actor_checkpoint.pt artifact; --pretrain flag in
train_policy.py with mutual exclusion vs --resume

**Features addressed:** Behavioral cloning from Showdown replays

**Must avoid:**
- Pitfall 8 (BC entropy collapse) -- ent_coef=0.05 for first 100k RL steps after BC init
- Pitfall 9 (action index mismatch) -- reconstruct poke-env state per turn; verify via Metamon
- Pitfall 10 (team composition mismatch) -- filter replays to >1500 ELO; format-match to RL env

**Needs deeper research before implementation:**
- Action space reconstruction from replay logs -- review Metamon ParsedReplayDataset before
  writing any parsing code: https://github.com/UT-Austin-RPL/metamon
- Switch action encoding -- poke-env encodes switches as len(available_moves) + switch_slot;
  verify this matches BattleEnv.action_space exactly before building the BC dataset

---

### Phase Ordering Rationale

- Phase 1 before Phase 3: BC Transitions are numpy arrays shaped (N, OBS_DIM). Building them
  with the old OBS_DIM=44 extractor then loading into an OBS_DIM=48 PPO policy silently corrupts
  training. OBS_DIM must be settled before any BC data is generated.
- Phase 2 after Phase 1: MaxBasePowerPlayer is the validation test for Phase 1. Run it with the
  new type_eff obs to confirm the encoding is working before investing in BC infrastructure.
- Phase 3 last: Highest complexity; other phases do not depend on it; its benefits are only
  visible after the obs expansion and curriculum are in place.

### Research Flags

**Needs research-phase during planning:**

- Phase 3 (BC): Action space reconstruction from Showdown replay logs is the single highest-risk
  implementation task. Study Metamon ParsedReplayDataset before writing any parsing code.
  Do not guess at the turn-state reconstruction logic.

**Standard patterns -- skip research-phase:**

- Phase 1 (obs expansion): Type chart math and poke-env obs API are fully documented.
- Phase 2 (curriculum): MaxBasePowerPlayer constructor is a one-liner.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | MaxBasePowerPlayer verified in baselines.py source; imitation BC API verified against readthedocs; SB3 obs incompatibility confirmed via GitHub issue #2031 |
| Features | MEDIUM | Type_eff and STAB ROI validated by poke-env official example; speed tier and BC ROI based on domain knowledge, not published ablations |
| Architecture | MEDIUM-HIGH | Partial state dict pattern is standard PyTorch (HIGH); poke-env SingleAgentWrapper opponent wiring is MEDIUM (less detail in docs than source) |
| Pitfalls | HIGH | All critical pitfalls cross-validated across ARCHITECTURE.md and PITFALLS.md; entropy collapse and action mismatch backed by published papers |

**Overall confidence:** MEDIUM-HIGH

### Gaps to Address

- **Normalization conflict between research files:** ARCHITECTURE.md says divide by 4.0;
  PITFALLS.md says log2. This SUMMARY resolves the conflict: use log2. Implementer must
  document the choice in code comments with this rationale.

- **BC dataset availability:** Research assumes replay files are available. If scraped replays
  do not exist yet, replay_scraper.py must run before pretrain.py can train. Verify replay
  dataset exists and is format-matched before beginning Phase 3 planning.

- **poke-env BattleEnv constructor signature for opponent:** ARCHITECTURE.md notes MEDIUM
  confidence on the exact API for passing MaxBasePowerPlayer to BattleEnv. Verify whether
  BattleEnv.__init__ accepts an opponent= kwarg directly before starting Phase 2 implementation.

- **OBS_DIM_DOUBLES current value:** Research confirms this constant exists and must be updated
  atomically with OBS_DIM, but its current value and derivation formula are not documented in
  the research files. Audit battle_env.py for this constant before the Phase 1 PR lands.

---

## Sources

### Primary (HIGH confidence)

- poke-env baselines.py -- MaxBasePowerPlayer class verified:
  https://github.com/hsahovic/poke-env/blob/master/src/poke_env/player/baselines.py
- imitation BC docs -- BC class, Transitions type, training loop:
  https://imitation.readthedocs.io/en/latest/algorithms/bc.html
- SB3 imitation learning guide (defers to imitation library):
  https://stable-baselines3.readthedocs.io/en/master/guide/imitation.html
- SB3 obs space incompatibility -- GitHub issue #2031:
  https://github.com/DLR-RM/stable-baselines3/issues/2031
- Metamon paper (BC from Showdown replays at scale):
  https://arxiv.org/abs/2504.04395
- Metamon parsed replay dataset (reference implementation):
  https://huggingface.co/datasets/jakegrigsby/metamon-parsed-replays

### Secondary (MEDIUM confidence)

- poke-env RL with Gymnasium wrapper example (validates type_eff + STAB as essential obs):
  https://poke-env.readthedocs.io/en/stable/examples/rl_with_gymnasium_wrapper.html
- SB3 ActorCriticPolicy source (partial state dict pattern):
  https://stable-baselines3.readthedocs.io/en/master/_modules/stable_baselines3/common/policies.html
- poke-env env module docs:
  https://poke-env.readthedocs.io/en/stable/modules/env.html
- Entropy collapse in PPO fine-tuning after BC:
  https://arxiv.org/html/2405.00662v1
- Bulbapedia -- Stellar type mechanics:
  https://bulbapedia.bulbagarden.net/wiki/Type

### Tertiary (LOW confidence)

- Ivison 2021 blog -- anecdotal type_eff obs improvement in early training:
  https://ivison.id.au/2021/08/02/pokerl.html

---

*Research completed: 2026-03-17*
*Ready for roadmap: yes*
