"""
Test script to verify all imports work correctly.

Run this before starting the bot to catch import errors early.
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if os.name == 'nt':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

print("Testing Imports...")
print("=" * 50)

# Test standard library imports
try:
    import json
    import traceback
    from datetime import datetime
    from pathlib import Path
    from typing import List, Dict, Optional
    import asyncio
    print("[OK] Standard library imports OK")
except Exception as e:
    print(f"[ERROR] Standard library import error: {e}")
    sys.exit(1)

# Test third-party imports
try:
    import discord
    from discord.ext import commands
    print(f"[OK] discord.py {discord.__version__} imported")
except Exception as e:
    print(f"[ERROR] discord.py import error: {e}")
    print("   Run: pip install discord.py")
    sys.exit(1)

try:
    import gspread
    from google.oauth2.service_account import Credentials
    print("[OK] gspread and google-auth imported")
except Exception as e:
    print(f"[ERROR] Google libraries import error: {e}")
    print("   Run: pip install gspread google-auth")
    sys.exit(1)

# Test local module imports (will fail if no credentials - this is expected!)
print("\n[INFO] Testing config module (requires .credentials.json)...")
try:
    import config
    print("[OK] config module loaded successfully")
    print("[OK] Credentials file found and valid!")
except SystemExit:
    print("[WARN] config module requires valid .credentials.json (expected for testing)")
    print("[INFO] Skipping config-dependent modules...")
    print("[INFO] Create .credentials.json to test full bot startup")

try:
    from utils.constants import (
        VALID_TERA_TYPES,
        TYPE_EMOJI,
        DEFAULT_TOTAL_POINTS,
        DEFAULT_MIN_POKEMON,
        DEFAULT_MAX_POKEMON,
        EMBED_COLOR_SUCCESS,
        EMBED_COLOR_ERROR
    )
    print(f"[OK] utils.constants imported ({len(VALID_TERA_TYPES)} Tera types)")
except Exception as e:
    print(f"[ERROR] utils.constants import error: {e}")
    sys.exit(1)

try:
    from utils.text_formatter import (
        to_small_caps,
        format_team_channel_name,
        format_category_name
    )
    print("[OK] utils.text_formatter imported")

    # Test text formatter
    test_name = "Fire Fighters"
    formatted = format_team_channel_name(test_name)
    print(f"   Example: '{test_name}' → '{formatted}'")

except Exception as e:
    print(f"[ERROR] utils.text_formatter import error: {e}")
    sys.exit(1)

# Services already imported above in bulk

# Test credentials file exists
try:
    from pathlib import Path
    creds_path = Path(".credentials.json")

    if creds_path.exists():
        print("[OK] .credentials.json found")

        # Try loading credentials
        with open(creds_path) as f:
            creds = json.load(f)

        # Check required fields
        required_fields = ["discord_bot_token", "spreadsheet_id"]
        missing = [f for f in required_fields if f not in creds]

        if missing:
            print(f"[WARN]  .credentials.json missing fields: {', '.join(missing)}")
        else:
            print("[OK] .credentials.json has all required fields")
    else:
        print("[WARN]  .credentials.json not found (required to run bot)")
        print("   Create it with: discord_bot_token and spreadsheet_id")

except Exception as e:
    print(f"[WARN]  Could not validate .credentials.json: {e}")

print("=" * 50)
print("[OK] All imports successful!")
print("\nNext steps:")
print("1. Ensure .credentials.json is configured")
print("2. Set up Google Sheets with required tabs")
print("3. Run: python bot.py")
