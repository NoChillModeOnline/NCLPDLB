# Requirements — NCLPDLB ML Knowledge Injection

*Generated: 2026-03-17 from research synthesis*

---

## V1 (This Milestone)

### REQ-01 — Type Effectiveness Observation Expansion

**Priority:** Critical (all other changes depend on this)

- `battle_env.py` `OBS_DIM` constant updated from 44 to 48
- `battle_env.py` `OBS_DIM_DOUBLES` updated atomically in the same commit
- 4 new floats added to obs vector (one per move slot): type effectiveness of that move vs current opponent active Pokémon
- Normalization: log2 encoding — `log2(effectiveness) / 2.0` → range [-1, 1]; immunity hardcoded to -1.0; unknown opponent type defaults to 0.0 (neutral in log2 space)
- New `src/ml/type_chart.py` module; effectiveness computed via poke-env `damage_multiplier()` method (handles dual typing automatically); do NOT hardcode 18×18 matrix
- Assertion added at env init: `assert env.observation_space.shape[0] == OBS_DIM`
- Stellar Tera type special-cased before any matrix lookup
- All existing OBS_DIM=44 checkpoints are abandoned (clean break)
- Backward-compatible: `train_all.py` invocations unchanged

### REQ-02 — MaxBasePowerPlayer Curriculum Opponent

**Priority:** High

- `train_policy.py` epoch-0 opponent changed from `RandomPlayer` to `MaxBasePowerPlayer`
- Import: `from poke_env.player import MaxBasePowerPlayer` (NOT `MaxDamagePlayer` — does not exist)
- Graduation from curriculum to self-play gated by explicit win-rate threshold (≥70% over 500 episodes)
- `SelfPlayCallback` and `BattleEnv` unchanged
- Backward-compatible: existing `train_all.py` call signature unchanged

### REQ-03 — Behavioral Cloning Pre-Training

**Priority:** High

- New `src/ml/pretrain.py` module implementing BC training loop using `imitation` library (`pip install imitation`)
- Input: parsed replay data from existing `replay_parser.py` → `BattleRecord` objects → `feature_extractor.py` → numpy obs arrays (must use OBS_DIM=48)
- Output: `bc_actor_checkpoint.pt` (actor weights only: `mlp_extractor.*` + `action_net.*` keys)
- BC-to-PPO weight transfer: partial state dict update; value head stays at random init (no BC signal for value)
- `train_policy.py` new `--pretrain <path>` flag; mutually exclusive with `--resume`; weights loaded at step 0 before any RL updates
- `ent_coef` raised to 0.05 for first 100k PPO steps after BC init, then annealed to 0.01
- Action index mapping verified: replay move names → poke-env integer action indices; abort if >5% of turns fail to map
- GitHub Actions workflow updated: scrape replays → pretrain → RL

---

## V2 (Next Milestone — Do Not Build Now)

- **REQ-V2-01** STAB flag per move (4 binary floats) — OBS_DIM 48→52
- **REQ-V2-02** Speed tier comparison (2 floats: binary faster/slower + ratio) — OBS_DIM 52→54
- **REQ-V2-03** Opponent active Pokémon boosts (6 floats) — OBS_DIM 54→60

---

## Out of Scope

- Ability awareness (~300 abilities; embedding approach; often unrevealed mid-battle)
- Item awareness (hidden until activated; separate revealed-flag pattern)
- Full Smogon tier data integration
- Opponent moveset tracking (requires opponent modeling)
- Full damage calculator in obs (redundant once type_eff + STAB + boosts are present)
- OBS_DIM=54 expansion in this milestone (validate 44→48 first)

---

## Constraints

- Must not break existing `train_all.py` invocations (backward-compatible API only)
- OBS_DIM change invalidates all saved checkpoints — clean break required
- poke-env `MaxBasePowerPlayer` is the correct class name (verified in baselines.py)
- BC obs arrays must be built with OBS_DIM=48 feature extractor (not legacy 44)
- Windows (local dev) and Linux (GitHub Actions) both supported
