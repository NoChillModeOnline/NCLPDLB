"""
Admin Cog — Commissioner and admin override commands.
"""
import asyncio
import logging
import subprocess
import sys
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from src.services.draft_service import DraftService

log = logging.getLogger(__name__)


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
        await self.draft_service.override_pick(
            guild_id=str(interaction.guild_id),
            player_id=str(user.id),
            old_pokemon=old_pokemon,
            new_pokemon=new_pokemon,
        )
        await interaction.followup.send(
            f"Override: removed **{old_pokemon}**, added **{new_pokemon}** for {user.display_name}."
        )

    # ── /admin-sync ────────────────────────────────────────────
    @app_commands.command(name="admin-sync", description="Sync slash commands with Discord (push new/updated commands)")
    @app_commands.describe(scope="guild = instant (test guild only), global = up to 1 hour to propagate everywhere")
    @app_commands.choices(scope=[
        app_commands.Choice(name="guild (instant)", value="guild"),
        app_commands.Choice(name="global (up to 1 hour)", value="global"),
    ])
    @is_commissioner()
    async def admin_sync(
        self,
        interaction: discord.Interaction,
        scope: app_commands.Choice[str] = None,
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        use_guild = (scope is None) or (scope.value == "guild")

        if use_guild and interaction.guild:
            synced = await interaction.client.tree.sync(guild=interaction.guild)
            await interaction.followup.send(
                f"✅ Synced **{len(synced)} command(s)** to this server (instant).",
                ephemeral=True,
            )
        else:
            synced = await interaction.client.tree.sync()
            await interaction.followup.send(
                f"✅ Synced **{len(synced)} command(s)** globally. May take up to 1 hour to appear.",
                ephemeral=True,
            )

    # ── /admin-reset ───────────────────────────────────────────
    @app_commands.command(name="admin-reset", description="Reset the current draft (CANNOT BE UNDONE)")
    @is_commissioner()
    async def admin_reset(self, interaction: discord.Interaction) -> None:
        # Confirm via button
        view = ConfirmResetView(guild_id=str(interaction.guild_id), draft_service=self.draft_service)
        await interaction.response.send_message(
            "⚠️ Are you sure you want to reset the draft? This cannot be undone.", view=view, ephemeral=True
        )

    # ── /admin-train ───────────────────────────────────────────
    @app_commands.command(
        name="admin-train",
        description="Train the AI bot for a battle format (requires local Showdown server)",
    )
    @app_commands.describe(
        format="Format to train (e.g. gen9randombattle)",
        timesteps="Training steps — higher = stronger but slower (default: 500000)",
        force="Re-train even if a model already exists",
    )
    @is_commissioner()
    async def admin_train(
        self,
        interaction: discord.Interaction,
        format: str,
        timesteps: int = 500_000,
        force: bool = False,
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)

        from src.ml.train_all import TRAINING_MAP
        if format not in TRAINING_MAP:
            await interaction.followup.send(
                f"Unknown format `{format}`. Check `/spar` autocomplete for valid formats.",
                ephemeral=True,
            )
            return

        model_path = Path("data/ml/policy") / format / "final_model.zip"
        if model_path.exists() and not force:
            await interaction.followup.send(
                f"Model for `{format}` already exists. Use `force: True` to retrain.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="Training Started",
            description=(
                f"Training AI for **{format}**\n"
                f"Steps: `{timesteps:,}` | Force: `{force}`\n\n"
                "This runs in the background and may take **30–120 minutes**.\n"
                "You'll get a DM when it finishes."
            ),
            color=discord.Color.blurple(),
        )
        embed.set_footer(text="Requires local Showdown server on ws://localhost:8000")
        await interaction.followup.send(embed=embed, ephemeral=True)

        asyncio.create_task(
            _run_training(interaction, format, timesteps, force)
        )

    @admin_train.autocomplete("format")
    async def admin_train_format_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        from src.ml.train_all import TRAINING_MAP
        needle = current.lower()
        return [
            app_commands.Choice(name=fmt, value=fmt)
            for fmt in TRAINING_MAP
            if needle in fmt.lower()
        ][:25]

    # ── /admin-train-all ───────────────────────────────────────
    @app_commands.command(
        name="admin-train-all",
        description="Train AI models for all formats sequentially (requires local Showdown server)",
    )
    @app_commands.describe(
        timesteps="Training steps per format (default: 500000)",
        skip_existing="Skip formats that already have a final_model.zip (default: True)",
    )
    @is_commissioner()
    async def admin_train_all(
        self,
        interaction: discord.Interaction,
        timesteps: int = 500_000,
        skip_existing: bool = True,
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)

        from src.ml.train_all import TRAINING_MAP
        from src.ml.showdown_player import best_model_for_format

        save_dir = Path("data/ml/policy")
        total = len([f for f, e in TRAINING_MAP.items() if e[0] is not None])
        already_done = sum(
            1 for fmt in TRAINING_MAP
            if skip_existing and best_model_for_format(fmt, str(save_dir)) is not None
        )
        to_train = total - already_done

        embed = discord.Embed(
            title="Training All Formats",
            description=(
                f"**{to_train}** format(s) queued — **{already_done}** already trained (skipped).\n"
                f"Steps per format: `{timesteps:,}` | Skip existing: `{skip_existing}`\n\n"
                "Trains one format at a time. Each takes **30–120 minutes**.\n"
                "You'll get a DM with the final summary when all are done."
            ),
            color=discord.Color.blurple(),
        )
        embed.set_footer(text="Requires local Showdown server on ws://localhost:8000")
        await interaction.followup.send(embed=embed, ephemeral=True)

        asyncio.create_task(
            _run_training_all(interaction, timesteps, force=not skip_existing)
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


async def _run_training(
    interaction: discord.Interaction,
    fmt: str,
    timesteps: int,
    force: bool,
) -> None:
    """Background task: run train_all for a single format and DM the result."""
    project_root = Path(__file__).parents[3]
    cmd = [
        sys.executable, "-m", "src.ml.train_all",
        "--formats", fmt,
        "--timesteps", str(timesteps),
    ]
    if force:
        cmd.append("--force")

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(project_root),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        stdout, _ = await proc.communicate()
        ok = proc.returncode == 0
        output = (stdout or b"").decode(errors="replace")[-1500:]  # last 1500 chars

        embed = discord.Embed(
            title="Training Complete" if ok else "Training Failed",
            description=f"Format: `{fmt}`\n```\n{output}\n```",
            color=discord.Color.green() if ok else discord.Color.red(),
        )
        await interaction.user.send(embed=embed)
    except Exception as exc:
        log.error(f"[admin-train] {fmt} failed: {exc}", exc_info=True)
        try:
            await interaction.user.send(f"Training `{fmt}` encountered an error: `{exc}`")
        except Exception:
            pass


async def _run_training_all(
    interaction: discord.Interaction,
    timesteps: int,
    force: bool,
) -> None:
    """Background task: run train_all for every format and DM a summary."""
    project_root = Path(__file__).parents[3]
    cmd = [
        sys.executable, "-m", "src.ml.train_all",
        "--timesteps", str(timesteps),
    ]
    if force:
        cmd.append("--force")

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(project_root),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        stdout, _ = await proc.communicate()
        ok = proc.returncode == 0
        output = (stdout or b"").decode(errors="replace")[-1800:]

        embed = discord.Embed(
            title="Train-All Complete" if ok else "Train-All Finished With Errors",
            description=f"```\n{output}\n```",
            color=discord.Color.green() if ok else discord.Color.orange(),
        )
        await interaction.user.send(embed=embed)
    except Exception as exc:
        log.error(f"[admin-train-all] failed: {exc}", exc_info=True)
        try:
            await interaction.user.send(f"Train-all encountered an error: `{exc}`")
        except Exception:
            pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))
