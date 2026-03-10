# Deployment Guide

Step-by-step instructions for deploying the Pokemon Draft League Bot to Azure or Fly.io (free tier).

---

## Prerequisites (Both Paths)

1. **Discord Bot Setup:**
   - Create application at https://discord.com/developers/applications
   - Create bot user and copy token
   - Enable **Message Content Intent** and **Server Members Intent**
   - Invite bot with scopes: `bot` + `applications.commands`
   - Required permissions: Send Messages, Embed Links, Attach Files, Manage Roles

2. **Google Sheets Setup:**
   - Create Google Cloud project: https://console.cloud.google.com
   - Enable **Google Sheets API**
   - Create service account → download `credentials.json`
   - Create a new Google Sheet
   - Share it with the service account email (Editor access)
   - Copy the spreadsheet ID from the URL

3. **Pokemon Data Seed:**
   ```bash
   python scripts/seed_pokemon_data.py
   ```
   Creates `data/pokemon.json` with all 1,025 Gen 1-9 Pokemon.

4. **Google Sheets Initialization:**
   ```bash
   python scripts/setup_google_sheet.py
   ```
   Creates all 17 tabs with headers and formatting.

---

## Path A: Free Tier (Fly.io + Cloudflare)

**Total cost:** $0/month

### 1. Install Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### 2. Sign up and authenticate

```bash
flyctl auth signup
# Or login if you have an account:
flyctl auth login
```

### 3. Deploy the Discord bot

```bash
flyctl deploy --config fly.bot.toml
```

**First deployment will prompt you to:**
- Create an app name (e.g., `my-draft-bot`)
- Choose a region (select closest to your users)
- Set up secrets

### 4. Configure secrets

```bash
flyctl secrets set \
  DISCORD_TOKEN="your_discord_token" \
  DISCORD_CLIENT_ID="your_client_id" \
  GOOGLE_SHEETS_SPREADSHEET_ID="your_sheet_id" \
  --app my-draft-bot
```

**Upload Google credentials:**
```bash
# Encode credentials.json to base64
cat credentials.json | base64 > credentials.b64

# Set as secret
flyctl secrets set GOOGLE_SHEETS_CREDENTIALS_B64="$(cat credentials.b64)" --app my-draft-bot
```

Update `src/data/sheets.py` to decode base64 credentials if `GOOGLE_SHEETS_CREDENTIALS_B64` is set.

### 5. Deploy the API

```bash
flyctl deploy --config fly.api.toml
```

```bash
flyctl secrets set \
  DISCORD_TOKEN="your_token" \
  GOOGLE_SHEETS_SPREADSHEET_ID="your_sheet_id" \
  --app my-draft-api
```

### 6. Set up Cloudflare R2 (video storage)

1. Create Cloudflare account: https://dash.cloudflare.com
2. Go to R2 Object Storage → Create bucket: `pokemon-draft-videos`
3. Create API token with R2 permissions
4. Add secrets to Fly:

```bash
flyctl secrets set \
  R2_ACCOUNT_ID="your_account_id" \
  R2_ACCESS_KEY_ID="your_key" \
  R2_SECRET_ACCESS_KEY="your_secret" \
  R2_BUCKET_NAME="pokemon-draft-videos" \
  R2_PUBLIC_URL="https://pub-xxxxx.r2.dev" \
  --app my-draft-bot
```

### 7. Deploy frontend to Cloudflare Pages

```bash
cd src/web
npm install
npm run build
```

1. Go to Cloudflare Pages → Create project
2. Connect your GitHub repo
3. Build settings:
   - Framework: Vite
   - Build command: `cd src/web && npm run build`
   - Output directory: `src/web/dist`
4. Environment variables:
   - `VITE_API_URL`: `https://my-draft-api.fly.dev`

### 8. Verify deployment

```bash
# Check bot logs
flyctl logs --app my-draft-bot

# Check API health
curl https://my-draft-api.fly.dev/health

# Visit frontend
# https://pokemon-draft-league.pages.dev
```

---

## Path B: Azure (Production)

**Estimated cost:** ~$20-35/month

### 1. Install Azure CLI

```bash
# macOS
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Windows
winget install Microsoft.AzureCLI
```

### 2. Login and set subscription

```bash
az login
az account set --subscription "Your Subscription Name"
```

### 3. Create resource group

```bash
az group create \
  --name pokemon-draft-rg \
  --location eastus2
```

### 4. Create Azure Container Registry

```bash
az acr create \
  --name pokemondraftacr \
  --resource-group pokemon-draft-rg \
  --sku Basic
```

### 5. Create Azure Blob Storage (for videos)

```bash
# Create storage account
az storage account create \
  --name pokemondraftstorage \
  --resource-group pokemon-draft-rg \
  --location eastus2 \
  --sku Standard_LRS

# Create container
az storage container create \
  --name match-videos \
  --account-name pokemondraftstorage \
  --public-access off

# Get connection string
az storage account show-connection-string \
  --name pokemondraftstorage \
  --resource-group pokemon-draft-rg
```

Save the connection string for later.

### 6. Create Azure Static Web Apps (frontend)

```bash
az staticwebapp create \
  --name pokemon-draft-frontend \
  --resource-group pokemon-draft-rg \
  --location eastus2
```

Get the deployment token:
```bash
az staticwebapp secrets list \
  --name pokemon-draft-frontend \
  --resource-group pokemon-draft-rg \
  --query "properties.apiKey" -o tsv
```

### 7. Set up GitHub Actions secrets

Go to your GitHub repo → Settings → Secrets and variables → Actions

**Add these secrets:**

| Secret | Value | How to get |
|--------|-------|------------|
| `AZURE_CREDENTIALS` | Service principal JSON | See step 8 below |
| `ACR_NAME` | `pokemondraftacr` | Your ACR name |
| `AZURE_RG` | `pokemon-draft-rg` | Your resource group |
| `AZURE_STATIC_WEB_APPS_TOKEN` | From step 6 | Deployment token |
| `DISCORD_TOKEN` | Your Discord bot token | Discord Developer Portal |
| `AZURE_STORAGE_CONNECTION_STRING` | From step 5 | Connection string |

### 8. Create service principal for GitHub Actions

```bash
az ad sp create-for-rbac \
  --name "github-deploy-pokemon-draft" \
  --role Contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/pokemon-draft-rg \
  --sdk-auth
```

Copy the entire JSON output and save as `AZURE_CREDENTIALS` secret.

### 9. Set GitHub variable

Go to Settings → Secrets and variables → Actions → Variables

Add variable:
- Name: `DEPLOY_TARGET`
- Value: `azure`

### 10. Push to trigger deployment

```bash
git add .
git commit -m "Deploy to Azure"
git push origin main
```

GitHub Actions will:
1. Build Docker images
2. Push to Azure Container Registry
3. Deploy bot to Azure Container Instances
4. Deploy frontend to Azure Static Web Apps

### 11. Upload credentials to Azure

Since ACI can't mount secrets as files easily, upload `credentials.json` to Blob Storage or Azure Key Vault:

**Option A: Blob Storage**
```bash
az storage blob upload \
  --account-name pokemondraftstorage \
  --container-name config \
  --name credentials.json \
  --file credentials.json
```

Update bot to download from blob on startup.

**Option B: Key Vault** (recommended)
```bash
# Create Key Vault
az keyvault create \
  --name pokemon-draft-kv \
  --resource-group pokemon-draft-rg \
  --location eastus2

# Store credentials as secret
az keyvault secret set \
  --vault-name pokemon-draft-kv \
  --name google-credentials \
  --file credentials.json
```

Update bot to fetch from Key Vault using managed identity.

### 12. Configure environment variables in ACI

```bash
az container create \
  --resource-group pokemon-draft-rg \
  --name pokemon-draft-bot \
  --image pokemondraftacr.azurecr.io/pokemon-draft-bot:latest \
  --registry-login-server pokemondraftacr.azurecr.io \
  --registry-username pokemondraftacr \
  --registry-password $(az acr credential show -n pokemondraftacr --query "passwords[0].value" -o tsv) \
  --cpu 1 \
  --memory 1.5 \
  --environment-variables \
    DEPLOY_TARGET=azure \
    GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id \
  --secure-environment-variables \
    DISCORD_TOKEN=your_discord_token \
    AZURE_STORAGE_CONNECTION_STRING="your_connection_string"
```

### 13. Verify deployment

```bash
# Check bot logs
az container logs \
  --resource-group pokemon-draft-rg \
  --name pokemon-draft-bot

# Check static web app URL
az staticwebapp show \
  --name pokemon-draft-frontend \
  --resource-group pokemon-draft-rg \
  --query "defaultHostname" -o tsv
```

---

## Post-Deployment

### 1. Test bot commands

In Discord:
```
/draft-setup
/team
/standings
```

### 2. Train ML models (optional)

SSH into your deployment or run locally, then upload models to persistent storage:

```bash
# Train all formats (8-12 hours)
python -m src.ml.train_all

# Upload to Azure Blob
az storage blob upload-batch \
  --account-name pokemondraftstorage \
  --destination ml-models \
  --source data/ml/policy
```

Update bot to download models from blob storage on startup.

### 3. Set up monitoring

**Fly.io:**
```bash
flyctl dashboard --app my-draft-bot
```

**Azure:**
- Enable Application Insights on your ACI
- Set up alerts for container restarts or high memory usage

### 4. Database backup (if using PostgreSQL)

**Azure:**
```bash
az postgres flexible-server backup create \
  --resource-group pokemon-draft-rg \
  --name your-db-server \
  --backup-name manual-backup-$(date +%Y%m%d)
```

---

## Troubleshooting

### Fly.io: "Out of memory"

Increase memory allocation in `fly.toml`:
```toml
[vm]
  memory = '512mb'  # Default is 256mb
```

### Azure: "Image pull failed"

Enable admin user on ACR:
```bash
az acr update --name pokemondraftacr --admin-enabled true
```

### Bot not connecting to Discord

Check token is set correctly:
```bash
# Fly
flyctl secrets list --app my-draft-bot

# Azure
az container show \
  --resource-group pokemon-draft-rg \
  --name pokemon-draft-bot \
  --query "containers[0].environmentVariables"
```

### Google Sheets "Permission denied"

Verify service account email has Editor access to the spreadsheet.

---

## Updating Deployment

### Fly.io

```bash
# Bot
flyctl deploy --config fly.bot.toml

# API
flyctl deploy --config fly.api.toml
```

### Azure

Just push to `main` — GitHub Actions auto-deploys.

```bash
git add .
git commit -m "Update feature X"
git push origin main
```

---

## Costs

### Fly.io (Free Tier)

- Bot: Free (3 shared VMs, 256MB RAM)
- API: Free (512MB RAM)
- Cloudflare Pages: Free (unlimited bandwidth)
- Cloudflare R2: Free (10GB storage)
- **Total: $0/month**

Upgrade to paid if you exceed free tier limits.

### Azure

- Container Registry (Basic): $5/month
- Container Instances (1 vCPU, 1.5GB RAM): $15-30/month
- Blob Storage (~10GB): $0.20/month
- Static Web Apps: Free tier
- **Total: ~$20-35/month**

Add ~$25/month if using Azure Database for PostgreSQL.

---

## Rollback

### Fly.io

```bash
# List releases
flyctl releases --app my-draft-bot

# Rollback to previous
flyctl releases rollback --app my-draft-bot
```

### Azure

Redeploy a previous commit:
```bash
git revert HEAD
git push origin main
```

Or manually update ACI to use an older image tag.
