# NCLPDLB ML Knowledge Injection

## What This Is

A reinforcement learning Pokemon battle bot (poke-env + stable-baselines3 PPO) that currently
learns purely through self-play. This milestone injects three forms of domain knowledge to
accelerate learning across 22 competitive formats: type effectiveness awareness in the
observation space, a stronger curriculum opponent, and imitation learning pre-training
from human Showdown replays.

## Core Value

The bot must learn to make type-effective, strategically sound decisions far faster than
pure self-play allows — reducing steps needed to surpass random baseline from ~200k to ~50k.

## Requirements

### Validated

- ✓ PPO self-play training pipeline (train_policy.py) — existing
- ✓ Battle observation space (battle_env.py, OBS_DIM=44) — existing
- ✓ Replay scraper and parser (replay_scraper.py, replay_parser.py) — existing
- ✓ Feature extractor for offline datasets (feature_extractor.py) — existing
- ✓ Multi-format training runner (train_all.py, 22 formats) — existing

### Active

- [ ] Type effectiveness features added to observation space (battle_env.py)
- [ ] OBS_DIM updated from 44 to 48 (singles) and OBS_DIM_DOUBLES from 72 to 76
- [ ] MaxDamagePlayer curriculum: initial steps vs max-damage opponent before self-play
- [ ] Imitation learning pre-trainer (new src/ml/pretrain.py)
- [ ] BC policy trained from Showdown replays initializes PPO starting weights
- [ ] train_policy.py --pretrain flag to load BC checkpoint
- [ ] GitHub Actions workflow updated to scrape replays + pretrain before RL

### Out of Scope

- Full Smogon tier data integration — too large a dependency for this milestone
- Ability/item awareness in obs — follow-on milestone after type chart proves out
- Opponent moveset tracking — requires opponent modeling, separate milestone

## Context

**Architecture:**
- battle_env.py: Gymnasium wrapper; embed_battle() builds obs vector, calc_reward() shapes reward
- train_policy.py: PPO training; SelfPlayOpponent starts as RandomPlayer (epoch 0), swaps checkpoint every swap_every steps
- replay_scraper.py / replay_parser.py: async scraper + log parser -> BattleRecord objects
- feature_extractor.py: converts BattleRecords to numpy arrays for offline ML

**Type effectiveness gap:** Move features include type_id but NOT effectiveness vs opponent.
Agent must discover through reward signal that Fire is weak to Water — requires thousands of
redundant battles currently.

**Curriculum gap:** SelfPlayOpponent starts as RandomPlayer. Epoch 0 training signal is weak
because random play doesn't pressure the agent to learn defensive timing or type selection.

**Initialization gap:** PPO starts from random weights. Human replays encode patterns like
"use your best super-effective move" that BC can teach in minutes of supervised training.

## Constraints

- **Compatibility**: Must not break existing train_all.py invocations (backward-compatible API only)
- **OBS_DIM**: Changing OBS_DIM invalidates saved model checkpoints — new training runs required
- **poke-env API**: MaxBasePowerPlayer exists in poke-env; verify exact class name before coding
- **Action mapping**: BC pre-training must map replay moves to the same 0-25 action space as PPO
- **Platform**: Training runs on GitHub Actions (Linux); local dev may be Windows

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Add 4 type-effectiveness floats (one per move slot) | Minimal obs expansion, directly encodes most important battle mechanic | — Pending |
| Use MaxBasePowerPlayer as curriculum opponent | Built into poke-env, zero external deps | — Pending |
| BC pre-training from replays initializes PPO | Replay data already scraped; BC is supervised so fast to train | — Pending |
| Keep BC as optional --pretrain flag | Backward compatible, lets existing workflows continue | — Pending |

---
*Last updated: 2026-03-17 after initialization*
