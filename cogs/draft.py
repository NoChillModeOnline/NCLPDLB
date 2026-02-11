"""
Draft management commands for Pokemon Draft League Bot.

Handles draft initialization, pick making, budget tracking,
and draft completion.
"""

import discord
from discord.ext import commands
import asyncio
from typing import Optional

from services.draft_service import DraftService
from utils.constants import (
    EMBED_COLOR_SUCCESS,
    EMBED_COLOR_ERROR,
    EMBED_COLOR_WARNING,
    EMBED_COLOR_INFO,
    DEFAULT_TOTAL_POINTS,
    DEFAULT_MIN_POKEMON,
    DEFAULT_MAX_POKEMON,
    PICK_TIMEOUT_SECONDS
)


class Draft(commands.Cog):
    """Draft management commands"""

    def __init__(self, bot):
        self.bot = bot

        # Use shared SheetsService instance from bot (optimization)
        self.sheets = bot.sheets
        self.draft_service = DraftService(self.sheets)

    # ==================== DRAFT INITIALIZATION ====================

    @commands.command(name="draft")
    async def draft_base(self, ctx):
        """Base command - shows draft help"""
        embed = discord.Embed(
            title="📋 Draft Commands",
            description="Manage your Pokémon draft",
            color=EMBED_COLOR_INFO
        )

        embed.add_field(
            name="🎲 Draft Management",
            value=(
                "`!draft start` - Start a new draft (admin)\n"
                "`!draft status` - View current draft status\n"
                "`!draft end` - End the draft manually (admin)"
            ),
            inline=False
        )

        embed.add_field(
            name="🎯 Making Picks",
            value=(
                "`!draft pick <pokemon>` - Make your draft pick\n"
                "`!draft budget [player]` - Check points remaining\n"
                "`!draft available [max_cost]` - View available Pokémon"
            ),
            inline=False
        )

        embed.add_field(
            name="🔧 Admin Tools",
            value=(
                "`!draft undo` - Undo last pick (admin)"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="start")
    @commands.has_permissions(administrator=True)
    async def start_draft(self, ctx):
        """
        Start a new draft with interactive setup (admin only).

        Asks questions to configure the draft before starting.
        """
        # Check if draft is already active
        status = self.draft_service.get_draft_status()
        if status["is_active"]:
            await ctx.send("❌ A draft is already in progress! Use `!draft end` to finish it first.")
            return

        await ctx.send("🎮 **Starting Draft Setup...**")

        # ==================== QUESTION 1: Draft Type ====================

        draft_type_embed = discord.Embed(
            title="❓ Question 1: Draft Type",
            description="Which draft format would you like to use?",
            color=EMBED_COLOR_INFO
        )
        draft_type_embed.add_field(
            name="🐍 Snake Draft (Recommended)",
            value=(
                "Draft order reverses each round.\n"
                "Example: Round 1 (1→8), Round 2 (8→1), Round 3 (1→8)\n"
                "**Fair for all positions**"
            ),
            inline=False
        )
        draft_type_embed.add_field(
            name="➡️ Linear Draft",
            value=(
                "Draft order stays the same each round.\n"
                "Example: Round 1 (1→8), Round 2 (1→8), Round 3 (1→8)\n"
                "**Gives advantage to early picks**"
            ),
            inline=False
        )
        draft_type_embed.set_footer(text="Reply with: snake or linear")

        await ctx.send(embed=draft_type_embed)

        def check_author(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check_author, timeout=60.0)
            draft_type = msg.content.lower().strip()

            if draft_type not in ["snake", "linear"]:
                await ctx.send("❌ Invalid draft type. Defaulting to **snake**.")
                draft_type = "snake"
            else:
                await ctx.send(f"✅ Draft type set to: **{draft_type.title()}**")

        except asyncio.TimeoutError:
            await ctx.send("❌ Timed out. Cancelling draft setup.")
            return

        # ==================== QUESTION 2: Player Selection ====================

        player_select_embed = discord.Embed(
            title="❓ Question 2: Who's Drafting?",
            description="Select which coaches will participate in this draft.",
            color=EMBED_COLOR_INFO
        )
        player_select_embed.add_field(
            name="Option 1: All Coaches",
            value="Include all users with the 'Coach' role",
            inline=False
        )
        player_select_embed.add_field(
            name="Option 2: Custom List",
            value="Specify players manually (mention them)",
            inline=False
        )
        player_select_embed.set_footer(text="Reply with: all or mention players (@user1 @user2 ...)")

        await ctx.send(embed=player_select_embed)

        try:
            msg = await self.bot.wait_for('message', check=check_author, timeout=60.0)
            selection = msg.content.lower().strip()

            if selection == "all":
                # Get all members with Coach role
                coach_role = discord.utils.get(ctx.guild.roles, name="Coach")
                if not coach_role:
                    await ctx.send("❌ No 'Coach' role found! Create it with `!league init` first.")
                    return

                players = [member.display_name for member in coach_role.members]

                if not players:
                    await ctx.send("❌ No coaches found! Players must register with `!league register` first.")
                    return

                await ctx.send(f"✅ Found {len(players)} coaches: {', '.join(players)}")

            else:
                # Get mentioned users
                if not msg.mentions:
                    await ctx.send("❌ No players mentioned! Cancelling draft setup.")
                    return

                players = [member.display_name for member in msg.mentions]
                await ctx.send(f"✅ Draft players: {', '.join(players)}")

        except asyncio.TimeoutError:
            await ctx.send("❌ Timed out. Cancelling draft setup.")
            return

        # ==================== QUESTION 3: Confirm Settings ====================

        confirm_embed = discord.Embed(
            title="✅ Confirm Draft Settings",
            description="Please review the draft configuration:",
            color=EMBED_COLOR_SUCCESS
        )
        confirm_embed.add_field(name="Draft Type", value=draft_type.title(), inline=True)
        confirm_embed.add_field(name="Players", value=len(players), inline=True)
        confirm_embed.add_field(name="Point Budget", value=f"{DEFAULT_TOTAL_POINTS} per player", inline=True)
        confirm_embed.add_field(name="Team Size", value=f"{DEFAULT_MIN_POKEMON}-{DEFAULT_MAX_POKEMON} Pokémon", inline=True)
        confirm_embed.add_field(name="Pick Timer", value=f"{PICK_TIMEOUT_SECONDS//60} minutes", inline=True)
        confirm_embed.add_field(
            name="Players",
            value=", ".join(players),
            inline=False
        )
        confirm_embed.set_footer(text="Reply with: confirm or cancel")

        await ctx.send(embed=confirm_embed)

        try:
            msg = await self.bot.wait_for('message', check=check_author, timeout=30.0)
            confirmation = msg.content.lower().strip()

            if confirmation != "confirm":
                await ctx.send("❌ Draft setup cancelled.")
                return

        except asyncio.TimeoutError:
            await ctx.send("❌ Timed out. Draft setup cancelled.")
            return

        # ==================== START THE DRAFT ====================

        try:
            draft_state = self.draft_service.start_draft(players, draft_type)

            # Create announcement embed
            announce_embed = discord.Embed(
                title="🎮 DRAFT HAS STARTED! 🎮",
                description=f"**{len(players)} coaches** are ready to draft!",
                color=EMBED_COLOR_SUCCESS
            )
            announce_embed.add_field(
                name="📋 Draft Settings",
                value=(
                    f"**Type:** {draft_type.title()} Draft\n"
                    f"**Budget:** {DEFAULT_TOTAL_POINTS} points per coach\n"
                    f"**Team Size:** {DEFAULT_MIN_POKEMON}-{DEFAULT_MAX_POKEMON} Pokémon\n"
                    f"**Pick Timer:** {PICK_TIMEOUT_SECONDS//60} minutes per pick"
                ),
                inline=False
            )
            announce_embed.add_field(
                name="📝 Draft Order",
                value="\n".join([f"{i+1}. {player}" for i, player in enumerate(draft_state["players"])]),
                inline=False
            )
            announce_embed.add_field(
                name="⚡ Current Pick",
                value=f"**{draft_state['players'][0]}** is on the clock!",
                inline=False
            )
            announce_embed.add_field(
                name="🎯 How to Pick",
                value=f"Use `!draft pick <pokemon_name>` to make your selection",
                inline=False
            )

            await ctx.send(embed=announce_embed)

            # Mention the first player
            first_player_member = discord.utils.find(
                lambda m: m.display_name == draft_state["players"][0],
                ctx.guild.members
            )
            if first_player_member:
                await ctx.send(f"{first_player_member.mention} You're up! Use `!draft pick <pokemon>` to make your selection.")

        except Exception as e:
            await ctx.send(f"❌ Error starting draft: {e}")

    # ==================== MAKING PICKS ====================

    @commands.command(name="pick")
    async def make_pick(self, ctx, *, pokemon: str):
        """
        Make a draft pick.

        Usage: !draft pick <pokemon_name>
        Example: !draft pick Pikachu
        """
        player_name = ctx.author.display_name

        try:
            # Make the pick
            result = self.draft_service.make_pick(player_name, pokemon)

            # Create success embed
            embed = discord.Embed(
                title="✅ Pick Confirmed!",
                description=f"**{player_name}** drafted **{pokemon}**!",
                color=EMBED_COLOR_SUCCESS
            )
            embed.add_field(
                name="Pick Details",
                value=(
                    f"**Cost:** {result['pick_data']['cost']} points\n"
                    f"**Round:** {result['pick_data']['round']}\n"
                    f"**Pick #:** {result['pick_data']['pick_number']}"
                ),
                inline=True
            )
            embed.add_field(
                name="Your Budget",
                value=(
                    f"**Remaining:** {result['remaining_budget']}/{DEFAULT_TOTAL_POINTS} points\n"
                    f"**Pokémon:** {result['pokemon_count']}/{DEFAULT_MAX_POKEMON}"
                ),
                inline=True
            )

            await ctx.send(embed=embed)

            # Announce next player if draft is still active
            if result["next_player"]:
                next_player_member = discord.utils.find(
                    lambda m: m.display_name == result["next_player"],
                    ctx.guild.members
                )
                if next_player_member:
                    await ctx.send(
                        f"⏰ {next_player_member.mention} You're up! "
                        f"Use `!draft pick <pokemon>` to make your selection. "
                        f"({PICK_TIMEOUT_SECONDS//60} minute timer)"
                    )
            else:
                # Draft is complete
                await ctx.send("🎉 **DRAFT COMPLETE!** All coaches have finished drafting their teams!")
                await ctx.send("📊 Use `!team <player>` to view rosters.")
                await ctx.send("⚡ Use `!tera set <pokemon> <type>` to designate Tera Captains.")
                await ctx.send("🏁 Admin: Use `!league start` to create coach channels and begin the season!")

        except ValueError as e:
            await ctx.send(f"❌ {str(e)}")
        except Exception as e:
            await ctx.send(f"❌ Error making pick: {e}")

    # ==================== DRAFT STATUS ====================

    @commands.command(name="status")
    async def draft_status(self, ctx):
        """View current draft status."""
        status = self.draft_service.get_draft_status()

        if not status["is_active"]:
            await ctx.send("ℹ️ No draft is currently in progress. Use `!draft start` to begin!")
            return

        # Create status embed
        embed = discord.Embed(
            title="📊 Draft Status",
            color=EMBED_COLOR_INFO
        )
        embed.add_field(
            name="Current Pick",
            value=(
                f"**Round:** {status['current_round']}\n"
                f"**Pick:** {status['current_pick']}\n"
                f"**Total Picks:** {status['total_picks']}"
            ),
            inline=True
        )
        embed.add_field(
            name="On the Clock",
            value=f"**{status['current_player']}**" + (" ⏰ TIMEOUT!" if status['pick_timeout'] else ""),
            inline=True
        )
        embed.add_field(
            name="Draft Type",
            value=status['draft_type'].title(),
            inline=True
        )

        # Show draft order
        player_status = []
        for i, player in enumerate(status['players'], 1):
            budget_info = self.draft_service.get_player_budget(player)
            marker = "👉 " if player == status['current_player'] else "   "
            player_status.append(
                f"{marker}{i}. **{player}** - "
                f"{budget_info['pokemon_count']} Pokémon, "
                f"{budget_info['points_remaining']} pts left"
            )

        embed.add_field(
            name="Draft Order",
            value="\n".join(player_status),
            inline=False
        )

        await ctx.send(embed=embed)

    # ==================== BUDGET TRACKING ====================

    @commands.command(name="budget")
    async def check_budget(self, ctx, player: Optional[str] = None):
        """
        Check draft budget and remaining points.

        Usage: !draft budget [player_name]
        Example: !draft budget or !draft budget Player1
        """
        target_player = player if player else ctx.author.display_name

        try:
            budget_info = self.draft_service.get_player_budget(target_player)

            # Create budget embed
            embed = discord.Embed(
                title=f"💰 {budget_info['player']}'s Draft Budget",
                color=EMBED_COLOR_INFO
            )
            embed.add_field(
                name="Point Summary",
                value=(
                    f"**Total:** {budget_info['total_points']} points\n"
                    f"**Used:** {budget_info['points_used']} points\n"
                    f"**Remaining:** {budget_info['points_remaining']} points"
                ),
                inline=True
            )
            embed.add_field(
                name="Team Progress",
                value=(
                    f"**Pokémon Drafted:** {budget_info['pokemon_count']}\n"
                    f"**Minimum Required:** {budget_info['min_pokemon']}\n"
                    f"**Maximum Allowed:** {budget_info['max_pokemon']}"
                ),
                inline=True
            )

            # Show drafted Pokemon
            if budget_info['drafted_pokemon']:
                pokemon_list = "\n".join([
                    f"{i+1}. **{p['pokemon']}** ({p['cost']} pts)"
                    for i, p in enumerate(budget_info['drafted_pokemon'])
                ])
                embed.add_field(
                    name="Drafted Pokémon",
                    value=pokemon_list,
                    inline=False
                )

            await ctx.send(embed=embed)

        except ValueError as e:
            await ctx.send(f"❌ {str(e)}")
        except Exception as e:
            await ctx.send(f"❌ Error checking budget: {e}")

    @commands.command(name="available")
    async def view_available(self, ctx, max_cost: Optional[int] = None):
        """
        View available Pokémon to draft.

        Usage: !draft available [max_cost]
        Example: !draft available or !draft available 10
        """
        try:
            available = self.draft_service.get_available_pokemon(max_cost)

            if not available:
                await ctx.send("ℹ️ No Pokémon available within your budget!")
                return

            # Limit to first 20 to avoid message length issues
            display_count = min(20, len(available))
            pokemon_list = "\n".join([
                f"{i+1}. **{p['name']}** ({p['type1']}" +
                (f"/{p['type2']}" if p['type2'] else "") +
                f") - **{p['cost']} pts** [{p['tier']}]"
                for i, p in enumerate(available[:display_count])
            ])

            embed = discord.Embed(
                title=f"📋 Available Pokémon{f' (≤{max_cost} pts)' if max_cost else ''}",
                description=pokemon_list,
                color=EMBED_COLOR_INFO
            )
            embed.set_footer(text=f"Showing {display_count} of {len(available)} available Pokémon")

            await ctx.send(embed=embed)

        except ValueError as e:
            await ctx.send(f"❌ {str(e)}")
        except Exception as e:
            await ctx.send(f"❌ Error fetching available Pokémon: {e}")

    # ==================== ADMIN COMMANDS ====================

    @commands.command(name="undo")
    @commands.has_permissions(administrator=True)
    async def undo_pick(self, ctx):
        """Undo the last draft pick (admin only)."""
        try:
            undone_pick = self.draft_service.undo_last_pick()

            embed = discord.Embed(
                title="↩️ Pick Undone",
                description=f"Undid {undone_pick['player']}'s pick of **{undone_pick['pokemon']}**",
                color=EMBED_COLOR_WARNING
            )
            embed.add_field(
                name="Pick Details",
                value=(
                    f"**Pick #:** {undone_pick['pick_number']}\n"
                    f"**Cost:** {undone_pick['cost']} points\n"
                    f"**Round:** {undone_pick['round']}"
                ),
                inline=False
            )

            await ctx.send(embed=embed)

        except ValueError as e:
            await ctx.send(f"❌ {str(e)}")
        except Exception as e:
            await ctx.send(f"❌ Error undoing pick: {e}")

    @commands.command(name="end")
    @commands.has_permissions(administrator=True)
    async def end_draft(self, ctx):
        """End the draft manually (admin only)."""
        status = self.draft_service.get_draft_status()

        if not status["is_active"]:
            await ctx.send("ℹ️ No active draft to end.")
            return

        # Confirmation
        await ctx.send("⚠️ Are you sure you want to end the draft? Reply with `confirm` to proceed.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)

            if msg.content.lower() != 'confirm':
                await ctx.send("❌ Draft end cancelled.")
                return

            self.draft_service.end_draft()
            await ctx.send("✅ Draft has been ended manually.")

        except asyncio.TimeoutError:
            await ctx.send("❌ Timed out. Draft end cancelled.")


# Setup function for loading the cog
async def setup(bot):
    await bot.add_cog(Draft(bot))
