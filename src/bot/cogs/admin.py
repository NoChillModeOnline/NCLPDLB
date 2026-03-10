"""
Admin Cog — Commissioner and admin override commands.
"""
import discord
from discord import app_commands
from discord.ext import commands

from src.services.draft_service import DraftService


def is_commissioner():
    """Check decorator: user must be league commissioner or have Manage Guild."""
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.guild_permissions.manage_guild:
            return True
        raise app_commands.CheckFailure("You must be a commissioner or have Manage Guild permission.")
    return app_commands.check(predicate)


class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.draft_service = DraftService()

    @app_commands.command(name="admin-skip", description="Force-skip a player's turn (commissioner only)")
    @app_commands.describe(user="Player to skip")
    @is_commissioner()
    async def admin_skip(self, interaction: discord.Interaction, user: discord.Member) -> None:
        await interaction.response.defer()
        result = await self.draft_service.force_skip(
            guild_id=str(interaction.guild_id),
            player_id=str(user.id),
        )
        await interaction.followup.send(f"Skipped {user.display_name}'s turn. Next: {result.next_player}")

    @app_commands.command(name="admin-pause", description="Pause the active draft")
    @is_commissioner()
    async def admin_pause(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.draft_service.pause_draft(str(interaction.guild_id))
        await interaction.followup.send("Draft paused.")

    @app_commands.command(name="admin-resume", description="Resume a paused draft")
    @is_commissioner()
    async def admin_resume(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.draft_service.resume_draft(str(interaction.guild_id))
        await interaction.followup.send("Draft resumed!")

    @app_commands.command(name="admin-override-pick", description="Override a pick (commissioner only)")
    @app_commands.describe(user="Player whose pick to change", old_pokemon="Pokemon to remove", new_pokemon="Pokemon to add")
    @is_commissioner()
    async def admin_override_pick(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        old_pokemon: str,
        new_pokemon: str,
    ) -> None:
        await interaction.response.defer()
        result = await self.draft_service.override_pick(
            guild_id=str(interaction.guild_id),
            player_id=str(user.id),
            old_pokemon=old_pokemon,
            new_pokemon=new_pokemon,
        )
        await interaction.followup.send(
            f"Override: removed **{old_pokemon}**, added **{new_pokemon}** for {user.display_name}."
        )

    @app_commands.command(name="admin-reset", description="Reset the current draft (CANNOT BE UNDONE)")
    @is_commissioner()
    async def admin_reset(self, interaction: discord.Interaction) -> None:
        # Confirm via button
        view = ConfirmResetView(guild_id=str(interaction.guild_id), draft_service=self.draft_service)
        await interaction.response.send_message(
            "⚠️ Are you sure you want to reset the draft? This cannot be undone.", view=view, ephemeral=True
        )


class ConfirmResetView(discord.ui.View):
    def __init__(self, guild_id: str, draft_service: DraftService) -> None:
        super().__init__(timeout=30)
        self.guild_id = guild_id
        self.draft_service = draft_service

    @discord.ui.button(label="Confirm Reset", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.draft_service.reset_draft(self.guild_id)
        await interaction.response.send_message("Draft has been reset.", ephemeral=True)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message("Reset cancelled.", ephemeral=True)
        self.stop()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))
