"""
Azure Configuration Module
Handles Azure-specific configuration and services
"""

import os
import json
from typing import Optional, Dict

# Try to import Azure libraries (optional)
try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    print("Azure libraries not installed. Run: pip install azure-identity azure-keyvault-secrets")


class AzureConfig:
    """Azure configuration and Key Vault integration"""

    def __init__(self):
        self.key_vault_url = os.getenv('KEY_VAULT_URL')
        self.use_key_vault = os.getenv('USE_AZURE_KEY_VAULT', 'false').lower() == 'true'
        self._credential = None
        self._secret_client = None

    def _get_secret_client(self) -> Optional['SecretClient']:
        """Get Azure Key Vault secret client"""
        if not AZURE_AVAILABLE:
            print("Azure SDK not available")
            return None

        if not self.key_vault_url:
            print("KEY_VAULT_URL not set")
            return None

        if not self._secret_client:
            self._credential = DefaultAzureCredential()
            self._secret_client = SecretClient(
                vault_url=self.key_vault_url,
                credential=self._credential
            )

        return self._secret_client

    def get_secret(self, secret_name: str) -> Optional[str]:
        """
        Get secret from Azure Key Vault or environment variable

        Args:
            secret_name: Name of the secret

        Returns:
            Secret value or None
        """
        # Try environment variable first
        env_value = os.getenv(secret_name.upper().replace('-', '_'))
        if env_value:
            return env_value

        # Try Key Vault if enabled
        if self.use_key_vault:
            client = self._get_secret_client()
            if client:
                try:
                    secret = client.get_secret(secret_name)
                    return secret.value
                except Exception as e:
                    print(f"Failed to get secret from Key Vault: {e}")

        return None

    def get_database_config(self) -> Dict[str, str]:
        """
        Get Azure PostgreSQL database configuration

        Returns:
            Database configuration dictionary
        """
        return {
            'host': self.get_secret('postgres-host') or os.getenv('POSTGRES_HOST'),
            'database': self.get_secret('postgres-database') or os.getenv('POSTGRES_DB', 'pokemon_league'),
            'user': self.get_secret('postgres-user') or os.getenv('POSTGRES_USER'),
            'password': self.get_secret('postgres-password') or os.getenv('POSTGRES_PASSWORD'),
            'sslmode': 'require',
            'port': int(os.getenv('POSTGRES_PORT', '5432'))
        }

    def create_credentials_from_env(self) -> bool:
        """
        Create .credentials.json from environment variables
        Useful for Azure App Service deployment

        Returns:
            True if successful, False otherwise
        """
        discord_token = self.get_secret('discord-bot-token') or os.getenv('DISCORD_BOT_TOKEN')
        spreadsheet_id = self.get_secret('spreadsheet-id') or os.getenv('SPREADSHEET_ID')

        if not discord_token or not spreadsheet_id:
            print("Missing required environment variables!")
            return False

        credentials = {
            'discord_bot_token': discord_token,
            'spreadsheet_id': spreadsheet_id
        }

        try:
            with open('.credentials.json', 'w') as f:
                json.dump(credentials, f, indent=2)
            print("✅ Created .credentials.json from environment variables")
            return True
        except Exception as e:
            print(f"❌ Failed to create credentials file: {e}")
            return False

    def create_service_account_from_env(self) -> bool:
        """
        Create service-account.json from environment variable
        Useful for Azure App Service deployment

        Returns:
            True if successful, False otherwise
        """
        service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT')

        if not service_account_json:
            print("GOOGLE_SERVICE_ACCOUNT environment variable not set")
            return False

        try:
            # Validate JSON
            service_account_data = json.loads(service_account_json)

            with open('service-account.json', 'w') as f:
                json.dump(service_account_data, f, indent=2)

            print("✅ Created service-account.json from environment variable")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in GOOGLE_SERVICE_ACCOUNT: {e}")
            return False
        except Exception as e:
            print(f"❌ Failed to create service account file: {e}")
            return False

    def setup_azure_credentials(self) -> bool:
        """
        Setup all credentials from Azure environment

        Returns:
            True if successful, False otherwise
        """
        print("Setting up credentials from Azure environment...")

        success = True

        # Create credentials.json
        if not self.create_credentials_from_env():
            print("⚠️  Failed to create .credentials.json")
            success = False

        # Create service-account.json
        if not self.create_service_account_from_env():
            print("⚠️  Failed to create service-account.json")
            success = False

        return success


def check_azure_environment() -> Dict[str, bool]:
    """
    Check Azure environment configuration

    Returns:
        Dictionary with status of various checks
    """
    checks = {
        'azure_sdk_installed': AZURE_AVAILABLE,
        'key_vault_url_set': bool(os.getenv('KEY_VAULT_URL')),
        'discord_token_set': bool(os.getenv('DISCORD_BOT_TOKEN')),
        'spreadsheet_id_set': bool(os.getenv('SPREADSHEET_ID')),
        'google_service_account_set': bool(os.getenv('GOOGLE_SERVICE_ACCOUNT')),
        'postgres_configured': bool(os.getenv('POSTGRES_HOST')),
    }

    return checks


def print_azure_status():
    """Print Azure configuration status"""
    print("\n" + "="*60)
    print("  AZURE CONFIGURATION STATUS")
    print("="*60)

    checks = check_azure_environment()

    for check, status in checks.items():
        status_str = "✅" if status else "❌"
        print(f"{status_str} {check.replace('_', ' ').title()}")

    print("="*60 + "\n")


if __name__ == '__main__':
    # Run configuration check
    print_azure_status()

    # Setup credentials if running on Azure
    if os.getenv('WEBSITE_INSTANCE_ID'):  # Azure App Service environment
        print("Detected Azure App Service environment")
        azure_config = AzureConfig()
        azure_config.setup_azure_credentials()
