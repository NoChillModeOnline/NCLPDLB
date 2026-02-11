#!/bin/bash
# Azure App Service Startup Script
# This script runs when the app starts on Azure

echo "================================================"
echo "  Pokemon Draft League Bot - Azure Startup"
echo "================================================"

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if credentials are configured via environment variables
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    echo "WARNING: DISCORD_BOT_TOKEN not set!"
fi

if [ -z "$SPREADSHEET_ID" ]; then
    echo "WARNING: SPREADSHEET_ID not set!"
fi

# Create .credentials.json from environment variables if provided
if [ -n "$DISCORD_BOT_TOKEN" ] && [ -n "$SPREADSHEET_ID" ]; then
    echo "Creating .credentials.json from environment variables..."
    cat > .credentials.json <<EOF
{
    "discord_bot_token": "$DISCORD_BOT_TOKEN",
    "spreadsheet_id": "$SPREADSHEET_ID"
}
EOF
fi

# Create service account JSON if provided
if [ -n "$GOOGLE_SERVICE_ACCOUNT" ]; then
    echo "Creating service-account.json from environment variable..."
    echo "$GOOGLE_SERVICE_ACCOUNT" > service-account.json
fi

echo "================================================"
echo "  Starting Pokemon Draft League Bot"
echo "================================================"

# Start the bot
python bot.py
