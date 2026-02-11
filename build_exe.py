"""
Build script to create standalone executable for Pokemon Draft League Bot
Run this with: python build_exe.py
"""

import PyInstaller.__main__
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'bot.py',                          # Main script
    '--onefile',                       # Create single executable
    '--name=PokemonDraftBot',          # Name of executable
    '--icon=NONE',                     # No icon (can add later)
    '--console',                       # Show console window
    '--add-data=cogs;cogs',            # Include cogs folder
    '--add-data=services;services',    # Include services folder
    '--add-data=utils;utils',          # Include utils folder
    '--hidden-import=discord',         # Ensure discord.py is included
    '--hidden-import=gspread',         # Ensure gspread is included
    '--hidden-import=google.auth',     # Ensure google auth is included
    '--hidden-import=google.oauth2',   # Ensure oauth2 is included
    '--collect-all=discord',           # Collect all discord files
    '--collect-all=gspread',           # Collect all gspread files
    f'--distpath={script_dir}/dist',   # Output directory
    f'--workpath={script_dir}/build',  # Build directory
    f'--specpath={script_dir}',        # Spec file location
])

print("\n" + "="*60)
print("  BUILD COMPLETE!")
print("="*60)
print(f"\nExecutable created at: {script_dir}\\dist\\PokemonDraftBot.exe")
print("\nTo run the bot:")
print("  1. Make sure .credentials.json is in the same folder as the .exe")
print("  2. Double-click PokemonDraftBot.exe")
print("\n" + "="*60)
