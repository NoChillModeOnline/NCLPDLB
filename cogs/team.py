"""
Team Management Cog

Handles all team-related commands:
- View teams and rosters
- Team validation and analysis
- Trade proposals and management
"""

import discord
from discord.ext import commands
from services.sheets_service import SheetsService
from services.team_validator import TeamValidator
from utils.constants import EMBED_COLOR_INFO, EMBED_COLOR_SUCCESS, EMBED_COLOR_WARNING, TYPE_EMOJI
import config


class Team(commands.Cog):
    """Team management and analysis commands"""

    def __init__(self, bot):
        self.bot = bot
        self.sheets = SheetsService(config.CONFIG['spreadsheet_id'])
        self.validator = TeamValidator(self.sheets)

    @commands.group(name='team', invoke_without_command=True)
    async def team(self, ctx, player: discord.Member = None):
        """
        View a team's roster

        Usage:
            !team @Player  - View another player's team
            !team          - View your own team (same as !roster)
        """
        target_player = player if player else ctx.author

        try:
            # Get team data
            team_data = self.sheets.get_team_by_player(target_player.display_name)

            if not team_data:
                await ctx.send(f"❌ {target_player.display_name} has not registered yet!")
                return

            # Create embed
            embed = discord.Embed(
                title=f"{team_data.get('team_name', 'Unknown Team')}",
                description=f"Coach: {target_player.mention}",
                color=EMBED_COLOR_INFO
            )

            # Add team logo if available
            team_logo = team_data.get('team_logo', '')
            if team_logo:
                embed.set_thumbnail(url=team_logo)

            # Add Pokemon list
            pokemon_list = team_data.get('pokemon_list', [])
            if pokemon_list:
                # Get detailed data for each Pokemon
                roster_lines = []
                for pkmn_name in pokemon_list:
                    pkmn_data = self.sheets.get_pokemon_data(pkmn_name)
                    if pkmn_data:
                        type1 = pkmn_data.get('type1', '').title()
                        type2 = pkmn_data.get('type2', '').title()
                        cost = pkmn_data.get('point_cost', 0)

                        type_str = f"{TYPE_EMOJI.get(type1, '⚪')} {type1}"
                        if type2:
                            type_str += f" / {TYPE_EMOJI.get(type2, '⚪')} {type2}"

                        roster_lines.append(f"**{pkmn_name}** ({cost} pts) - {type_str}")
                    else:
                        roster_lines.append(f"**{pkmn_name}** (? pts)")

                embed.add_field(
                    name=f"📋 Roster ({len(pokemon_list)} Pokémon)",
                    value="\n".join(roster_lines),
                    inline=False
                )
            else:
                embed.add_field(
                    name="📋 Roster",
                    value="*No Pokémon drafted yet*",
                    inline=False
                )

            # Add points info
            points_used = team_data.get('total_points_used', 0)
            points_remaining = 120 - points_used
            embed.add_field(
                name="💰 Point Budget",
                value=f"Used: {points_used}/120\nRemaining: {points_remaining}",
                inline=True
            )

            # Add Tera Captains
            tera_captains = self.sheets.get_tera_captains(target_player.display_name)
            if tera_captains:
                tera_lines = []
                for captain in tera_captains:
                    pokemon = captain['pokemon']
                    tera_type = captain['tera_type']
                    emoji = TYPE_EMOJI.get(tera_type, '✨')
                    tera_lines.append(f"{emoji} **{pokemon}** → {tera_type} Tera")

                embed.add_field(
                    name="⚡ Tera Captains",
                    value="\n".join(tera_lines),
                    inline=True
                )

            embed.set_footer(text=f"Use !analyze to see detailed team analysis")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error viewing team: {str(e)}")

    @commands.command(name='roster')
    async def roster(self, ctx):
        """
        View your own team roster (shortcut for !team)

        Usage:
            !roster
        """
        await self.team(ctx, player=None)

    @commands.command(name='analyze')
    async def analyze(self, ctx, player: discord.Member = None):
        """
        Analyze a team's composition with strategic insights

        Usage:
            !analyze          - Analyze your team
            !analyze @Player  - Analyze another player's team
        """
        target_player = player if player else ctx.author

        # Send "analyzing" message
        analyzing_msg = await ctx.send(f"🔍 Analyzing {target_player.display_name}'s team...")

        try:
            # Perform comprehensive analysis
            analysis = self.validator.analyze_team(target_player.display_name)

            if 'error' in analysis:
                await analyzing_msg.edit(content=f"❌ {analysis['error']}")
                return

            # Create main analysis embed
            team_data = analysis['team_data']
            embed = discord.Embed(
                title=f"📊 Team Analysis: {team_data.get('team_name', 'Unknown Team')}",
                description=f"Coach: {target_player.mention}",
                color=EMBED_COLOR_INFO
            )

            # Overall efficiency score
            efficiency = analysis.get('efficiency_score', 0)
            efficiency_emoji = "🟢" if efficiency >= 80 else "🟡" if efficiency >= 60 else "🔴"
            embed.add_field(
                name=f"{efficiency_emoji} Team Efficiency",
                value=f"**{efficiency}/100**",
                inline=True
            )

            # Pokemon count
            pkmn_count = analysis.get('pokemon_count', 0)
            embed.add_field(
                name="📋 Roster Size",
                value=f"**{pkmn_count} Pokémon**",
                inline=True
            )

            # Points used
            points_used = team_data.get('total_points_used', 0)
            embed.add_field(
                name="💰 Points Used",
                value=f"**{points_used}/120**",
                inline=True
            )

            await analyzing_msg.delete()

            # Send main embed
            await ctx.send(embed=embed)

            # Type Coverage Embed
            type_coverage = analysis['type_coverage']
            coverage_embed = discord.Embed(
                title="🌈 Type Coverage Analysis",
                color=EMBED_COLOR_INFO
            )

            # Type representation
            type_counts = type_coverage.get('type_counts', {})
            if type_counts:
                sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
                type_lines = [
                    f"{TYPE_EMOJI.get(t, '⚪')} **{t}**: {count}x"
                    for t, count in sorted_types[:10]
                ]
                coverage_embed.add_field(
                    name="📊 Type Distribution",
                    value="\n".join(type_lines),
                    inline=True
                )

            # Missing types
            missing_types = type_coverage.get('missing_types', [])
            if missing_types:
                missing_display = ", ".join(missing_types[:8])
                if len(missing_types) > 8:
                    missing_display += f"... (+{len(missing_types) - 8} more)"
                coverage_embed.add_field(
                    name="❌ Missing Types",
                    value=missing_display,
                    inline=True
                )

            await ctx.send(embed=coverage_embed)

            # Offensive Coverage Embed
            offensive = analysis['offensive_coverage']
            offensive_embed = discord.Embed(
                title="⚔️ Offensive Coverage",
                color=EMBED_COLOR_INFO
            )

            coverage_pct = offensive.get('coverage_percentage', 0)
            coverage_emoji = "✅" if coverage_pct >= 80 else "⚠️" if coverage_pct >= 60 else "❌"

            offensive_embed.add_field(
                name=f"{coverage_emoji} Coverage Score",
                value=f"**{coverage_pct:.0f}%** of types covered",
                inline=False
            )

            # Coverage gaps
            coverage_gaps = offensive.get('coverage_gaps', [])
            if coverage_gaps:
                gaps_display = ", ".join([
                    f"{TYPE_EMOJI.get(t, '⚪')} {t}"
                    for t in coverage_gaps[:6]
                ])
                if len(coverage_gaps) > 6:
                    gaps_display += f"\n... +{len(coverage_gaps) - 6} more"

                offensive_embed.add_field(
                    name="🚫 Cannot Hit Super-Effectively",
                    value=gaps_display,
                    inline=False
                )

            await ctx.send(embed=offensive_embed)

            # Weaknesses Embed
            weaknesses = analysis['weaknesses']
            weakness_embed = discord.Embed(
                title="🛡️ Team Weaknesses",
                color=EMBED_COLOR_WARNING
            )

            # Critical weaknesses
            critical = weaknesses.get('critical_weaknesses', {})
            if critical:
                critical_lines = [
                    f"{TYPE_EMOJI.get(t, '⚪')} **{t}**: Hits {count}/{pkmn_count} Pokémon"
                    for t, count in sorted(critical.items(), key=lambda x: x[1], reverse=True)
                ]
                weakness_embed.add_field(
                    name="⚠️ Critical Weaknesses (4+ Pokémon)",
                    value="\n".join(critical_lines),
                    inline=False
                )
            else:
                weakness_embed.add_field(
                    name="✅ No Critical Weaknesses",
                    value="No type hits more than 3 Pokémon super-effectively",
                    inline=False
                )

            # Shared weaknesses
            shared = weaknesses.get('shared_weaknesses', {})
            if shared:
                shared_lines = [
                    f"{TYPE_EMOJI.get(t, '⚪')} **{t}**: {count} Pokémon"
                    for t, count in sorted(shared.items(), key=lambda x: x[1], reverse=True)[:5]
                ]
                weakness_embed.add_field(
                    name="⚡ Common Weaknesses (50%+ of team)",
                    value="\n".join(shared_lines),
                    inline=False
                )

            await ctx.send(embed=weakness_embed)

            # Tera Suggestions Embed
            tera_suggestions = analysis.get('tera_suggestions', [])
            if tera_suggestions:
                tera_embed = discord.Embed(
                    title="💡 Tera Captain Suggestions",
                    description="Strategic Tera types to cover your team's weaknesses",
                    color=EMBED_COLOR_INFO
                )

                for suggestion in tera_suggestions[:3]:
                    weakness = suggestion['covers_weakness']
                    affects = suggestion['affects_pokemon']
                    suggested_types = suggestion['suggested_tera_types']
                    priority = suggestion['priority']

                    priority_emoji = "🔴" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢"

                    types_display = ", ".join([
                        f"{TYPE_EMOJI.get(t, '✨')} {t}"
                        for t in suggested_types
                    ])

                    tera_embed.add_field(
                        name=f"{priority_emoji} Cover {TYPE_EMOJI.get(weakness, '⚪')} {weakness} Weakness",
                        value=f"Affects **{affects}** Pokémon\nSuggested: {types_display}",
                        inline=False
                    )

                await ctx.send(embed=tera_embed)

            # Speed Tiers Embed
            speed_tiers = analysis['speed_tiers']
            speed_embed = discord.Embed(
                title="⚡ Speed Tier Distribution",
                color=EMBED_COLOR_INFO
            )

            tiers = speed_tiers.get('tiers', {})
            fast = tiers.get('fast', [])
            medium = tiers.get('medium', [])
            slow = tiers.get('slow', [])

            if fast:
                fast_list = [f"**{name}** ({spd})" for name, spd in fast[:5]]
                speed_embed.add_field(
                    name=f"💨 Fast (≥100 Speed) - {len(fast)} Pokémon",
                    value="\n".join(fast_list) if fast_list else "None",
                    inline=True
                )

            if medium:
                medium_list = [f"**{name}** ({spd})" for name, spd in medium[:5]]
                speed_embed.add_field(
                    name=f"⚡ Medium (60-99 Speed) - {len(medium)} Pokémon",
                    value="\n".join(medium_list) if medium_list else "None",
                    inline=True
                )

            if slow:
                slow_list = [f"**{name}** ({spd})" for name, spd in slow[:5]]
                speed_embed.add_field(
                    name=f"🐢 Slow (<60 Speed) - {len(slow)} Pokémon",
                    value="\n".join(slow_list) if slow_list else "None",
                    inline=True
                )

            avg_speed = speed_tiers.get('average_speed', 0)
            speed_embed.add_field(
                name="📊 Average Speed",
                value=f"**{avg_speed}**",
                inline=False
            )

            await ctx.send(embed=speed_embed)

            # Warnings and Strengths Embed
            summary_embed = discord.Embed(
                title="📝 Team Summary",
                color=EMBED_COLOR_SUCCESS if efficiency >= 70 else EMBED_COLOR_WARNING
            )

            # Strengths
            strengths = analysis.get('strengths', [])
            if strengths:
                summary_embed.add_field(
                    name="💪 Strengths",
                    value="\n".join(strengths),
                    inline=False
                )

            # Warnings
            warnings = analysis.get('warnings', [])
            if warnings:
                summary_embed.add_field(
                    name="⚠️ Areas to Improve",
                    value="\n".join(warnings),
                    inline=False
                )
            else:
                summary_embed.add_field(
                    name="✅ Well-Balanced Team",
                    value="No major weaknesses detected!",
                    inline=False
                )

            await ctx.send(embed=summary_embed)

        except Exception as e:
            await analyzing_msg.edit(content=f"❌ Error during analysis: {str(e)}")
            import traceback
            print(f"Analysis error: {traceback.format_exc()}")

    @commands.command(name='teams')
    async def teams(self, ctx):
        """
        List all teams in the league

        Usage:
            !teams
        """
        try:
            # Get all teams from Teams sheet
            all_teams = self.sheets.get_all_records(self.sheets.SHEET_TEAMS)

            if not all_teams:
                await ctx.send("📋 No teams registered yet!")
                return

            # Create embed
            embed = discord.Embed(
                title="🏆 All Teams in the League",
                description=f"Total: {len(all_teams)} coaches",
                color=EMBED_COLOR_INFO
            )

            # Group by team
            for team in all_teams:
                player = team.get('player', 'Unknown')
                team_name = team.get('team_name', 'Unknown Team')
                pokemon_count = len(team.get('pokemon_list', []))
                points_used = team.get('total_points_used', 0)

                embed.add_field(
                    name=f"{team_name}",
                    value=f"Coach: **{player}**\nRoster: {pokemon_count} Pokémon\nPoints: {points_used}/120",
                    inline=True
                )

            embed.set_footer(text="Use !team @Player to view detailed roster")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error listing teams: {str(e)}")

    @commands.command(name='dmanalysis')
    async def dm_analysis(self, ctx, player: discord.Member = None):
        """
        Send team analysis via Direct Message

        Usage:
            !dmanalysis          - Receive your analysis via DM
            !dmanalysis @Player  - Send analysis to another player (admin only)

        The bot will send a comprehensive 7-embed analysis directly to your DMs,
        keeping your team strategy private.
        """
        target_player = player if player else ctx.author

        # Check permissions if targeting another player
        if player and player != ctx.author:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ Only administrators can send analysis to other players!")
                return

        # Confirm in channel
        status_msg = await ctx.send(f"📨 Preparing team analysis for {target_player.mention}...")

        try:
            # Perform analysis
            analysis = self.validator.analyze_team(target_player.display_name)

            if 'error' in analysis:
                await status_msg.edit(content=f"❌ {analysis['error']}")
                return

            # Try to DM the user
            try:
                await target_player.send(f"# 📊 Your Team Analysis\n\nHere's a comprehensive analysis of your team in **{ctx.guild.name}**:")

                # Send all embeds via DM
                embeds_sent = 0

                # 1. Main Analysis
                team_data = analysis['team_data']
                embed = discord.Embed(
                    title=f"📊 Team Analysis: {team_data.get('team_name', 'Unknown Team')}",
                    description=f"Coach: {target_player.mention}",
                    color=EMBED_COLOR_INFO
                )

                efficiency = analysis.get('efficiency_score', 0)
                efficiency_emoji = "🟢" if efficiency >= 80 else "🟡" if efficiency >= 60 else "🔴"
                embed.add_field(
                    name=f"{efficiency_emoji} Team Efficiency",
                    value=f"**{efficiency}/100**",
                    inline=True
                )

                pkmn_count = analysis.get('pokemon_count', 0)
                embed.add_field(
                    name="📋 Roster Size",
                    value=f"**{pkmn_count} Pokémon**",
                    inline=True
                )

                points_used = team_data.get('total_points_used', 0)
                embed.add_field(
                    name="💰 Points Used",
                    value=f"**{points_used}/120**",
                    inline=True
                )

                await target_player.send(embed=embed)
                embeds_sent += 1

                # 2. Type Coverage
                type_coverage = analysis['type_coverage']
                coverage_embed = discord.Embed(
                    title="🌈 Type Coverage Analysis",
                    color=EMBED_COLOR_INFO
                )

                type_counts = type_coverage.get('type_counts', {})
                if type_counts:
                    sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
                    type_lines = [
                        f"{TYPE_EMOJI.get(t, '⚪')} **{t}**: {count}x"
                        for t, count in sorted_types[:10]
                    ]
                    coverage_embed.add_field(
                        name="📊 Type Distribution",
                        value="\n".join(type_lines),
                        inline=True
                    )

                missing_types = type_coverage.get('missing_types', [])
                if missing_types:
                    missing_display = ", ".join(missing_types[:8])
                    if len(missing_types) > 8:
                        missing_display += f"... (+{len(missing_types) - 8} more)"
                    coverage_embed.add_field(
                        name="❌ Missing Types",
                        value=missing_display,
                        inline=True
                    )

                await target_player.send(embed=coverage_embed)
                embeds_sent += 1

                # 3. Offensive Coverage
                offensive = analysis['offensive_coverage']
                offensive_embed = discord.Embed(
                    title="⚔️ Offensive Coverage",
                    color=EMBED_COLOR_INFO
                )

                coverage_pct = offensive.get('coverage_percentage', 0)
                coverage_emoji = "✅" if coverage_pct >= 80 else "⚠️" if coverage_pct >= 60 else "❌"

                offensive_embed.add_field(
                    name=f"{coverage_emoji} Coverage Score",
                    value=f"**{coverage_pct:.0f}%** of types covered",
                    inline=False
                )

                coverage_gaps = offensive.get('coverage_gaps', [])
                if coverage_gaps:
                    gaps_display = ", ".join([
                        f"{TYPE_EMOJI.get(t, '⚪')} {t}"
                        for t in coverage_gaps[:6]
                    ])
                    if len(coverage_gaps) > 6:
                        gaps_display += f"\n... +{len(coverage_gaps) - 6} more"

                    offensive_embed.add_field(
                        name="🚫 Cannot Hit Super-Effectively",
                        value=gaps_display,
                        inline=False
                    )

                await target_player.send(embed=offensive_embed)
                embeds_sent += 1

                # 4. Weaknesses
                weaknesses = analysis['weaknesses']
                weakness_embed = discord.Embed(
                    title="🛡️ Team Weaknesses",
                    color=EMBED_COLOR_WARNING
                )

                critical = weaknesses.get('critical_weaknesses', {})
                if critical:
                    critical_lines = [
                        f"{TYPE_EMOJI.get(t, '⚪')} **{t}**: Hits {count}/{pkmn_count} Pokémon"
                        for t, count in sorted(critical.items(), key=lambda x: x[1], reverse=True)
                    ]
                    weakness_embed.add_field(
                        name="⚠️ Critical Weaknesses (4+ Pokémon)",
                        value="\n".join(critical_lines),
                        inline=False
                    )
                else:
                    weakness_embed.add_field(
                        name="✅ No Critical Weaknesses",
                        value="No type hits more than 3 Pokémon super-effectively",
                        inline=False
                    )

                shared = weaknesses.get('shared_weaknesses', {})
                if shared:
                    shared_lines = [
                        f"{TYPE_EMOJI.get(t, '⚪')} **{t}**: {count} Pokémon"
                        for t, count in sorted(shared.items(), key=lambda x: x[1], reverse=True)[:5]
                    ]
                    weakness_embed.add_field(
                        name="⚡ Common Weaknesses (50%+ of team)",
                        value="\n".join(shared_lines),
                        inline=False
                    )

                await target_player.send(embed=weakness_embed)
                embeds_sent += 1

                # 5. Tera Suggestions
                tera_suggestions = analysis.get('tera_suggestions', [])
                if tera_suggestions:
                    tera_embed = discord.Embed(
                        title="💡 Tera Captain Suggestions",
                        description="Strategic Tera types to cover your team's weaknesses",
                        color=EMBED_COLOR_INFO
                    )

                    for suggestion in tera_suggestions[:3]:
                        weakness = suggestion['covers_weakness']
                        affects = suggestion['affects_pokemon']
                        suggested_types = suggestion['suggested_tera_types']
                        priority = suggestion['priority']

                        priority_emoji = "🔴" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢"

                        types_display = ", ".join([
                            f"{TYPE_EMOJI.get(t, '✨')} {t}"
                            for t in suggested_types
                        ])

                        tera_embed.add_field(
                            name=f"{priority_emoji} Cover {TYPE_EMOJI.get(weakness, '⚪')} {weakness} Weakness",
                            value=f"Affects **{affects}** Pokémon\nSuggested: {types_display}",
                            inline=False
                        )

                    await target_player.send(embed=tera_embed)
                    embeds_sent += 1

                # 6. Speed Tiers
                speed_tiers = analysis['speed_tiers']
                speed_embed = discord.Embed(
                    title="⚡ Speed Tier Distribution",
                    color=EMBED_COLOR_INFO
                )

                tiers = speed_tiers.get('tiers', {})
                fast = tiers.get('fast', [])
                medium = tiers.get('medium', [])
                slow = tiers.get('slow', [])

                if fast:
                    fast_list = [f"**{name}** ({spd})" for name, spd in fast[:5]]
                    speed_embed.add_field(
                        name=f"💨 Fast (≥100 Speed) - {len(fast)} Pokémon",
                        value="\n".join(fast_list) if fast_list else "None",
                        inline=True
                    )

                if medium:
                    medium_list = [f"**{name}** ({spd})" for name, spd in medium[:5]]
                    speed_embed.add_field(
                        name=f"⚡ Medium (60-99 Speed) - {len(medium)} Pokémon",
                        value="\n".join(medium_list) if medium_list else "None",
                        inline=True
                    )

                if slow:
                    slow_list = [f"**{name}** ({spd})" for name, spd in slow[:5]]
                    speed_embed.add_field(
                        name=f"🐢 Slow (<60 Speed) - {len(slow)} Pokémon",
                        value="\n".join(slow_list) if slow_list else "None",
                        inline=True
                    )

                avg_speed = speed_tiers.get('average_speed', 0)
                speed_embed.add_field(
                    name="📊 Average Speed",
                    value=f"**{avg_speed}**",
                    inline=False
                )

                await target_player.send(embed=speed_embed)
                embeds_sent += 1

                # 7. Summary
                summary_embed = discord.Embed(
                    title="📝 Team Summary",
                    color=EMBED_COLOR_SUCCESS if efficiency >= 70 else EMBED_COLOR_WARNING
                )

                strengths = analysis.get('strengths', [])
                if strengths:
                    summary_embed.add_field(
                        name="💪 Strengths",
                        value="\n".join(strengths),
                        inline=False
                    )

                warnings = analysis.get('warnings', [])
                if warnings:
                    summary_embed.add_field(
                        name="⚠️ Areas to Improve",
                        value="\n".join(warnings),
                        inline=False
                    )
                else:
                    summary_embed.add_field(
                        name="✅ Well-Balanced Team",
                        value="No major weaknesses detected!",
                        inline=False
                    )

                summary_embed.set_footer(text="💡 Use these insights to optimize your team and set strategic Tera Captains!")

                await target_player.send(embed=summary_embed)
                embeds_sent += 1

                # Final message with resources
                resources_msg = (
                    f"\n📚 **Competitive Resources:**\n"
                    f"• **Smogon Dex:** https://www.smogon.com/dex/\n"
                    f"• **Pikalytics:** https://pikalytics.com/\n"
                    f"• **Damage Calc:** https://calc.pokemonshowdown.com/\n"
                    f"\n💡 **Next Steps:**\n"
                    f"• Review your Tera Captain suggestions\n"
                    f"• Check coverage gaps and consider trades\n"
                    f"• Research matchups on Smogon\n"
                    f"• Use `!tera set <pokemon> <type>` to designate captains"
                )

                await target_player.send(resources_msg)

                # Confirm in channel
                await status_msg.edit(
                    content=f"✅ Sent {embeds_sent} analysis embeds to {target_player.mention} via DM!"
                )

            except discord.Forbidden:
                await status_msg.edit(
                    content=f"❌ Cannot send DM to {target_player.mention}. They may have DMs disabled.\n"
                            f"💡 {target_player.mention}, enable DMs from server members in Privacy Settings, then try again."
                )

        except Exception as e:
            await status_msg.edit(content=f"❌ Error during analysis: {str(e)}")
            import traceback
            print(f"DM Analysis error: {traceback.format_exc()}")


async def setup(bot):
    """Add the cog to the bot"""
    await bot.add_cog(Team(bot))
