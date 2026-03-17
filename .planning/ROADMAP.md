# Roadmap — NCLPDLB ML Knowledge Injection

*Generated: 2026-03-17*

---

## Phase Overview

| Phase | Name | Status | Goal |
|-------|------|--------|------|
| 01 | Observation Space Expansion | ⬜ pending | Add type effectiveness to obs vector; OBS_DIM 44→48 |
| 02 | Curriculum Opponent | ⬜ pending | MaxBasePowerPlayer at epoch 0; win-rate threshold |
| 03 | Behavioral Cloning Pre-Training | ⬜ pending | pretrain.py + --pretrain flag + workflow update |

---

## Phase 01 — Observation Space Expansion

**Goal:** Expand observation vector from 44 to 48 floats by adding per-move type effectiveness
signals, enabling the agent to learn type matchups from reward signal instead of discovering
them blindly.

**Success Criteria:**
- `OBS_DIM == 48` in `battle_env.py` (and `OBS_DIM_DOUBLES` updated atomically)
- New `src/ml/type_chart.py` module with `get_type_effectiveness(move, defender)` function
- `_move_features()` in `battle_env.py` returns 5 values (power, acc, type_id, prio, **type_eff**)
- Log2 normalization: `log2(e)/2.0` → [-1,1]; unknown type → 0.0; immunity → -1.0
- Stellar Tera type special-cased before matrix lookup
- Assertion at env init catches future OBS_DIM mismatches
- `train_all.py` runs without modification (backward-compatible)
- All OBS_DIM=44 checkpoints deprecated (documented in commit message)

**Research flag:** None — type chart math and poke-env API fully documented in research.

**Key files:**
- `src/ml/type_chart.py` (NEW)
- `src/ml/battle_env.py` (MODIFIED)

**Blocks:** Phase 02 (type_eff obs needed to validate curriculum), Phase 03 (BC Transitions must use OBS_DIM=48)

---

## Phase 02 — Curriculum Opponent

**Goal:** Replace RandomPlayer epoch-0 opponent with MaxBasePowerPlayer to give the agent
meaningful training signal during early exploration, and gate self-play graduation behind
an explicit win-rate threshold.

**Success Criteria:**
- `train_policy.py` `SelfPlayOpponent` epoch-0 path uses `MaxBasePowerPlayer`
- Import is `from poke_env.player import MaxBasePowerPlayer` (verified)
- Win-rate threshold: ≥70% over 500 episodes required before graduation to self-play
- `BattleEnv` and `SelfPlayCallback` unchanged
- `train_all.py` call signature unchanged
- Phase 01 type_eff obs is present (enables win-rate validation of Phase 01 encoding)

**Research flag:** None — MaxBasePowerPlayer constructor is a one-liner; already verified.

**Key files:**
- `src/ml/train_policy.py` (MODIFIED)

**Depends on:** Phase 01 (validates type_eff encoding against a deterministic opponent)

---

## Phase 03 — Behavioral Cloning Pre-Training

**Goal:** Build a BC pre-training pipeline that extracts (state, action) pairs from human
Showdown replays and initializes PPO actor weights, giving the agent a head start on move
selection before any RL updates.

**Success Criteria:**
- `src/ml/pretrain.py` BC training loop using `imitation` library
- BC input: BattleRecords from replay_parser.py → feature_extractor.py (OBS_DIM=48 arrays)
- BC output: `bc_actor_checkpoint.pt` (actor-only: `mlp_extractor.*` + `action_net.*` keys)
- `train_policy.py` `--pretrain <path>` flag loads checkpoint at step 0 (not --resume)
- `ent_coef=0.05` for first 100k PPO steps after BC init; anneal to 0.01
- Action index mapping logs unmappable turn rate; aborts if >5%
- GitHub Actions workflow updated: scrape → pretrain → RL
- `pip install imitation` added to requirements

**Research flag:** YES — action space reconstruction from Showdown replay logs is highest-risk.
Study Metamon ParsedReplayDataset (https://github.com/UT-Austin-RPL/metamon) before planning.

**Key files:**
- `src/ml/pretrain.py` (NEW)
- `src/ml/train_policy.py` (MODIFIED — --pretrain flag)
- `.github/workflows/train.yml` (MODIFIED — scrape + pretrain steps)

**Depends on:** Phase 01 (BC Transitions must use OBS_DIM=48 obs vectors)

---

## Dependency Graph

```
Phase 01 (obs expansion)
     |
     +---> Phase 02 (curriculum) — validates Phase 01 encoding
     |
     +---> Phase 03 (BC pretrain) — requires OBS_DIM=48 settled
```

---

*Last updated: 2026-03-17 after research synthesis*
