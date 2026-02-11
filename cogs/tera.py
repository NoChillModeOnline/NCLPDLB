"""
Tera Captain management commands for Pokemon Draft League Bot.

Handles Tera Captain designation, type changes, and viewing.
"""

import discord
from discord.ext import commands
from typing import Optional

from services.sheets_service import SheetsService
from services.tera_service import TeraService
from utils.constants import (
    EMBED_COLOR_SUCCESS,
    EMBED_COLOR_ERROR,
    EMBED_COLOR_INFO,
    EMBED_COLOR_TERA,
    DEFAULT_MAX_TERA_CAPTAINS,
    DEFAULT_MAX_TERA_CAPTAIN_COST,
    DEFAULT_MAX_TERA_TOTAL_POINTS
)
from config import Config


class Tera(commands.Cog):
    """Tera Captain management commands"""

    def __init__(self, bot):
        self.bot = bot

        # Initialize services
        config = Config()
        self.sheets = SheetsService(
            credentials_path=config.credentials_path,
            spreadsheet_id=config.spreadsheet_id
        )
        self.tera_service = TeraService(self.sheets)

    # ==================== BASE COMMAND ====================

    @commands.command(name="tera")
    async def tera_base(self, ctx, player: Optional[str] = None):
        """
        Show Tera Captains for yourself or another player.

        Usage: !tera or !tera @player
        Alias for: !tera show
        """
        await self.show_tera_captains(ctx, player)

    # ==================== TERA CAPTAIN DESIGNATION ====================

    @commands.command(name="set")
    async def set_tera_captain(self, ctx, pokemon: str, tera_type: str):
        """
        Designate a Pokémon as a Tera Captain with chosen Tera Type.

        Usage: !tera set <pokemon> <type>
        Example: !tera set Pikachu Dragon
        """
        player_name = ctx.author.display_name

        try:
            result = self.tera_service.set_tera_captain(player_name, pokemon, tera_type)

            # Create success embed
            embed = discord.Embed(
                title="⚡ Tera Captain Designated!",
                description=f"**{pokemon}** is now a Tera Captain!",
                color=EMBED_COLOR_TERA
            )
            embed.add_field(
                name="Tera Type",
                value=f"{result['tera_type']} {self.tera_service.get_valid_types_display().split()[self.tera_service.sheets.get_pokemon_data(pokemon)['type1']]}",
                inline=True
            )
            embed.add_field(
                name="Point Cost",
                value=f"{result['point_cost']} pts",
                inline=True
            )
            embed.add_field(
                name="Progress",
                value=f"{result['total_captains']}/{DEFAULT_MAX_TERA_CAPTAINS} Tera Captains\n{result['total_points']}/{DEFAULT_MAX_TERA_TOTAL_POINTS} points used",
                inline=True
            )

            # Add tip if not complete
            if result['total_captains'] < DEFAULT_MAX_TERA_CAPTAINS:
                embed.add_field(
                    name="📝 Reminder",
                    value=f"You need exactly {DEFAULT_MAX_TERA_CAPTAINS} Tera Captains. Set {DEFAULT_MAX_TERA_CAPTAINS - result['total_captains']} more!",
                    inline=False
                )

            await ctx.send(embed=embed)

        except ValueError as e:
            await ctx.send(str(e))
        except Exception as e:
            await ctx.send(f"❌ Error setting Tera Captain: {e}")

    @commands.command(name="change")
    async def change_tera_type(self, ctx, pokemon: str, new_type: str):
        """
        Change a Tera Captain's Tera Type.

        Usage: !tera change <pokemon> <new_type>
        Example: !tera change Pikachu Steel
        """
        player_name = ctx.author.display_name

        try:
            result = self.tera_service.change_tera_type(player_name, pokemon, new_type)

            # Create success embed
            embed = discord.Embed(
                title="🔄 Tera Type Changed!",
                description=f"**{pokemon}**'s Tera type has been updated!",
                color=EMBED_COLOR_SUCCESS
            )
            embed.add_field(
                name="Old Tera Type",
                value=result['old_type'],
                inline=True
            )
            embed.add_field(
                name="➡️",
                value="",
                inline=True
            )
            embed.add_field(
                name="New Tera Type",
                value=result['new_type'],
                inline=True
            )

            await ctx.send(embed=embed)

        except ValueError as e:
            await ctx.send(str(e))
        except Exception as e:
            await ctx.send(f"❌ Error changing Tera type: {e}")

    @commands.command(name="remove")
    async def remove_tera_captain(self, ctx, pokemon: str):
        """
        Remove Tera Captain designation from a Pokémon.

        Usage: !tera remove <pokemon>
        Example: !tera remove Pikachu
        """
        player_name = ctx.author.display_name

        try:
            result = self.tera_service.remove_tera_captain(player_name, pokemon)

            # Create success embed
            embed = discord.Embed(
                title="↩️ Tera Captain Removed",
                description=f"**{pokemon}** is no longer a Tera Captain.",
                color=EMBED_COLOR_SUCCESS
            )
            embed.add_field(
                name="Previous Tera Type",
                value=result['tera_type'],
                inline=True
            )
            embed.add_field(
                name="Points Freed",
                value=f"{result['point_cost']} pts",
                inline=True
            )
            embed.add_field(
                name="Remaining",
                value=f"{result['remaining_captains']}/{DEFAULT_MAX_TERA_CAPTAINS} Tera Captains\n{result['remaining_points']}/{DEFAULT_MAX_TERA_TOTAL_POINTS} points",
                inline=True
            )

            await ctx.send(embed=embed)

        except ValueError as e:
            await ctx.send(str(e))
        except Exception as e:
            await ctx.send(f"❌ Error removing Tera Captain: {e}")

    # ==================== VIEWING TERA CAPTAINS ====================

    @commands.command(name="show")
    async def show_tera_captains(self, ctx, player: Optional[str] = None):
        """
        Display Tera Captains for a player.

        Usage: !tera show or !tera show @player
        Example: !tera show or !tera show Player1
        """
        target_player = player if player else ctx.author.display_name

        try:
            captains = self.tera_service.get_player_tera_captains(target_player)

            if not captains:
                if target_player == ctx.author.display_name:
                    await ctx.send(
                        f"ℹ️ You haven't set any Tera Captains yet!\n"
                        f"Use `!tera set <pokemon> <type>` to designate a Tera Captain.\n"
                        f"You need exactly {DEFAULT_MAX_TERA_CAPTAINS} Tera Captains."
                    )
                else:
                    await ctx.send(f"ℹ️ {target_player} hasn't set any Tera Captains yet.")
                return

            # Create display embed
            embed = discord.Embed(
                title=f"⚡ {target_player}'s Tera Captains ⚡",
                color=EMBED_COLOR_TERA
            )

            total_points = sum(c["point_cost"] for c in captains)

            for i, captain in enumerate(captains, 1):
                field_value = (
                    f"**Original:** {captain['original_types']}\n"
                    f"**Tera Type:** {captain['emoji']} {captain['tera_type']}\n"
                    f"**Cost:** {captain['point_cost']} pts"
                )
                embed.add_field(
                    name=f"{i}. {captain['pokemon']}",
                    value=field_value,
                    inline=False
                )

            # Add summary
            embed.add_field(
                name="📊 Summary",
                value=(
                    f"**Captains:** {len(captains)}/{DEFAULT_MAX_TERA_CAPTAINS}\n"
                    f"**Total Points:** {total_points}/{DEFAULT_MAX_TERA_TOTAL_POINTS}"
                ),
                inline=False
            )

            # Add reminder if incomplete
            if len(captains) < DEFAULT_MAX_TERA_CAPTAINS:
                embed.set_footer(text=f"⚠️ You need exactly {DEFAULT_MAX_TERA_CAPTAINS} Tera Captains! Set {DEFAULT_MAX_TERA_CAPTAINS - len(captains)} more.")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error viewing Tera Captains: {e}")

    @commands.command(name="list")
    async def list_all_tera_captains(self, ctx):
        """
        Show all Tera Captains in the league.

        Usage: !tera list
        """
        try:
            all_captains = self.tera_service.get_all_tera_captains()

            if not all_captains:
                await ctx.send("ℹ️ No Tera Captains have been set yet in the league.")
                return

            # Create display embed
            embed = discord.Embed(
                title="⚡ League Tera Captains ⚡",
                description=f"Tera Captains from {len(all_captains)} coach(es)",
                color=EMBED_COLOR_TERA
            )

            for player, captains in all_captains.items():
                captain_list = "\n".join([
                    f"{c['emoji']} **{c['pokemon']}** → {c['tera_type']} ({c['point_cost']} pts)"
                    for c in captains
                ])

                embed.add_field(
                    name=f"🏆 {player}",
                    value=captain_list,
                    inline=False
                )

            embed.set_footer(text="💡 Use !tera show @player to see detailed info")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error listing Tera Captains: {e}")

    # ==================== REFERENCE COMMANDS ====================

    @commands.command(name="types")
    async def show_valid_types(self, ctx):
        """
        Display all valid Tera types.

        Usage: !tera types
        """
        types_display = self.tera_service.get_valid_types_display()

        embed = discord.Embed(
            title="✨ Valid Tera Types ✨",
            description=types_display,
            color=EMBED_COLOR_INFO
        )
        embed.add_field(
            name="📝 Usage",
            value=f"Use `!tera set <pokemon> <type>` to designate a Tera Captain\nExample: `!tera set Pikachu Dragon`",
            inline=False
        )
        embed.add_field(
            name="⚠️ Requirements",
            value=(
                f"• Exactly {DEFAULT_MAX_TERA_CAPTAINS} Tera Captains per team\n"
                f"• Only Pokémon ≤{DEFAULT_MAX_TERA_CAPTAIN_COST} points can be Tera Captains\n"
                f"• Total Tera Captain points ≤{DEFAULT_MAX_TERA_TOTAL_POINTS}"
            ),
            inline=False
        )
        embed.set_footer(text="✨ Stellar is a special Tera type from Scarlet/Violet!")

        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def tera_help(self, ctx):
        """
        Show Tera Captain command help.

        Usage: !tera help
        """
        embed = discord.Embed(
            title="⚡ Tera Captain Commands",
            description="Manage your Tera Captains",
            color=EMBED_COLOR_INFO
        )

        embed.add_field(
            name="🎯 Designation",
            value=(
                "`!tera set <pokemon> <type>` - Designate a Tera Captain\n"
                "`!tera change <pokemon> <type>` - Change Tera type\n"
                "`!tera remove <pokemon>` - Remove Tera Captain"
            ),
            inline=False
        )

        embed.add_field(
            name="👀 Viewing",
            value=(
                "`!tera` or `!tera show` - View your Tera Captains\n"
                "`!tera show @player` - View another player's Tera Captains\n"
                "`!tera list` - View all league Tera Captains"
            ),
            inline=False
        )

        embed.add_field(
            name="📚 Reference",
            value="`!tera types` - Show all valid Tera types",
            inline=False
        )

        embed.add_field(
            name="📋 Requirements",
            value=(
                f"• **Exactly {DEFAULT_MAX_TERA_CAPTAINS}** Tera Captains per team\n"
                f"• Only Pokémon with **≤{DEFAULT_MAX_TERA_CAPTAIN_COST} points** can be Tera Captains\n"
                f"• Total Tera Captain points must be **≤{DEFAULT_MAX_TERA_TOTAL_POINTS}**\n"
                f"• **{len(self.tera_service.get_valid_types_display().split())} valid Tera types** (18 standard + Stellar ✨)"
            ),
            inline=False
        )

        await ctx.send(embed=embed)


# Setup function for loading the cog
async def setup(bot):
    await bot.add_cog(Tera(bot))
