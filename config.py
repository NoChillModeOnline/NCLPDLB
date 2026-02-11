"""
Configuration loader for Pokemon Draft Bot.

Loads credentials from .credentials.json and exports configuration constants.
"""

import json
import os
import sys
from pathlib import Path


class Config:
    """Configuration manager for bot credentials and settings"""

    def __init__(self, credentials_path=".credentials.json"):
        """
        Initialize configuration from credentials file.

        Args:
            credentials_path: Path to credentials JSON file (default: .credentials.json)
        """
        self.credentials_path = Path(credentials_path)
        self._load_credentials()

    def _load_credentials(self):
        """Load and validate credentials from JSON file"""
        if not self.credentials_path.exists():
            print(f"❌ Error: Credentials file not found at {self.credentials_path}")
            print("\nPlease create a .credentials.json file with:")
            print("""{
    "discord_bot_token": "YOUR_DISCORD_BOT_TOKEN",
    "spreadsheet_id": "YOUR_GOOGLE_SHEET_ID"
}""")
            sys.exit(1)

        try:
            with open(self.credentials_path, "r", encoding="utf-8") as f:
                creds = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in {self.credentials_path}")
            print(f"Details: {e}")
            sys.exit(1)

        # Validate required fields
        required_fields = ["discord_bot_token", "spreadsheet_id"]
        missing = [field for field in required_fields if field not in creds]

        if missing:
            print(f"❌ Error: Missing required fields in {self.credentials_path}")
            print(f"Missing: {', '.join(missing)}")
            sys.exit(1)

        # Set credentials as attributes
        self.discord_token = creds["discord_bot_token"]
        self.spreadsheet_id = creds["spreadsheet_id"]

        # Optional: Google service account credentials
        # If not provided in separate file, look for it in credentials
        self.google_creds_path = creds.get("google_credentials_path", ".credentials.json")

    def validate(self):
        """Validate that all required credentials are present"""
        if not self.discord_token or self.discord_token == "YOUR_DISCORD_BOT_TOKEN":
            print("❌ Error: Discord bot token not configured")
            return False

        if not self.spreadsheet_id or self.spreadsheet_id == "YOUR_GOOGLE_SHEET_ID":
            print("❌ Error: Google Spreadsheet ID not configured")
            return False

        return True


# Create global config instance
try:
    config = Config()
    if not config.validate():
        print("\n⚠️ Configuration validation failed!")
        print("Please update .credentials.json with your actual credentials.")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error loading configuration: {e}")
    sys.exit(1)

# Export configuration constants
DISCORD_TOKEN = config.discord_token
SPREADSHEET_ID = config.spreadsheet_id
GOOGLE_CREDS_PATH = config.google_creds_path

# Bot settings
COMMAND_PREFIX = "!"
BOT_DESCRIPTION = "Pokemon Draft League Management Bot"

# League settings (can be overridden by Config sheet)
DEFAULT_TOTAL_POINTS = 120
DEFAULT_MIN_POKEMON = 10
DEFAULT_MAX_POKEMON = 12
DEFAULT_MAX_TERA_CAPTAINS = 3
DEFAULT_MAX_TERA_POINTS = 25

# Draft settings
PICK_TIMEOUT_SECONDS = 300  # 5 minutes

print("✅ Configuration loaded successfully")
print(f"   - Spreadsheet ID: {SPREADSHEET_ID[:20]}...")
print(f"   - Command Prefix: {COMMAND_PREFIX}")
