# Deployment Checklist

Quick reference for deploying the Pokemon Draft League Bot to production.

---

## Prerequisites (Both Platforms)

- [ ] Discord bot token from https://discord.com/developers/applications
- [ ] Google Sheets spreadsheet ID: `16F9FP5wkyzDdF8C7vD9xwY2j2JkcWYR1EUK_MtRt7zs`
- [ ] Google service account credentials.json
- [ ] Bot invited to Discord server with proper permissions
- [ ] All code synced to GitHub: https://github.com/NoChillModeOnline/NCLPDLB

---

## Option A: Fly.io Deployment (Free Tier)

**Cost:** $0/month for free tier

### 1. Install Fly CLI

```bash
# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh
```

### 2. Authenticate

```bash
flyctl auth login
# Opens browser for authentication
```

### 3. Create Apps

```bash
cd pokemon-draft-league-bot

# Create bot app
flyctl apps create pokemon-draft-bot

# Create API app
flyctl apps create pokemon-draft-api
```

### 4. Set Secrets (Bot)

```bash
# Encode credentials.json to base64
cat credentials.json | base64 > credentials.b64

# Set secrets
flyctl secrets set \
  DISCORD_TOKEN="YOUR_DISCORD_TOKEN_HERE" \
  DISCORD_CLIENT_ID="YOUR_CLIENT_ID_HERE" \
  GOOGLE_SHEETS_SPREADSHEET_ID="16F9FP5wkyzDdF8C7vD9xwY2j2JkcWYR1EUK_MtRt7zs" \
  GOOGLE_SHEETS_CREDENTIALS_B64="$(cat credentials.b64)" \
  --app pokemon-draft-bot
```

### 5. Set Secrets (API)

```bash
flyctl secrets set \
  DISCORD_TOKEN="YOUR_DISCORD_TOKEN_HERE" \
  GOOGLE_SHEETS_SPREADSHEET_ID="16F9FP5wkyzDdF8C7vD9xwY2j2JkcWYR1EUK_MtRt7zs" \
  GOOGLE_SHEETS_CREDENTIALS_B64="$(cat credentials.b64)" \
  --app pokemon-draft-api
```

### 6. Deploy

```bash
# Deploy bot
flyctl deploy --config fly.bot.toml --app pokemon-draft-bot

# Deploy API
flyctl deploy --config fly.api.toml --app pokemon-draft-api
```

### 7. Verify

```bash
# Check bot logs
flyctl logs --app pokemon-draft-bot

# Check API health
curl https://pokemon-draft-api.fly.dev/health

# Test in Discord
# Type /draft-setup in your Discord server
```

### 8. Monitor

```bash
# View dashboard
flyctl dashboard --app pokemon-draft-bot

# Check status
flyctl status --app pokemon-draft-bot
```

---

## Option B: Azure Deployment

**Cost:** ~$20-35/month (or free with Azure credits)

### 1. Set GitHub Secrets

Go to https://github.com/NoChillModeOnline/NCLPDLB/settings/secrets/actions

Add these secrets:

| Secret Name | Value | Where to Get |
|-------------|-------|--------------|
| `AZURE_CREDENTIALS` | Service principal JSON | See step 2 below |
| `ACR_NAME` | `pokemondraftacr` | Your Azure Container Registry name |
| `AZURE_RG` | `pokemon-draft-rg` | Your resource group name |
| `AZURE_STATIC_WEB_APPS_TOKEN` | Deployment token | Azure Static Web Apps portal |
| `DISCORD_TOKEN` | Your bot token | Discord Developer Portal |
| `AZURE_STORAGE_CONNECTION_STRING` | Connection string | Azure Storage Account |

### 2. Create Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name pokemon-draft-rg \
  --location eastus2

# Create container registry
az acr create \
  --name pokemondraftacr \
  --resource-group pokemon-draft-rg \
  --sku Basic

# Create service principal for GitHub Actions
az ad sp create-for-rbac \
  --name "github-deploy-pokemon-draft" \
  --role Contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/pokemon-draft-rg \
  --sdk-auth
# Copy the JSON output as AZURE_CREDENTIALS secret
```

### 3. Set GitHub Variable

Go to https://github.com/NoChillModeOnline/NCLPDLB/settings/variables/actions

Add variable:
- Name: `DEPLOY_TARGET`
- Value: `azure`

### 4. Deploy

```bash
# Trigger deployment by pushing to main
git push origin master
```

GitHub Actions will automatically:
1. Build Docker images
2. Push to Azure Container Registry
3. Deploy containers to Azure Container Instances
4. Deploy frontend to Azure Static Web Apps

### 5. Verify

```bash
# Check container logs
az container logs \
  --resource-group pokemon-draft-rg \
  --name pokemon-draft-bot

# Get API URL
az container show \
  --resource-group pokemon-draft-rg \
  --name pokemon-draft-api \
  --query ipAddress.fqdn -o tsv
```

---

## Option C: Local Docker (Testing)

**Use this to test before deploying to production**

### 1. Build Images

```bash
docker-compose build
```

### 2. Start Services

```bash
# Start bot and API
docker-compose up -d

# View logs
docker-compose logs -f bot
```

### 3. Test

```bash
# Check API health
curl http://localhost:8000/health

# Check bot logs
docker-compose logs bot | grep -i "ready"
```

### 4. Stop

```bash
docker-compose down
```

---

## Post-Deployment Tasks

### 1. Invite Bot to Discord Server

Use this URL (replace `YOUR_CLIENT_ID`):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=2147551232&scope=bot%20applications.commands
```

Required permissions:
- Send Messages
- Embed Links
- Attach Files
- Manage Roles
- Use Slash Commands

### 2. Test Core Commands

In Discord:
```
/draft-setup
/team
/standings
/help
```

### 3. Share Spreadsheet

Share the Google Sheet with your service account email:
1. Open https://docs.google.com/spreadsheets/d/16F9FP5wkyzDdF8C7vD9xwY2j2JkcWYR1EUK_MtRt7zs
2. Click "Share"
3. Add the email from credentials.json (client_email field)
4. Grant "Editor" access

### 4. Monitor First Week

- Check bot stays online (Fly.io dashboard or Azure portal)
- Monitor logs for errors
- Test all major commands
- Verify Google Sheets updates correctly

---

## Troubleshooting

### Bot Not Responding
```bash
# Fly.io
flyctl logs --app pokemon-draft-bot | grep -i error

# Azure
az container logs --resource-group pokemon-draft-rg --name pokemon-draft-bot
```

### Google Sheets Errors
1. Verify service account has Editor access
2. Check GOOGLE_SHEETS_SPREADSHEET_ID is correct
3. Verify credentials.json is valid

### Commands Not Appearing
1. Ensure bot has `applications.commands` scope
2. Wait 5-10 minutes for Discord to sync commands
3. Restart bot: `flyctl apps restart pokemon-draft-bot`

### API Not Accessible
```bash
# Check API is running
curl https://your-api-url/health

# Should return: {"status":"ok","pokemon_loaded":1025}
```

---

## ML Training (Optional - After Deployment)

If you want to add `/spar` command later:

### 1. Train Models Locally (Docker Required)

```bash
docker-compose run --rm bot python -m src.ml.train_all
```

This takes 8-12 hours and creates models in `data/ml/policy/`

### 2. Upload Models to Deployment

**Fly.io:**
```bash
# Create volume
flyctl volumes create bot_models --size 10 --app pokemon-draft-bot

# Upload models
flyctl ssh sftp shell --app pokemon-draft-bot
# Then: put -r data/ml/policy /app/data/ml/
```

**Azure:**
```bash
# Upload to blob storage
az storage blob upload-batch \
  --account-name pokemondraftstorage \
  --destination ml-models \
  --source data/ml/policy
```

### 3. Restart Bot

```bash
# Fly.io
flyctl apps restart pokemon-draft-bot

# Azure (redeploy)
git commit --allow-empty -m "Trigger redeploy"
git push origin master
```

---

## Costs Summary

### Fly.io (Free)
- Bot: Free (3 shared VMs)
- API: Free (512MB RAM)
- **Total: $0/month**

Paid upgrade if needed: ~$5/month for dedicated VMs

### Azure
- Container Registry: $5/month (Basic)
- Container Instances: $15-30/month (1 vCPU, 1.5GB RAM)
- Blob Storage: $0.20/month (~10GB)
- Static Web Apps: Free tier
- **Total: ~$20-35/month**

Free credits available: https://azure.microsoft.com/free
