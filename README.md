# Pokemon Draft League Bot

A full-featured Discord bot for running Pokemon draft leagues — supporting Pokemon Showdown and console games (Scarlet/Violet, Sword/Shield), with Google Sheets integration, a React web dashboard, ELO matchmaking, and dual deployment (free tier + Azure).

---

## Features

| Category | Details |
|----------|---------|
| **Draft Formats** | Snake, Auction, Tiered, Adaptive Banning — fully customizable |
| **Tera Captains** | Per-team tera captain limit + tera type assignment per pick |
| **Team Logos** | Upload PNG/JPG logos via `/team-register` — saved to Discord CDN + Sheets |
| **Pokemon Data** | All 1,025 Gen 1-9 Pokemon with animated sprites (Showdown CDN) |
| **Analytics** | Type coverage, weaknesses, speed tiers, team archetype, threat score |
| **ELO** | Per-league ratings (K=32), standings, streak tracking |
| **Battle Sim** | Heuristic matchup scoring, Showdown replay parsing |
| **Spreadsheet** | 17-tab Google Sheets backend (Setup, Draft, Standings, MVP Race, etc.) |
| **Web Dashboard** | React + Vite — live draft board, standings, team viewer, Pokemon search |
| **Deployment** | Free tier (Fly.io + Cloudflare) or Azure (ACI + Static Web Apps) |
| **Platform** | Windows 10+ / macOS 11+ / Linux — fully cross-platform |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker Desktop (optional but recommended)
- Google Cloud service account JSON
- Discord bot token

### 1. Clone & configure

```bash
git clone <your-repo>
cd pokemon-draft-league-bot
cp .env.example .env
# Edit .env with your tokens
```

### 2. Install Python dependencies

```bash
pip install uv
uv pip install -r requirements.txt
```

### 3. Seed Pokemon data

```bash
python scripts/seed_pokemon_data.py
```

This fetches all 1,025 Gen 1-9 Pokemon from PokéAPI and saves animated GIF sprite URLs.

### 4. Set up Google Sheets

```bash
python scripts/setup_google_sheet.py
```

Creates all 17 tabs with correct headers, formatting, and data validation dropdowns.

### 5. Run with Docker

```bash
docker compose up
```

Or run individually:

```bash
python src/bot/main.py       # Discord bot
uvicorn src.api.app:app --reload   # Web API
cd src/web && npm install && npm run dev   # React dashboard
```

---

## Discord Commands

### Draft Setup

| Command | Description | Permission |
|---------|-------------|------------|
| `/draft-setup` | Interactive wizard: league name, format, game mode, player count, tera captains | Manage Server |
| `/draft-create` | Quick create with inline options | Manage Server |
| `/draft-join [team_name] [pool] [logo]` | Join draft, set team name and upload logo | Anyone |
| `/draft-start` | Start the draft when all players are registered | Commissioner |
| `/draft-status` | Show current round, active player, pick count | Anyone |

### Picking

| Command | Description |
|---------|-------------|
| `/pick <pokemon> [tera_type] [is_tera_captain]` | Pick a Pokemon; optionally assign tera type and mark as captain |
| `/ban <pokemon>` | Ban a Pokemon during the ban phase |
| `/bid <amount>` | Place a bid during auction drafts |

### Team Management

| Command | Description |
|---------|-------------|
| `/team [user]` | View your or another player's team with analytics |
| `/team-register <team_name> [pool] [logo]` | Set team name, pool, and upload a logo image |
| `/teamimport` | Import a Pokemon Showdown team export (modal) |
| `/teamexport` | Export your team to Showdown format |
| `/trade <user> <offer> <want>` | Propose a trade |
| `/trade-accept <trade_id>` | Accept a pending trade |
| `/legality <pokemon> <game>` | Check if a Pokemon is legal in a format |

### Stats & Analysis

| Command | Description |
|---------|-------------|
| `/analysis [user]` | Full team analysis (coverage, weaknesses, archetypes, threat score) |
| `/matchup <user1> <user2>` | Compare two teams head-to-head |
| `/standings [pool]` | View league standings with ELO |
| `/replay <url>` | Submit a Showdown replay — auto-parses result and records to Sheets |
| `/match-upload <opponent> <file>` | Upload a capture card video for a match |

### League

| Command | Description |
|---------|-------------|
| `/league-create <name>` | Create a new league |
| `/schedule` | View this week's suggested matchups |
| `/result <opponent> <winner>` | Report a match result (updates ELO) |

### Spreadsheet Management (Manage Server only)

| Command | Description |
|---------|-------------|
| `/sheet-setup view/edit` | View or edit Setup tab values |
| `/sheet-standings` | Recalculate standings and write to Standings tab |
| `/sheet-schedule` | Add a match to the Schedule tab |
| `/sheet-result` | Record a match result to Match Stats tab |
| `/sheet-transaction` | Log a trade/drop/add to Transactions tab |
| `/sheet-rule` | Add a rule to the Rules tab |
| `/sheet-player` | Update a player's team name, pool, or logo |
| `/sheet-pokedex` | Sync all Pokemon data to the Pokedex tab |
| `/sheet-playoff` | Add a playoff match to Playoffs tab |

### Admin

| Command | Description |
|---------|-------------|
| `/admin-skip [player]` | Force-skip a player's turn |
| `/admin-pause` | Pause the draft |
| `/admin-resume` | Resume a paused draft |
| `/admin-override-pick <player> <pokemon>` | Override a pick as commissioner |
| `/admin-reset` | Reset the entire draft (with confirmation) |

### Machine Learning / Showdown

| Command | Description |
|---------|-------------|
| `/spar <format> [username]` | Battle the trained PPO agent live on Pokemon Showdown |

**Supported formats:**

- Gen 9: Random Battle, OU, Doubles OU, National Dex, Monotype, Anything Goes, VGC 2026 Reg I/F
- Gen 7/6: Random Battle

**Training the agents:**

```bash
# Train all formats sequentially (500k steps each, ~8-12 hours total)
python -m src.ml.train_all

# Train a specific format
python -m src.ml.train_policy --format gen9ou --timesteps 500000 --team-format gen9ou

# Doubles formats (VGC, Doubles OU) use BattleDoubleEnv automatically
python -m src.ml.train_policy --format gen9vgc2026regi --team-format gen9vgc2026regi
```

Models are saved to `data/ml/policy/<format>/final_model.zip`. The bot loads these when a user runs `/spar`.

---

## Architecture

```text
┌─────────────────┐
│  Discord Bot    │──┐
│  (Python 3.11)  │  │
└─────────────────┘  │
                     ├──► Google Sheets (17 tabs)
┌─────────────────┐  │
│  FastAPI Server │──┤
│  (REST+WebSocket)│  │
└─────────────────┘  │
         ▲           │
         │           ▼
┌─────────────────┐  ┌──────────────────┐
│  React Frontend │  │  poke-env        │
│  (Vite + TS)    │  │  Showdown Client │
└─────────────────┘  └──────────────────┘
         │                    │
         ▼                    ▼
  ┌──────────────┐   ┌─────────────────┐
  │ Static Web   │   │ Pokemon Showdown│
  │ Apps / Pages │   │ (play.pokemonshowdown.com)
  └──────────────┘   └─────────────────┘

Storage:
  ├─ SQLite (dev) / PostgreSQL (prod) — local state
  ├─ Google Sheets — draft logs, standings, team rosters
  ├─ Azure Blob / R2 — match videos, thumbnails
  └─ Local files — ML models (data/ml/policy/), Pokemon DB
```

**Key components:**

- **Discord Bot** — Commands, modals, views, embeds; cogs for draft/team/stats/admin/league
- **FastAPI** — REST endpoints + WebSocket for live draft board updates
- **React Dashboard** — Real-time draft spectating, standings, team viewer, Pokemon search
- **poke-env** — Python Showdown client for `/spar` battles with trained PPO agents
- **Google Sheets** — Single source of truth for league data (no SQL migrations needed)
- **ML Pipeline** — PPO (stable-baselines3) + custom Gym env for turn-based Showdown battles

---

## Google Sheets Structure

The bot connects to a spreadsheet with 17 tabs:

| Tab | Purpose |
|-----|---------|
| **Setup** | League config: name, format, pools, tera rules, commissioner |
| **Rules** | Rule reference (Tera Captains, trading rules, etc.) |
| **Cover** | Title/intro page |
| **Draft** | Full pick log: round, pick, pool, player, Pokemon, tera type, tier |
| **Draft Board** | Visual board summary (populated by bot) |
| **Pool A Board** | Pool A rosters |
| **Pool B Board** | Pool B rosters |
| **Schedule** | Match schedule with results |
| **Match Stats** | Full match records: teams used, replays, videos |
| **Standings** | W/L/ELO/streak per pool |
| **Pokemon Stats** | Per-Pokemon performance stats |
| **MVP Race** | Most impactful Pokemon leaderboard |
| **Transactions** | All trades, drops, adds |
| **Playoffs** | Bracket results |
| **Pokedex** | All 1,025 Pokemon reference data |
| **Team Page Template** | Per-player team page with logo URL |
| **Data** | Internal key/value store |

### Connecting the Bot to Your Spreadsheet

1. Create a Google Cloud project and enable the Sheets API
2. Create a service account and download `credentials.json`
3. Share your spreadsheet with the service account email
4. Add the spreadsheet ID to `.env`:

   ```text
   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
   ```

5. Run `python scripts/setup_google_sheet.py` to initialize all tabs

---

## Environment Variables

See [.env.example](.env.example) for all variables. Key ones:

```env
DISCORD_TOKEN=         # Bot token from Discord Developer Portal
DISCORD_CLIENT_ID=     # Application ID
DISCORD_GUILD_ID=      # Test server ID (for instant slash command sync)
BOT_NAME=DraftBot      # Display name in embeds and logs
BOT_STATUS=Pokemon Draft League

GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id

DEPLOY_TARGET=free     # "free" (Fly.io) or "azure"
```

---

## Deployment

### Free Tier (Default)

| Service | Provider | Cost |
|---------|---------|------|
| Bot | Fly.io | Free (3 shared VMs) |
| API | Fly.io | Free (512MB RAM) |
| Frontend | Cloudflare Pages | Free (unlimited) |
| Videos | Cloudflare R2 | Free (10GB) |
| Database | Google Sheets + SQLite | Free |

```bash
flyctl deploy --config fly.bot.toml
flyctl deploy --config fly.api.toml
```

### Azure (Production)

```bash
# Set DEPLOY_TARGET=azure in GitHub repo variables
# GitHub Actions will auto-deploy on push to main
```

Push to `main` — GitHub Actions runs tests then deploys to both targets based on `DEPLOY_TARGET`.

---

## Development

```bash
# Run tests
pytest tests/ -v

# Run specific suite
pytest tests/unit/ -v
pytest tests/e2e/ -v

# Load testing
locust -f tests/performance/locustfile.py --host http://localhost:8000

# Lint + type check
ruff check src/
mypy src/
```

---

## Troubleshooting

### Bot not responding to slash commands

- **Symptom:** Commands don't appear in Discord autocomplete
- **Fix:**
  1. Verify `DISCORD_TOKEN` and `DISCORD_CLIENT_ID` in `.env`
  2. Ensure bot has `applications.commands` scope when invited
  3. For instant sync, set `DISCORD_GUILD_ID` to your test server
  4. Restart the bot — slash commands register on startup

### Google Sheets permission denied

- **Symptom:** `gspread.exceptions.APIError: Insufficient permissions`
- **Fix:**
  1. Share the spreadsheet with the service account email (found in `credentials.json` → `client_email`)
  2. Grant **Editor** access, not Viewer
  3. Verify `GOOGLE_SHEETS_SPREADSHEET_ID` matches your sheet

### `/spar` command fails with "Model not found"

- **Symptom:** `/spar gen9ou` returns "No trained model found"
- **Fix:** Train the model first:

  ```bash
  python -m src.ml.train_policy --format gen9ou --team-format gen9ou --timesteps 500000
  ```

  Models must exist at `data/ml/policy/<format>/final_model.zip`

### Video uploads fail

- **Symptom:** `/match-upload` returns "Upload failed"
- **Fix:**
  1. Check file size (max 100MB by default)
  2. Verify storage backend is configured:
     - **R2:** Set `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`
     - **Azure:** Set `AZURE_STORAGE_CONNECTION_STRING`
  3. Ensure `ffmpeg` is installed for thumbnail generation

### Import errors on ARM64 Windows

- **Symptom:** `aiohttp` or `discord.py` fail to install
- **Fix:** Use Python 3.11 (not 3.14) or run via Docker (Linux containers have pre-built wheels)

### Draft hangs after `/draft-start`

- **Symptom:** No pick prompt appears
- **Fix:**
  1. Check bot has `Send Messages` + `Embed Links` permissions in the draft channel
  2. Verify player count matches setup (all slots filled)
  3. Check logs: `tail -f logs/bot.log`

### WebSocket connection refused on frontend

- **Symptom:** React dashboard shows "Connecting..." forever
- **Fix:**
  1. Ensure API is running: `uvicorn src.api.app:app --reload`
  2. Update `CORS_ORIGINS` in `.env` to include frontend URL
  3. Check firewall isn't blocking port 8000

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest tests/ -v`) and linter (`ruff check src/`)
4. Commit with clear messages
5. Open a pull request

---

## License

MIT
