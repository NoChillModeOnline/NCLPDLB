"""
League management commands for Pokemon Draft League Bot.

Handles league initialization, coach registration, season start,
coach management, error diagnostics, and league reset.
"""

import discord
from discord.ext import commands
import asyncio
from typing import Optional

from services.discord_service import DiscordService
from services.error_diagnostics import ErrorDiagnostics
from utils.constants import (
    EMBED_COLOR_SUCCESS,
    EMBED_COLOR_ERROR,
    EMBED_COLOR_WARNING,
    EMBED_COLOR_INFO,
    DEFAULT_MIN_POKEMON,
    DEFAULT_MAX_POKEMON
)


class League(commands.Cog):
    """League initialization and management commands"""

    def __init__(self, bot):
        self.bot = bot

        # Use shared SheetsService instance from bot (optimization)
        self.sheets = bot.sheets
        self.discord_service = DiscordService(bot)
        self.diagnostics = ErrorDiagnostics(self.sheets)

    # ==================== LEAGUE INITIALIZATION ====================

    @commands.command(name="league")
    async def league_base(self, ctx):
        """Base command - shows league help"""
        embed = discord.Embed(
            title="🎮 League Commands",
            description="Manage your Pokémon Draft League",
            color=EMBED_COLOR_INFO
        )

        embed.add_field(
            name="📋 Setup Commands",
            value=(
                "`!league init <name>` - Initialize new league (admin)\n"
                "`!league register <team_name> <logo_url>` - Register as coach\n"
                "`!league uploadlogo` - Upload team logo (attach image)\n"
                "`!league start` - Start season & create channels (admin)"
            ),
            inline=False
        )

        embed.add_field(
            name="👥 Coach Management",
            value=(
                "`!league addcoach @user` - Add coach to league (admin)\n"
                "`!league removecoach @user` - Remove coach (admin)"
            ),
            inline=False
        )

        embed.add_field(
            name="🔧 Maintenance",
            value=(
                "`!league diagnose` - Run error diagnostics (admin)\n"
                "`!league reset` - Reset entire league (admin)"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="init")
    @commands.has_permissions(administrator=True)
    async def init_league(self, ctx, *, league_name: str):
        """
        Initialize a new draft league (admin only).

        Usage: !league init <league_name>
        Example: !league init Summer 2026 League
        """
        # Store league name in Config sheet
        try:
            # This would update Config sheet - implement based on your sheet structure
            await ctx.send(f"⚠️ Config sheet update not yet implemented")

            # Create Coach role
            await self.discord_service.create_coach_role(ctx.guild)

            # Announce league creation
            embed = discord.Embed(
                title="🎉 League Initialized!",
                description=f"**{league_name}** has been created!",
                color=EMBED_COLOR_SUCCESS
            )

            embed.add_field(
                name="📝 Next Steps",
                value=(
                    "1. Coaches: Use `!league register <team_name> <logo_url>` to join\n"
                    "2. Complete the draft with `!draft start`\n"
                    "3. Admin: Start season with `!league start`"
                ),
                inline=False
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error initializing league: {e}")

    @commands.command(name="register")
    async def register_coach(self, ctx, team_name: str, team_logo: str = ""):
        """
        Register as a coach in the league.

        Usage: !league register "Team Name" <logo_url>
        Example: !league register "Fire Fighters" https://i.imgur.com/logo.png
        """
        player_name = ctx.author.display_name

        try:
            # Assign Coach role
            await self.discord_service.assign_coach_role(ctx.guild, ctx.author)

            # Store in Teams sheet (basic entry - roster added during draft)
            # This would be implemented with sheets service method
            await ctx.send(f"⚠️ Teams sheet update not yet implemented")

            # Announce registration
            embed = discord.Embed(
                title="✅ Coach Registered!",
                description=f"{ctx.author.mention} joined as **{team_name}**",
                color=EMBED_COLOR_SUCCESS
            )

            if team_logo:
                embed.set_thumbnail(url=team_logo)

            embed.add_field(
                name="📝 Next Steps",
                value="Wait for the draft to begin!",
                inline=False
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error registering: {e}")

    @commands.command(name="uploadlogo")
    async def upload_logo(self, ctx):
        """
        Upload team logo by attaching an image file.

        Usage: !league uploadlogo (attach an image file)
        """
        player_name = ctx.author.display_name

        # Check if user has Coach role
        coach_role = discord.utils.get(ctx.guild.roles, name="Coach")
        if not coach_role or coach_role not in ctx.author.roles:
            await ctx.send("❌ You must be registered as a coach first! Use `!league register`")
            return

        # Check for attachment
        if not ctx.message.attachments:
            await ctx.send(
                "❌ Please attach an image file when using this command!\n"
                "Example: Use `!league uploadlogo` and attach your team logo image."
            )
            return

        attachment = ctx.message.attachments[0]

        # Validate it's an image
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        if not any(attachment.filename.lower().endswith(ext) for ext in valid_extensions):
            await ctx.send(
                f"❌ Invalid file type! Please upload an image file.\n"
                f"Supported formats: PNG, JPG, JPEG, GIF, WEBP"
            )
            return

        # Check file size (max 8MB for Discord)
        if attachment.size > 8 * 1024 * 1024:
            await ctx.send("❌ File too large! Maximum size is 8MB.")
            return

        try:
            # Get the attachment URL (Discord hosts it)
            logo_url = attachment.url

            # Update team logo in Google Sheets
            # This would be implemented with sheets service method
            await ctx.send(f"⚠️ Sheet update for logo not yet implemented")

            # Confirmation embed with logo preview
            embed = discord.Embed(
                title="✅ Team Logo Uploaded!",
                description=f"Logo updated for {ctx.author.mention}",
                color=EMBED_COLOR_SUCCESS
            )
            embed.set_image(url=logo_url)
            embed.add_field(
                name="Logo URL",
                value=f"[View Full Size]({logo_url})",
                inline=False
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error uploading logo: {e}")

    # ==================== SEASON START ====================

    @commands.command(name="start")
    @commands.has_permissions(administrator=True)
    async def start_league(self, ctx):
        """
        Start the league season (creates coach channels).

        IMPORTANT: Only use AFTER draft is 100% complete!
        """
        await ctx.send("🚀 Starting league season... Validating rosters...")

        # Verify all teams have valid rosters
        teams = self.sheets.get_all_teams()

        if not teams:
            await ctx.send("❌ No teams found! Coaches must register first.")
            return

        incomplete_teams = []

        for player_name, team_data in teams.items():
            roster = team_data.get("roster", [])
            if not roster or len(roster) < DEFAULT_MIN_POKEMON:
                incomplete_teams.append(player_name)

        if incomplete_teams:
            embed = discord.Embed(
                title="❌ Cannot Start Season",
                description="Some teams don't have complete rosters!",
                color=EMBED_COLOR_ERROR
            )
            embed.add_field(
                name="Incomplete Teams",
                value="\n".join(incomplete_teams),
                inline=False
            )
            embed.add_field(
                name="Required",
                value=f"Minimum {DEFAULT_MIN_POKEMON} Pokémon per team",
                inline=False
            )
            await ctx.send(embed=embed)
            return

        await ctx.send("✅ All rosters validated! Creating coach channels...")

        # Create category
        category = await self.discord_service.create_coach_category(ctx.guild)

        # Create channel for each coach
        created_count = 0
        errors = []

        for player_name, team_data in teams.items():
            try:
                # Find Discord member
                member = discord.utils.find(
                    lambda m: m.display_name == player_name or m.name == player_name,
                    ctx.guild.members
                )

                if not member:
                    errors.append(f"Could not find Discord member for {player_name}")
                    continue

                # Get roster and Tera Captains
                roster = team_data["roster"]
                tera_captains = self.sheets.get_tera_captains(player_name)

                # Create channel
                await self.discord_service.create_coach_channel(
                    guild=ctx.guild,
                    category=category,
                    coach=member,
                    team_name=team_data["team_name"],
                    team_logo=team_data.get("team_logo", ""),
                    roster=roster,
                    tera_captains=tera_captains
                )

                created_count += 1

            except Exception as e:
                errors.append(f"Error creating channel for {player_name}: {e}")

        # Announce completion
        embed = discord.Embed(
            title="🎮 League Season Started! 🎮",
            description=f"Created {created_count} coach channels!",
            color=EMBED_COLOR_SUCCESS
        )

        embed.add_field(
            name="Next Steps",
            value="• Check your private channel\n• Review your roster\n• Prepare for Week 1 battles!",
            inline=False
        )

        if errors:
            embed.add_field(
                name="⚠️ Warnings",
                value="\n".join(errors[:5]),  # Show first 5 errors
                inline=False
            )

        await ctx.send(embed=embed)

    # ==================== COACH MANAGEMENT ====================

    @commands.command(name="addcoach")
    @commands.has_permissions(administrator=True)
    async def add_coach(self, ctx, member: discord.Member):
        """
        Add a coach to the league (reads data from Google Sheet).

        Usage: !league addcoach @user
        """
        # Check if user already has Coach role
        coach_role = discord.utils.get(ctx.guild.roles, name="Coach")
        if coach_role and coach_role in member.roles:
            await ctx.send(f"❌ {member.mention} is already a coach!")
            return

        # Check if Teams sheet has data for this player
        await ctx.send(f"🔍 Looking for {member.display_name}'s data in Google Sheets...")

        try:
            team_data = self.sheets.get_team_by_player(member.display_name)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Team Data Not Found",
                description=f"Could not find team data for {member.display_name}",
                color=EMBED_COLOR_ERROR
            )
            embed.add_field(
                name="Please Add Their Data First",
                value=(
                    "**Required sheets:**\n"
                    "• Teams: Player, Team_Name, Team_Logo, Pokemon_List\n"
                    "• Draft_History: Their draft picks\n"
                    "• Tera_Captains: Their Tera Captain choices"
                ),
                inline=False
            )
            await ctx.send(embed=embed)
            return

        # Assign Coach role
        await self.discord_service.assign_coach_role(ctx.guild, member)
        await ctx.send(f"✅ Assigned Coach role to {member.mention}")

        # Get category (or create if doesn't exist)
        category = await self.discord_service.create_coach_category(ctx.guild)

        # Get roster and Tera Captains from sheets
        roster = team_data.get("roster", [])
        tera_captains = self.sheets.get_tera_captains(member.display_name)

        if not roster:
            await ctx.send(
                f"⚠️ Warning: {member.display_name} has no Pokémon in their roster!\n"
                f"Please update the Teams sheet."
            )

        # Create coach channel
        await ctx.send(f"📝 Creating private channel for {team_data['team_name']}...")

        channel = await self.discord_service.create_coach_channel(
            guild=ctx.guild,
            category=category,
            coach=member,
            team_name=team_data["team_name"],
            team_logo=team_data.get("team_logo", ""),
            roster=roster,
            tera_captains=tera_captains
        )

        # Announce to main channel
        embed = discord.Embed(
            title="🎉 New Coach Joined!",
            description=f"Welcome {member.mention} to the league!",
            color=EMBED_COLOR_SUCCESS
        )
        embed.add_field(name="Team", value=team_data["team_name"], inline=True)
        embed.add_field(name="Pokémon", value=len(roster), inline=True)

        if team_data.get("team_logo"):
            embed.set_thumbnail(url=team_data["team_logo"])

        await ctx.send(embed=embed)
        await ctx.send(f"✅ {member.mention} Your private channel is ready: {channel.mention}")

    @commands.command(name="removecoach")
    @commands.has_permissions(administrator=True)
    async def remove_coach(self, ctx, member: discord.Member):
        """
        Remove a coach from the league (preserves match history).

        Usage: !league removecoach @user
        """
        # Check if user is a coach
        coach_role = discord.utils.get(ctx.guild.roles, name="Coach")
        if not coach_role or coach_role not in member.roles:
            await ctx.send(f"❌ {member.mention} is not a coach!")
            return

        # Get team data for confirmation
        try:
            team_data = self.sheets.get_team_by_player(member.display_name)
            team_name = team_data["team_name"]
        except Exception:
            team_name = member.display_name

        # Confirmation with warning
        embed = discord.Embed(
            title="⚠️ Remove Coach Confirmation",
            description=f"Are you sure you want to remove {member.mention} ({team_name})?",
            color=EMBED_COLOR_WARNING
        )
        embed.add_field(
            name="✅ What will be preserved:",
            value=(
                "• Match history (kills, deaths, +/-)\n"
                "• Draft history\n"
                "• Standings record (marked inactive)"
            ),
            inline=False
        )
        embed.add_field(
            name="❌ What will be removed:",
            value=(
                "• Private channel\n"
                "• Coach role\n"
                "• Active team data (archived first)"
            ),
            inline=False
        )
        embed.set_footer(text="Reply with 'confirm' to proceed or 'cancel' to abort")

        await ctx.send(embed=embed)

        # Wait for confirmation
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("❌ Timed out. Coach removal cancelled.")
            return

        if msg.content.lower() != 'confirm':
            await ctx.send("❌ Coach removal cancelled.")
            return

        # Proceed with removal
        await ctx.send(f"🗑️ Removing coach {member.mention}...")

        # 1. Archive team data
        try:
            self.sheets.archive_team(member.display_name, team_data)
            await ctx.send("✅ Team data archived")
        except Exception as e:
            await ctx.send(f"⚠️ Could not archive team data: {e}")

        # 2. Mark as inactive in Standings
        try:
            self.sheets.mark_team_inactive(member.display_name)
            await ctx.send("✅ Marked as inactive in standings")
        except Exception as e:
            await ctx.send(f"⚠️ Could not update standings: {e}")

        # 3. Remove Tera Captains entries
        try:
            self.sheets.clear_tera_captains(member.display_name)
            await ctx.send("✅ Cleared Tera Captain data")
        except Exception as e:
            await ctx.send(f"⚠️ Could not clear Tera Captains: {e}")

        # 4. Delete coach channel
        channel_deleted = await self.discord_service.remove_coach_channel(ctx.guild, team_name)
        if channel_deleted:
            await ctx.send("✅ Deleted private channel")
        else:
            await ctx.send("⚠️ Could not find private channel to delete")

        # 5. Remove Coach role
        role_removed = await self.discord_service.remove_coach_role(ctx.guild, member)
        if role_removed:
            await ctx.send("✅ Removed Coach role")
        else:
            await ctx.send("⚠️ Coach role already removed")

        # Final announcement
        embed = discord.Embed(
            title="👋 Coach Removed",
            description=f"{member.mention} ({team_name}) has been removed from the league.",
            color=EMBED_COLOR_ERROR
        )
        embed.add_field(
            name="Historical Data",
            value="All match history and stats have been preserved.",
            inline=False
        )

        await ctx.send(embed=embed)

    # ==================== DIAGNOSTICS ====================

    @commands.command(name="diagnose")
    @commands.has_permissions(administrator=True)
    async def diagnose_league(self, ctx):
        """
        Run spreadsheet error diagnostics (admin only).

        Usage: !league diagnose
        """
        await ctx.send("🔍 Running error diagnostics... This may take a moment.")

        try:
            # Run full diagnostic
            results = self.diagnostics.run_full_diagnostic()

            # Create summary embed
            embed = discord.Embed(
                title="📊 Diagnostic Results",
                color=EMBED_COLOR_INFO
            )

            # Add summary
            embed.add_field(
                name="Total Errors Found",
                value=f"**{results['total_errors']}**",
                inline=True
            )

            # Add severity breakdown
            severity_text = ""
            if results['critical'] > 0:
                severity_text += f"🚨 Critical: {results['critical']}\n"
            if results['high'] > 0:
                severity_text += f"⚠️ High: {results['high']}\n"
            if results['medium'] > 0:
                severity_text += f"⚡ Medium: {results['medium']}\n"
            if results['low'] > 0:
                severity_text += f"ℹ️ Low: {results['low']}\n"

            if severity_text:
                embed.add_field(
                    name="Severity Breakdown",
                    value=severity_text,
                    inline=True
                )

            # Add auto-fixable count
            embed.add_field(
                name="Auto-Fixable",
                value=f"**{results['auto_fixable']}**",
                inline=True
            )

            # Add details if errors found
            if results['total_errors'] > 0:
                embed.add_field(
                    name="📝 Details",
                    value="Check the `Error_Diagnostics` sheet in Google Sheets for full details.",
                    inline=False
                )
                embed.color = EMBED_COLOR_WARNING
            else:
                embed.add_field(
                    name="✅ All Clear!",
                    value="No errors detected in your league data.",
                    inline=False
                )
                embed.color = EMBED_COLOR_SUCCESS

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error running diagnostics: {e}")

    # ==================== LEAGUE RESET ====================

    @commands.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def reset_league(self, ctx):
        """
        Reset the entire league (admin only, nuclear option).

        Usage: !league reset
        """
        # Confirmation with BIG warning
        embed = discord.Embed(
            title="🚨 LEAGUE RESET WARNING 🚨",
            description="This will **DELETE ALL LEAGUE DATA**!",
            color=EMBED_COLOR_ERROR
        )
        embed.add_field(
            name="What will be deleted:",
            value=(
                "• All draft picks\n"
                "• All team rosters\n"
                "• All Tera Captains\n"
                "• All coach channels\n"
                "• All Coach roles\n"
                "• Match history (if implemented)\n"
                "• Standings (if implemented)"
            ),
            inline=False
        )
        embed.add_field(
            name="⚠️ THIS CANNOT BE UNDONE!",
            value="Reply with `DELETE EVERYTHING` to proceed or `cancel` to abort",
            inline=False
        )

        await ctx.send(embed=embed)

        # Wait for confirmation
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("❌ Timed out. League reset cancelled.")
            return

        if msg.content != 'DELETE EVERYTHING':
            await ctx.send("❌ League reset cancelled.")
            return

        # Proceed with reset
        await ctx.send("🗑️ Resetting league... This will take a moment.")

        # Delete all coach channels
        await self.discord_service.delete_coach_channels(ctx.guild)
        await ctx.send("✅ Deleted all coach channels")

        # Remove all coach roles
        await self.discord_service.remove_all_coach_roles(ctx.guild)
        await ctx.send("✅ Removed all Coach roles")

        # Note: Sheet data deletion would be implemented with sheets service methods
        await ctx.send("⚠️ Sheet data deletion not yet implemented")

        # Final message
        embed = discord.Embed(
            title="✅ League Reset Complete",
            description="The league has been reset. Use `!league init` to start a new season.",
            color=EMBED_COLOR_SUCCESS
        )

        await ctx.send(embed=embed)


# Setup function for loading the cog
async def setup(bot):
    await bot.add_cog(League(bot))
