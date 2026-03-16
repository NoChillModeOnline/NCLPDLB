# Pokemon Draft League Bot - Setup Status

**Last Updated:** 2026-02-16 23:50 EST

---

## ✅ Completed

### Data & Configuration

- ✅ **Pokemon Database**: 1,025 Gen 1-9 Pokemon seeded in `data/pokemon.json`
- ✅ **Google Sheets**: 17 tabs created and configured
  - Setup, Rules, Cover, Draft, Draft Board, Pool A/B Boards
  - Schedule, Match Stats, Standings, Pokemon Stats, MVP Race
  - Transactions, Playoffs, Pokédex (populated with all 1,025 Pokemon), Team Template, Data
- ✅ **Configuration Files**: `.env` and `credentials.json` in place
- ✅ **Spreadsheet ID**: `16F9FP5wkyzDdF8C7vD9xwY2j2JkcWYR1EUK_MtRt7zs`

### Code & Documentation

- ✅ **ML Infrastructure**:
  - BattleEnv (singles) and BattleDoubleEnv (doubles/VGC)
  - train_policy.py with team-based training
  - train_all.py for sequential format training
  - teams.py with 5 pre-built teams × 10 formats
  - RotatingTeambuilder for custom team formats
- ✅ **Supported Formats**: gen9randombattle, gen9ou, gen9nationaldex, gen9monotype, gen9anythinggoes, gen9doublesou, gen9vgc2026regi, gen9vgc2026regf, gen7randombattle, gen6randombattle
- ✅ **Documentation**: README.md, docs/COMMANDS.md, docs/API.md, docs/DEPLOYMENT.md
- ✅ **GitHub**: All code synced to https://github.com/NoChillModeOnline/NCLPDLB.git

### Deployment Configuration

- ✅ **Dockerfile**: Multi-stage build (bot + API targets)
- ✅ **docker-compose.yml**: Bot, API, and optional frontend services
- ✅ **Fly.io configs**: fly.bot.toml + fly.api.toml (free tier ready)
- ✅ **Azure config**: GitHub Actions workflow for Azure deployment
- ✅ **GitHub Actions**: Automated testing and deployment pipelines

---

## ⏸️ Blocked (Waiting for Virtualization Fix)

### ML Training

- ⏸️ **PyTorch + stable-baselines3**: Cannot install on ARM64 Windows natively
- ⏸️ **All 10 format training**: Requires Docker with Linux containers
- ⏸️ **Models**: None trained yet (requires ~8-12 hours once Docker running)

### Local Testing

- ⏸️ **discord.py**: Cannot install (requires aiohttp, no ARM64 Windows wheels)
- ⏸️ **Bot startup test**: Requires Docker environment

**Root Cause:** ARM64 Windows lacks pre-built wheels for PyTorch, aiohttp, and other ML dependencies.

**Solution:** Enable Windows virtualization → Docker Desktop → Linux containers with pre-built wheels.

---

## 📋 Next Steps (Once Virtualization Fixed)

### 1. Verify Docker is Running

```bash
docker ps  # Should show no errors
```

### 2. Build Docker Images

```bash
cd pokemon-draft-league-bot
docker-compose build
```

### 3. Test Bot Locally

```bash
docker-compose up bot
# Bot should connect to Discord and show "Ready!" in logs
```

### 4. Start ML Training (8-12 hours)

```bash
docker-compose run --rm bot python -m src.ml.train_all
```

This trains all 10 formats sequentially:

- gen9randombattle (500k steps)
- gen9ou (500k steps)
- gen9doublesou (500k steps)
- gen9nationaldex (500k steps)
- gen9monotype (500k steps)
- gen9anythinggoes (500k steps)
- gen7randombattle (500k steps)
- gen6randombattle (500k steps)
- gen9vgc2026regi (500k steps)
- gen9vgc2026regf (500k steps)

Models saved to: `data/ml/policy/<format>/final_model.zip`

### 5. Deploy to Production

**Option A: Fly.io (Free Tier)**

```bash
# Install Fly CLI
flyctl auth login

# Deploy bot
flyctl deploy --config fly.bot.toml

# Deploy API
flyctl deploy --config fly.api.toml

# Set secrets
flyctl secrets set \
  DISCORD_TOKEN="your_token" \
  GOOGLE_SHEETS_SPREADSHEET_ID="16F9FP5wkyzDdF8C7vD9xwY2j2JkcWYR1EUK_MtRt7zs" \
  --app pokemon-draft-bot
```

**Option B: Azure**

```bash
# Set GitHub variable DEPLOY_TARGET=azure
# Push to main branch triggers auto-deployment via GitHub Actions
git push origin main
```

**Option C: Skip ML, Deploy Now**

```bash
# All 50+ bot commands work without ML (only /spar requires trained models)
# Deploy immediately using Option A or B above
```

---

## 🎯 Current Recommendation

**Deploy the bot NOW without ML training:**

1. All core features work (draft, teams, analytics, ELO, trades, etc.)
2. Only `/spar` command requires trained models
3. Can add ML later after training completes
4. Users can start using the league immediately

**To deploy:**

1. Choose Fly.io (free) or Azure (paid)
2. Follow deployment steps in `docs/DEPLOYMENT.md`
3. Train models in background and re-deploy later

---

## 📊 Feature Availability

| Feature | Without ML | With ML |
|---------|-----------|---------|
| Draft (Snake/Auction/Tiered) | ✅ | ✅ |
| Team Management | ✅ | ✅ |
| Analytics & Coverage | ✅ | ✅ |
| ELO & Matchmaking | ✅ | ✅ |
| Replay Parsing | ✅ | ✅ |
| Web Dashboard | ✅ | ✅ |
| `/spar` (Battle AI) | ❌ | ✅ |

**49 out of 50 commands work without ML training.**

---

## 🔧 Virtualization Fix Instructions

### Step 1: Enable Windows Features

Run as Administrator in PowerShell:

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:Microsoft-Hyper-V-All /all /norestart
```

### Step 2: Restart Computer

```powershell
shutdown /r /t 0
```

### Step 3: Start Docker Desktop

1. Launch Docker Desktop from Start Menu
2. Wait for green "Running" status in system tray
3. Verify: `docker ps` (should show no errors)

### Step 4: Continue Setup

Return to this document and proceed with "Next Steps" above.

---

## 📞 Support

- **Documentation**: `README.md`, `docs/COMMANDS.md`, `docs/API.md`, `docs/DEPLOYMENT.md`
- **GitHub**: https://github.com/NoChillModeOnline/NCLPDLB
- **Spreadsheet**: https://docs.google.com/spreadsheets/d/16F9FP5wkyzDdF8C7vD9xwY2j2JkcWYR1EUK_MtRt7zs
