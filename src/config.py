"""
Central configuration management using pydantic-settings.
Cross-platform: uses pathlib for all file paths.
"""
import re
from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root — works on Windows, macOS, Linux
PROJECT_ROOT = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Deployment
    deploy_target: Literal["free", "azure"] = "free"

    # Discord
    discord_token: str
    discord_client_id: str
    discord_guild_id: str | None = None
    bot_name: str = "DraftBot"           # Display name shown in presence and embeds
    bot_status: str = "Pokemon Draft League"  # Activity text shown under bot name

    # Google Sheets
    google_sheets_credentials_file: Path = PROJECT_ROOT / "credentials.json"
    google_sheets_spreadsheet_id: str

    @field_validator("google_sheets_spreadsheet_id", mode="before")
    @classmethod
    def extract_spreadsheet_id(cls, v: str) -> str:
        """Accept either a bare ID or a full Google Sheets URL."""
        match = re.search(r"/spreadsheets/d/([a-zA-Z0-9_-]+)", v)
        return match.group(1) if match else v

    # Database
    database_url: str = f"sqlite+aiosqlite:///{PROJECT_ROOT / 'pokemon_draft.db'}"

    # PokéAPI
    pokeapi_base_url: str = "https://pokeapi.co/api/v2"
    pokeapi_rate_limit: int = 100

    # Showdown data URLs
    showdown_data_url: str = "https://raw.githubusercontent.com/smogon/pokemon-showdown/master/config/formats.ts"
    showdown_tiers_url: str = "https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/formats-data.ts"

    # Showdown bot account (used by /spar for live challenges)
    showdown_username: str = ""
    showdown_password: str = ""

    # ML policy models directory
    ml_policy_dir: str = "data/ml/policy"

    # Video Storage — Cloudflare R2 (free tier)
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_name: str = "pokemon-draft-videos"
    r2_public_url: str = ""

    # Video Storage — Azure Blob (Path B)
    azure_storage_connection_string: str = ""
    azure_storage_container: str = "match-videos"

    # Web API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_secret_key: str = "change-me-in-production"
    # Stored as comma-separated string; use .cors_origins_list for the parsed list
    cors_origins: str = "http://localhost:5173"

    # FFmpeg — cross-platform default uses PATH
    ffmpeg_path: str = "ffmpeg"

    # Smogon / VGC
    smogon_strategy_url: str = "https://www.smogon.com/dex"
    vgc_format: str = "reg-h"

    # ELO
    elo_k_factor: int = 32
    elo_default_rating: int = 1000

    # Logging
    log_level: str = "INFO"
    log_file: Path = PROJECT_ROOT / "logs" / "bot.log"

    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS origins as a list (split on comma)."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def data_dir(self) -> Path:
        """Cross-platform path to local data files."""
        return PROJECT_ROOT / "data"

    @property
    def video_storage_backend(self) -> str:
        """Which video backend to use based on deploy target."""
        return "azure" if self.deploy_target == "azure" else "r2"


# Singleton instance — import this everywhere
settings = Settings()
