# ☁️ Azure Deployment Guide

**Deploy your Pokemon Draft League Bot to Microsoft Azure**

---

## 📋 Overview

This guide covers deploying your bot to Azure using multiple services:
- **Azure App Service** - Host the Discord bot and web dashboard
- **Azure Functions** - Serverless bot deployment (alternative)
- **Azure Database for PostgreSQL** - Optional database upgrade from Google Sheets
- **Azure Storage** - Static file hosting for web assets
- **Azure Container Instances** - Docker-based deployment

**Cost:** Free tier available! ($0/month for small deployments)

---

## ⚡ Quick Start - Azure App Service (Recommended)

### Prerequisites
- Azure account (sign up at https://azure.microsoft.com/free)
- Azure CLI installed (optional but recommended)
- Your bot configured locally (`.credentials.json`)

### Method 1: Deploy via Azure Portal (Web Interface)

**Step 1: Create App Service**

1. Go to https://portal.azure.com
2. Click **"Create a resource"** → **"Web App"**
3. Configure:
   - **Subscription:** Your subscription
   - **Resource Group:** Create new → `pokemon-bot-rg`
   - **Name:** `pokemon-draft-bot` (must be unique)
   - **Publish:** Code
   - **Runtime stack:** Python 3.11
   - **Operating System:** Linux
   - **Region:** Choose closest to you
   - **Pricing Plan:** F1 (Free) or B1 (Basic - $13/month)

4. Click **"Review + Create"** → **"Create"**

**Step 2: Configure Application Settings**

1. Go to your App Service → **Configuration** → **Application settings**
2. Add these settings:
   ```
   DISCORD_BOT_TOKEN = your_discord_token
   SPREADSHEET_ID = your_google_sheet_id
   GOOGLE_SERVICE_ACCOUNT = paste_entire_service_account_json
   SCM_DO_BUILD_DURING_DEPLOYMENT = true
   ```

3. Click **"Save"**

**Step 3: Deploy Code**

Option A - Via Git (Recommended):
```bash
# Add Azure remote
git remote add azure https://pokemon-draft-bot.scm.azurewebsites.net:443/pokemon-draft-bot.git

# Deploy
git push azure master
```

Option B - Via ZIP Deploy:
```bash
# Create deployment package
zip -r deploy.zip . -x "*.git*" -x "*venv*" -x "*__pycache__*"

# Deploy via Azure CLI
az webapp deployment source config-zip \
  --resource-group pokemon-bot-rg \
  --name pokemon-draft-bot \
  --src deploy.zip
```

**Step 4: Start the Bot**

1. In Azure Portal → **Configuration** → **General settings**
2. Set **Startup Command:** `python bot.py`
3. Click **"Save"** and **"Restart"**

**Your bot is now live!** ✅

---

## 🐳 Method 2: Docker Container Deployment

### Create Dockerfile

Create `Dockerfile` in your project root:

```dockerfile
# Use official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for web dashboard
EXPOSE 5000

# Create startup script
COPY start.sh .
RUN chmod +x start.sh

# Run startup script
CMD ["./start.sh"]
```

### Create Startup Script

Create `start.sh`:

```bash
#!/bin/bash

# Start Discord bot in background
python bot.py &

# Start web dashboard in foreground
python web_server.py
```

### Deploy to Azure Container Instances

```bash
# Build Docker image
docker build -t pokemon-draft-bot .

# Login to Azure Container Registry
az acr login --name myregistry

# Tag and push image
docker tag pokemon-draft-bot myregistry.azurecr.io/pokemon-draft-bot:latest
docker push myregistry.azurecr.io/pokemon-draft-bot:latest

# Create container instance
az container create \
  --resource-group pokemon-bot-rg \
  --name pokemon-bot \
  --image myregistry.azurecr.io/pokemon-draft-bot:latest \
  --dns-name-label pokemon-draft-bot \
  --ports 5000 \
  --environment-variables \
    DISCORD_BOT_TOKEN=$DISCORD_TOKEN \
    SPREADSHEET_ID=$SHEET_ID
```

---

## ⚡ Method 3: Azure Functions (Serverless)

Perfect for lightweight, event-driven bots!

### Create Azure Function

**Step 1: Install Azure Functions Core Tools**

```bash
# Windows (via npm)
npm install -g azure-functions-core-tools@4

# Or via Chocolatey
choco install azure-functions-core-tools
```

**Step 2: Initialize Function App**

```bash
# Create function app
func init pokemon-bot-functions --python

cd pokemon-bot-functions

# Create HTTP trigger function
func new --name DiscordWebhook --template "HTTP trigger"
```

**Step 3: Update Function Code**

Edit `DiscordWebhook/__init__.py`:

```python
import azure.functions as func
import logging
import json
from discord_interactions import verify_key_decorator

# Your Discord public key
DISCORD_PUBLIC_KEY = "your_public_key"

@verify_key_decorator(DISCORD_PUBLIC_KEY)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Discord webhook triggered')

    try:
        body = req.get_json()

        # Handle Discord interactions
        if body.get('type') == 1:  # PING
            return func.HttpResponse(
                json.dumps({'type': 1}),
                mimetype='application/json'
            )

        # Handle your bot commands here
        # ... (implement your bot logic)

        return func.HttpResponse(
            json.dumps({'type': 4, 'data': {'content': 'Command processed!'}}),
            mimetype='application/json'
        )

    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return func.HttpResponse(
            "Error processing request",
            status_code=500
        )
```

**Step 4: Deploy to Azure**

```bash
# Login to Azure
az login

# Create function app
az functionapp create \
  --resource-group pokemon-bot-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name pokemon-bot-functions \
  --storage-account pokemonstorageacct

# Deploy function
func azure functionapp publish pokemon-bot-functions
```

---

## 🗄️ Method 4: Upgrade to Azure PostgreSQL

Replace Google Sheets with Azure Database for better performance!

### Create Azure PostgreSQL Database

```bash
# Create PostgreSQL server
az postgres flexible-server create \
  --resource-group pokemon-bot-rg \
  --name pokemon-draft-db \
  --location eastus \
  --admin-user dbadmin \
  --admin-password YourSecurePassword123! \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 15

# Create database
az postgres flexible-server db create \
  --resource-group pokemon-bot-rg \
  --server-name pokemon-draft-db \
  --database-name pokemon_league
```

### Update Bot Configuration

Create `azure_config.py`:

```python
import os
import psycopg2

# Azure PostgreSQL connection
DATABASE_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'pokemon-draft-db.postgres.database.azure.com'),
    'database': os.getenv('POSTGRES_DB', 'pokemon_league'),
    'user': os.getenv('POSTGRES_USER', 'dbadmin'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'sslmode': 'require'
}

def get_db_connection():
    """Get PostgreSQL database connection"""
    return psycopg2.connect(**DATABASE_CONFIG)
```

### Migration Script

Create `migrate_to_azure.py`:

```python
"""Migrate from Google Sheets to Azure PostgreSQL"""
import psycopg2
from services.sheets_service import SheetsService
import config

def migrate_data():
    """Migrate all data from Sheets to PostgreSQL"""

    # Connect to Azure PostgreSQL
    conn = psycopg2.connect(
        host='pokemon-draft-db.postgres.database.azure.com',
        database='pokemon_league',
        user='dbadmin',
        password='YourPassword',
        sslmode='require'
    )
    cur = conn.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            tier VARCHAR(10),
            type1 VARCHAR(20),
            type2 VARCHAR(20),
            hp INTEGER,
            attack INTEGER,
            defense INTEGER,
            sp_attack INTEGER,
            sp_defense INTEGER,
            speed INTEGER,
            point_cost INTEGER
        );

        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            player VARCHAR(100) UNIQUE NOT NULL,
            team_name VARCHAR(100),
            team_logo TEXT,
            total_points_used INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS rosters (
            id SERIAL PRIMARY KEY,
            team_id INTEGER REFERENCES teams(id),
            pokemon_name VARCHAR(100),
            point_cost INTEGER
        );

        CREATE TABLE IF NOT EXISTS tera_captains (
            id SERIAL PRIMARY KEY,
            team_id INTEGER REFERENCES teams(id),
            pokemon_name VARCHAR(100),
            tera_type VARCHAR(20),
            point_cost INTEGER
        );
    """)

    # Migrate Pokemon data
    sheets = SheetsService(config.CONFIG['spreadsheet_id'])
    pokemon_data = sheets.get_all_pokemon()

    for pokemon in pokemon_data:
        cur.execute("""
            INSERT INTO pokemon (name, tier, type1, type2, hp, attack, defense, sp_attack, sp_defense, speed, point_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
        """, (
            pokemon['name'],
            pokemon['tier'],
            pokemon['type1'],
            pokemon.get('type2'),
            pokemon['hp'],
            pokemon['attack'],
            pokemon['defense'],
            pokemon['sp_attack'],
            pokemon['sp_defense'],
            pokemon['speed'],
            pokemon['point_cost']
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Migration completed successfully!")

if __name__ == '__main__':
    migrate_data()
```

---

## 💰 Azure Pricing (Free Tier Options)

### App Service
- **F1 (Free):** 1 GB RAM, 1 GB storage, 60 CPU minutes/day
- **B1 (Basic):** $13/month, 1.75 GB RAM, 10 GB storage, always on
- **Recommended:** B1 for production

### Azure Functions
- **Consumption Plan:** First 1M executions free
- **Premium Plan:** $169/month (better performance)
- **Recommended:** Consumption for low traffic

### PostgreSQL
- **Burstable B1ms:** $12/month, 1 vCore, 2 GB RAM, 32 GB storage
- **Free tier:** Not available, but B1ms is cheapest
- **Alternative:** Keep Google Sheets (free!)

### Container Instances
- **Pricing:** ~$45/month for 1 vCore, 1.5 GB RAM
- **Not recommended:** More expensive than App Service

### Storage
- **Free tier:** 5 GB storage, 20,000 operations
- **Cost:** Minimal for static files

**Recommended Setup for Free/Low Cost:**
- App Service F1 (Free) or B1 ($13/month)
- Keep Google Sheets (Free)
- Azure Storage for static files (Free tier)
- **Total:** $0-13/month

---

## 🔧 Azure Configuration Files

### Create `azure-requirements.txt`

```txt
# Standard requirements
discord.py==2.6.4
gspread==6.1.4
google-auth==2.37.0
Flask==3.1.0

# Azure-specific packages
azure-identity==1.19.0
azure-storage-blob==12.24.0
psycopg2-binary==2.9.10
gunicorn==23.0.0
```

### Create `startup.txt` (Azure App Service)

```bash
#!/bin/bash

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (if using PostgreSQL)
# python migrate_to_azure.py

# Start bot
python bot.py
```

### Create `.deployment` (Azure deployment config)

```ini
[config]
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

---

## 🚀 Deployment Checklist

- [ ] Create Azure account
- [ ] Choose deployment method (App Service recommended)
- [ ] Create resource group
- [ ] Create App Service or Function App
- [ ] Configure environment variables
- [ ] Deploy code (Git or ZIP)
- [ ] Configure startup command
- [ ] Test bot functionality
- [ ] (Optional) Set up custom domain
- [ ] (Optional) Enable Application Insights for monitoring
- [ ] (Optional) Configure auto-scaling

---

## 📊 Monitoring & Logging

### Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app pokemon-bot-insights \
  --location eastus \
  --resource-group pokemon-bot-rg

# Link to App Service
az webapp config appsettings set \
  --name pokemon-draft-bot \
  --resource-group pokemon-bot-rg \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=your_key
```

### View Logs

```bash
# Stream live logs
az webapp log tail \
  --name pokemon-draft-bot \
  --resource-group pokemon-bot-rg

# Download logs
az webapp log download \
  --name pokemon-draft-bot \
  --resource-group pokemon-bot-rg \
  --log-file logs.zip
```

---

## 🔒 Security Best Practices

### Use Azure Key Vault

```bash
# Create Key Vault
az keyvault create \
  --name pokemon-bot-vault \
  --resource-group pokemon-bot-rg \
  --location eastus

# Store secrets
az keyvault secret set \
  --vault-name pokemon-bot-vault \
  --name discord-token \
  --value your_discord_token

# Reference in App Service
az webapp config appsettings set \
  --name pokemon-draft-bot \
  --resource-group pokemon-bot-rg \
  --settings DISCORD_BOT_TOKEN=@Microsoft.KeyVault(SecretUri=https://pokemon-bot-vault.vault.azure.net/secrets/discord-token/)
```

### Enable Managed Identity

```bash
# Enable system-assigned identity
az webapp identity assign \
  --name pokemon-draft-bot \
  --resource-group pokemon-bot-rg

# Grant Key Vault access
az keyvault set-policy \
  --name pokemon-bot-vault \
  --object-id <identity-principal-id> \
  --secret-permissions get list
```

---

## 🌐 Custom Domain Setup

```bash
# Map custom domain
az webapp config hostname add \
  --webapp-name pokemon-draft-bot \
  --resource-group pokemon-bot-rg \
  --hostname bot.yourdomain.com

# Enable HTTPS
az webapp config ssl bind \
  --certificate-thumbprint <thumbprint> \
  --ssl-type SNI \
  --name pokemon-draft-bot \
  --resource-group pokemon-bot-rg
```

---

## 🔄 CI/CD with GitHub Actions

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [ master ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: pokemon-draft-bot
        publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
```

---

## 🆘 Troubleshooting

### Bot not starting

Check logs:
```bash
az webapp log tail --name pokemon-draft-bot --resource-group pokemon-bot-rg
```

Common issues:
- Missing environment variables
- Incorrect startup command
- Port binding issues (use `0.0.0.0` not `localhost`)

### Database connection fails

- Check firewall rules allow Azure services
- Verify connection string is correct
- Enable SSL requirement

### High costs

- Use F1 free tier for testing
- Stop resources when not needed
- Monitor usage in Azure Portal

---

## 📚 Additional Resources

- [Azure App Service Docs](https://docs.microsoft.com/azure/app-service/)
- [Azure Functions Docs](https://docs.microsoft.com/azure/azure-functions/)
- [Azure PostgreSQL Docs](https://docs.microsoft.com/azure/postgresql/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)

---

## ✅ Summary

**Recommended Azure Setup:**

1. **For Beginners:** App Service F1 (Free)
2. **For Production:** App Service B1 ($13/month)
3. **For Scale:** Functions + PostgreSQL ($25-50/month)

**Keep it Free:**
- Use F1 App Service tier
- Keep Google Sheets (don't migrate to PostgreSQL)
- Use Azure Storage free tier

**Your bot will be:**
- ✅ Globally accessible
- ✅ Auto-scaling
- ✅ Highly available
- ✅ Professionally hosted

---

**Ready to deploy?** Start with App Service F1 (free) and upgrade as needed!
