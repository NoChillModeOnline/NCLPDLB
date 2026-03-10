"""
Pokemon Draft League Bot — Main entrypoint.
Discord.py 2.x with slash commands, views, and cogs.
Cross-platform compatible (Windows, macOS, Linux).
"""
import asyncio
import logging
import sys
from pathlib import Path

import discord
from discord.ext import commands

# Ensure src/ is on path (cross-platform)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config import settings

# ── Logging Setup ─────────────────────────────────────────────
log_dir = settings.log_file.parent
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(settings.log_file, encoding="utf-8"),
    ],
)
log = logging.getLogger("pokemon_draft_bot")

# ── Bot Setup ─────────────────────────────────────────────────
COGS = [
    "src.bot.cogs.draft",
    "src.bot.cogs.team",
    "src.bot.cogs.league",
    "src.bot.cogs.admin",
    "src.bot.cogs.stats",
    "src.bot.cogs.sheet",    # Google Sheets management commands
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class DraftLeagueBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="!",  # Fallback prefix; primary interface is slash commands
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        """Called once before the bot starts. Load cogs and sync slash commands."""
        for cog in COGS:
            try:
                await self.load_extension(cog)
                log.info(f"Loaded cog: {cog}")
            except Exception as e:
                log.error(f"Failed to load cog {cog}: {e}", exc_info=True)

        # Sync slash commands to test guild first (instant), then globally
        if settings.discord_guild_id:
            guild = discord.Object(id=int(settings.discord_guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            log.info(f"Slash commands synced to test guild {settings.discord_guild_id}")
        else:
            await self.tree.sync()
            log.info("Slash commands synced globally")

    async def on_ready(self) -> None:
        log.info(f"Bot ready! Logged in as {self.user} (ID: {self.user.id})")
        log.info(f"Bot name: {settings.bot_name}")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=settings.bot_status,
            )
        )

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        log.error(f"Command error: {error}", exc_info=True)


async def main() -> None:
    bot = DraftLeagueBot()
    async with bot:
        await bot.start(settings.discord_token)


if __name__ == "__main__":
    asyncio.run(main())
