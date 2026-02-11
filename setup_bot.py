"""
Interactive Setup Script for Pokemon Draft League Bot

This script helps you set up the bot by:
1. Collecting Discord bot token
2. Collecting Google Sheets credentials
3. Creating .credentials.json file
4. Installing dependencies
5. Testing the connection

Run with: python setup_bot.py
"""

import json
import os
import sys
import subprocess
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

def print_header(text):
    """Print a formatted header"""
    print('\n' + '='*70)
    print(f'  {text}')
    print('='*70 + '\n')

def print_step(number, text):
    """Print a step number"""
    print(f'\n[STEP {number}] {text}')
    print('-' * 70)

def get_input(prompt, required=True, default=''):
    """Get user input with optional default"""
    if default:
        full_prompt = f'{prompt} [{default}]: '
    else:
        full_prompt = f'{prompt}: '

    while True:
        value = input(full_prompt).strip() or default

        if required and not value:
            print('[X] This field is required. Please enter a value.')
            continue

        return value

def get_yes_no(prompt, default=True):
    """Get yes/no input"""
    default_text = 'Y/n' if default else 'y/N'
    response = input(f'{prompt} [{default_text}]: ').strip().lower()

    if not response:
        return default

    return response in ['y', 'yes']

def test_imports():
    """Test if required packages are installed"""
    print('\nTesting required packages...')

    required_packages = [
        'discord',
        'gspread',
        'google.auth',
        'flask'
    ]

    missing = []

    for package in required_packages:
        try:
            __import__(package)
            print(f'  [OK] {package}')
        except ImportError:
            print(f'  [X] {package} (not installed)')
            missing.append(package)

    return len(missing) == 0, missing

def install_dependencies():
    """Install required dependencies"""
    print_step(1, 'Installing Dependencies')

    if get_yes_no('Install required Python packages?', default=True):
        print('\nInstalling packages from requirements.txt...')

        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ])
            print('[OK] Dependencies installed successfully!')
            return True
        except subprocess.CalledProcessError as e:
            print(f'[X] Error installing dependencies: {e}')
            return False
    else:
        print('[!]  Skipping dependency installation')
        return True

def setup_credentials():
    """Interactive credentials setup"""
    print_step(2, 'Setting Up Credentials')

    print('\nYou need:')
    print('  1. Discord Bot Token (from Discord Developer Portal)')
    print('  2. Google Spreadsheet ID (from your Google Sheet URL)')
    print('  3. Google Service Account JSON (from Google Cloud Console)')
    print()

    # Method selection
    print('Choose setup method:')
    print('  1. Simple setup (Discord token + Spreadsheet ID only)')
    print('  2. Full setup (Include Google Service Account JSON)')
    print()

    method = get_input('Enter choice (1 or 2)', default='1')

    if method == '1':
        return setup_simple_credentials()
    else:
        return setup_full_credentials()

def setup_simple_credentials():
    """Setup with just Discord token and Spreadsheet ID"""
    print('\n📝 Simple Setup')
    print('This creates a basic .credentials.json file.')
    print('You will need to manually add Google Service Account details later.')
    print()

    discord_token = get_input('Discord Bot Token')
    spreadsheet_id = get_input('Google Spreadsheet ID')

    credentials = {
        'discord_bot_token': discord_token,
        'spreadsheet_id': spreadsheet_id,
        'type': 'service_account',
        'project_id': 'your-project-id',
        'private_key_id': 'your-private-key-id',
        'private_key': '-----BEGIN PRIVATE KEY-----\\nYOUR_PRIVATE_KEY\\n-----END PRIVATE KEY-----\\n',
        'client_email': 'your-service-account@project.iam.gserviceaccount.com',
        'client_id': '123456789',
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
        'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/...'
    }

    return save_credentials(credentials)

def setup_full_credentials():
    """Setup with full Google Service Account JSON"""
    print('\n📝 Full Setup')
    print()

    discord_token = get_input('Discord Bot Token')
    spreadsheet_id = get_input('Google Spreadsheet ID')

    print('\nNow we need your Google Service Account JSON file.')
    print('You can either:')
    print('  1. Provide the path to your JSON file')
    print('  2. Paste the JSON content directly')
    print()

    if get_yes_no('Do you have a JSON file path?', default=True):
        json_path = get_input('Path to service account JSON file')

        try:
            with open(json_path, 'r') as f:
                service_account = json.load(f)

            credentials = {
                'discord_bot_token': discord_token,
                'spreadsheet_id': spreadsheet_id,
                **service_account
            }

            return save_credentials(credentials)

        except FileNotFoundError:
            print(f'[X] File not found: {json_path}')
            return False
        except json.JSONDecodeError:
            print('[X] Invalid JSON file')
            return False
    else:
        print('\nPaste your Google Service Account JSON content below.')
        print('(Paste and press Enter, then Ctrl+D on Unix or Ctrl+Z on Windows):')

        try:
            json_content = sys.stdin.read()
            service_account = json.loads(json_content)

            credentials = {
                'discord_bot_token': discord_token,
                'spreadsheet_id': spreadsheet_id,
                **service_account
            }

            return save_credentials(credentials)

        except json.JSONDecodeError:
            print('[X] Invalid JSON content')
            return False

def save_credentials(credentials):
    """Save credentials to .credentials.json"""
    output_path = '.credentials.json'

    if os.path.exists(output_path):
        if not get_yes_no(f'{output_path} already exists. Overwrite?', default=False):
            print('[!]  Keeping existing credentials file')
            return True

    try:
        with open(output_path, 'w') as f:
            json.dump(credentials, f, indent=2)

        print(f'\n[OK] Credentials saved to {output_path}')

        # Set file permissions (Unix only)
        if os.name != 'nt':
            os.chmod(output_path, 0o600)
            print('[OK] File permissions set to 600 (owner read/write only)')

        return True

    except Exception as e:
        print(f'[X] Error saving credentials: {e}')
        return False

def test_connection():
    """Test the bot connection"""
    print_step(3, 'Testing Connection')

    if not os.path.exists('.credentials.json'):
        print('[X] .credentials.json not found. Please complete setup first.')
        return False

    if get_yes_no('Test connection to Google Sheets?', default=True):
        print('\nAttempting to connect to Google Sheets...')

        try:
            from services.sheets_service import SheetsService

            with open('.credentials.json', 'r') as f:
                creds = json.load(f)

            sheets = SheetsService('.credentials.json', creds['spreadsheet_id'])
            print('[OK] Successfully connected to Google Sheets!')

            # Try to get a config value
            league_name = sheets.get_config_value('league_name', 'Unknown')
            print(f'[OK] League name: {league_name}')

            return True

        except Exception as e:
            print(f'[X] Connection test failed: {e}')
            print('\nThis is normal if you haven\'t set up your Google Sheet yet.')
            print('Make sure to:')
            print('  1. Create a Google Sheet')
            print('  2. Share it with your service account email')
            print('  3. Add the required sheets (Config, Pokemon, Teams, etc.)')
            return False

    return True

def main():
    """Main setup flow"""
    print_header('POKEMON DRAFT LEAGUE BOT - SETUP WIZARD')

    print('This wizard will help you set up your Pokemon Draft League Bot.')
    print()
    print('You will need:')
    print('  * Discord Bot Token')
    print('  * Google Spreadsheet ID')
    print('  * Google Service Account JSON (optional now, required later)')
    print()

    if not get_yes_no('Ready to begin?', default=True):
        print('\n[BYE] Setup cancelled. Run this script again when ready!')
        return

    # Step 1: Install dependencies
    if not install_dependencies():
        print('\n[X] Setup failed at dependency installation')
        return

    # Test imports
    success, missing = test_imports()
    if not success:
        print(f'\n[X] Missing packages: {", ".join(missing)}')
        print('Please run: pip install -r requirements.txt')
        return

    # Step 2: Setup credentials
    if not setup_credentials():
        print('\n[X] Setup failed at credentials configuration')
        return

    # Step 3: Test connection (optional)
    test_connection()

    # Final summary
    print_header('SETUP COMPLETE!')

    print('[OK] Your bot is configured and ready to run!')
    print()
    print('Next steps:')
    print('  1. Make sure your Google Sheet is set up')
    print('  2. Share the sheet with your service account email')
    print('  3. Run the bot:')
    print()
    print('     Option A: python bot.py')
    print('     Option B: Double-click run_bot.bat')
    print('     Option C: Double-click desktop shortcut (if created)')
    print()
    print('  4. Start the web dashboard:')
    print('     python web_server.py')
    print()
    print('For detailed instructions, see DEPLOYMENT_CHECKLIST.md')
    print()
    print('[SUCCESS] Have fun running your Pokemon Draft League!')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n[BYE] Setup cancelled by user')
        sys.exit(0)
    except Exception as e:
        print(f'\n[X] Unexpected error: {e}')
        sys.exit(1)
