"""
Pokemon Draft League Discord Bot

Main entry point for the bot. Handles initialization, cog loading,
and event handlers.

Optimizations:
- Async cog loading for faster startup
- Connection pooling for Google Sheets
- Efficient error handling
- Status updates for monitoring
"""

import discord
from discord.ext import commands
import sys
import traceback
import asyncio
from typing import List

# Import configuration
from config import (
    DISCORD_TOKEN,
    COMMAND_PREFIX,
    BOT_DESCRIPTION
)


class PokemonDraftBot(commands.Bot):
    """Custom bot class for Pokemon Draft League"""

    def __init__(self):
        # Set up intents (required for message content and member info)
        intents = discord.Intents.default()
        intents.message_content = True  # Required for reading commands
        intents.members = True          # Required for member lookups
        intents.guilds = True           # Required for server management

        # Initialize bot with command prefix and intents
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            description=BOT_DESCRIPTION,
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )

    async def setup_hook(self):
        """
        Called when bot is starting up.
        Load all cogs (command modules) here.

        Optimizations:
        - Parallel cog loading for faster startup
        - Better error handling per cog
        """
        # List of cog modules to load
        cogs: List[str] = [
            'cogs.league',   # League initialization
            'cogs.draft',    # Draft management
            'cogs.tera',     # Tera Captain management
            'cogs.team',     # Team management and analysis
            # 'cogs.battle', # Battle tracking (uncomment when implemented)
            # 'cogs.stats',  # Statistics (uncomment when implemented)
        ]

        print(f'\n🔌 Loading {len(cogs)} cog(s)...')

        # Load cogs concurrently for faster startup
        async def load_cog(cog_name: str) -> tuple[str, bool, str]:
            """Load a single cog and return result"""
            try:
                await self.load_extension(cog_name)
                return (cog_name, True, '')
            except Exception as e:
                error_msg = f'{type(e).__name__}: {e}'
                traceback.print_exc()
                return (cog_name, False, error_msg)

        # Load all cogs in parallel
        results = await asyncio.gather(*[load_cog(cog) for cog in cogs])

        # Report results
        success_count = sum(1 for _, success, _ in results if success)
        for cog_name, success, error in results:
            if success:
                print(f'  ✅ {cog_name}')
            else:
                print(f'  ❌ {cog_name}: {error}')

        print(f'✅ Loaded {success_count}/{len(cogs)} cog(s)\n')

    async def on_ready(self):
        """Called when bot successfully connects to Discord"""
        # Calculate total members across all guilds
        total_members = sum(guild.member_count or 0 for guild in self.guilds)

        print('\n' + '='*60)
        print(f'🤖 Bot: {self.user.name} (ID: {self.user.id})')
        print(f'📊 Servers: {len(self.guilds)}')
        print(f'👥 Members: {total_members:,}')
        print(f'⚡ Prefix: {COMMAND_PREFIX}')
        print(f'🐍 Python: {sys.version.split()[0]}')
        print(f'📦 Discord.py: {discord.__version__}')
        print('='*60)
        print('✅ Pokemon Draft League Bot is ready!')
        print(f'   Use {COMMAND_PREFIX}help to see available commands\n')

        # Set bot status with activity
        await self.change_presence(
            activity=discord.Game(name=f'{COMMAND_PREFIX}help | Draft Leagues'),
            status=discord.Status.online
        )

    async def on_command_error(self, ctx, error):
        """Global error handler for commands"""

        # Ignore command not found errors (reduce spam)
        if isinstance(error, commands.CommandNotFound):
            return

        # Permission errors
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"❌ You don't have permission to use this command!\n"
                f"Required: {', '.join(error.missing_permissions)}"
            )
            return

        # Missing required argument
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"❌ Missing required argument: `{error.param.name}`\n"
                f"Use `{COMMAND_PREFIX}help {ctx.command}` for usage info."
            )
            return

        # Bad argument type
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                f"❌ Invalid argument provided!\n"
                f"Use `{COMMAND_PREFIX}help {ctx.command}` for usage info."
            )
            return

        # Command is on cooldown
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"⏳ This command is on cooldown. "
                f"Try again in {error.retry_after:.1f} seconds."
            )
            return

        # Bot missing permissions
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                f"❌ I don't have the required permissions!\n"
                f"I need: {', '.join(error.missing_permissions)}"
            )
            return

        # Unknown error - log it
        print(f"\n❌ Error in command '{ctx.command}':")
        print(f"   User: {ctx.author} ({ctx.author.id})")
        print(f"   Guild: {ctx.guild.name if ctx.guild else 'DM'}")
        print(f"   Channel: {ctx.channel}")
        print(f"   Message: {ctx.message.content}")
        print(f"   Error: {type(error).__name__}: {error}")
        traceback.print_exception(type(error), error, error.__traceback__)

        # Send generic error message to user
        await ctx.send(
            f"❌ An unexpected error occurred!\n"
            f"```\n{type(error).__name__}: {error}\n```\n"
            f"Please report this to an admin."
        )

    async def on_message(self, message):
        """Called for every message the bot can see"""
        # Ignore messages from bots (including self)
        if message.author.bot:
            return

        # Process commands
        await self.process_commands(message)


def main():
    """Main function to run the bot"""
    print("🚀 Starting Pokemon Draft League Bot...")
    print(f"   Python version: {sys.version}")
    print(f"   Discord.py version: {discord.__version__}")

    # Create and run bot
    bot = PokemonDraftBot()

    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("\n❌ Error: Invalid Discord bot token!")
        print("   Please check your .credentials.json file.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Bot shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {type(e).__name__}: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
