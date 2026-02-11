"""
Discord service for Pokemon Draft League Bot.

Handles all Discord server automation including category creation,
channel management, role assignment, and permission configuration.
"""

import discord
from typing import List, Dict, Optional
from utils.text_formatter import format_team_channel_name, format_category_name
from utils.constants import TYPE_EMOJI


class DiscordService:
    """Handles Discord server automation and management"""

    def __init__(self, bot):
        """
        Initialize Discord service.

        Args:
            bot: Discord bot instance
        """
        self.bot = bot

    # ==================== CATEGORY MANAGEMENT ====================

    async def create_coach_category(self, guild: discord.Guild) -> discord.CategoryChannel:
        """
        Create the Draft League Coaches category.

        Args:
            guild: Discord server

        Returns:
            Category channel object
        """
        category_name = format_category_name()

        # Check if category already exists
        existing = discord.utils.get(guild.categories, name=category_name)
        if existing:
            print(f"✅ Category already exists: {category_name}")
            return existing

        # Create new category
        category = await guild.create_category(category_name)
        print(f"✅ Created category: {category_name}")
        return category

    # ==================== CHANNEL MANAGEMENT ====================

    async def create_coach_channel(
        self,
        guild: discord.Guild,
        category: discord.CategoryChannel,
        coach: discord.Member,
        team_name: str,
        team_logo: str,
        roster: List[Dict],
        tera_captains: List[Dict]
    ) -> discord.TextChannel:
        """
        Create private channel for a coach with roster embed.

        Args:
            guild: Discord server
            category: Parent category for the channel
            coach: Discord member (the coach)
            team_name: Name of the team
            team_logo: URL to team logo image
            roster: List of Pokémon dictionaries
            tera_captains: List of Tera Captain dictionaries

        Returns:
            Created text channel
        """
        # Format channel name with small caps Unicode
        channel_name = format_team_channel_name(team_name)

        # Check if channel already exists
        existing = discord.utils.get(category.channels, name=channel_name)
        if existing:
            print(f"✅ Channel already exists: {channel_name}")
            return existing

        # Create channel with permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            coach: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            # Admin role permissions will be inherited from category/server settings
        }

        channel = await category.create_text_channel(
            name=channel_name,
            overwrites=overwrites
        )

        print(f"✅ Created channel: {channel_name} for {coach.name}")

        # Send welcome embed
        await self._send_coach_welcome(
            channel, coach, team_name, team_logo, roster, tera_captains
        )

        return channel

    async def _send_coach_welcome(
        self,
        channel: discord.TextChannel,
        coach: discord.Member,
        team_name: str,
        team_logo: str,
        roster: List[Dict],
        tera_captains: List[Dict]
    ):
        """
        Send welcome embed with team info to coach's channel.

        Args:
            channel: Coach's private channel
            coach: Discord member
            team_name: Team name (normal font)
            team_logo: URL to logo image
            roster: List of Pokémon with data
            tera_captains: List of Tera Captains
        """
        embed = discord.Embed(
            title=f"🏆 {team_name} 🏆",
            description=f"Welcome, Coach {coach.mention}!",
            color=discord.Color.gold()
        )

        # Set team logo as thumbnail
        if team_logo:
            try:
                embed.set_thumbnail(url=team_logo)
            except Exception as e:
                print(f"⚠️ Could not set team logo: {e}")

        # Add roster
        roster_text = ""
        total_points = 0

        for i, pokemon in enumerate(roster, 1):
            name = pokemon.get("name", "Unknown")
            type1 = pokemon.get("type1", "")
            type2 = pokemon.get("type2", "")
            cost = pokemon.get("point_cost", 0)
            total_points += cost

            # Format types
            types = f"{type1}" + (f"/{type2}" if type2 else "")

            # Mark Tera Captains with ⚡
            is_tera = any(tc["pokemon"] == name for tc in tera_captains)
            marker = "⚡ " if is_tera else ""

            roster_text += f"{i}. {marker}**{name}** ({types}) - {cost} pts\n"

        # Add roster field
        embed.add_field(
            name=f"📋 Roster ({len(roster)} Pokémon - {total_points}/120 pts)",
            value=roster_text if roster_text else "No Pokémon yet",
            inline=False
        )

        # Add Tera Captains section
        if tera_captains:
            tera_text = ""
            for tc in tera_captains:
                pokemon_name = tc["pokemon"]
                tera_type = tc["tera_type"]
                emoji = TYPE_EMOJI.get(tera_type, "⭐")
                point_cost = tc.get("point_cost", 0)

                tera_text += f"{emoji} **{pokemon_name}** → {tera_type} Type ({point_cost} pts)\n"

            embed.add_field(
                name="⚡ Tera Captains",
                value=tera_text,
                inline=False
            )

        # Add footer
        embed.set_footer(text="Good luck this season! 🎮")

        await channel.send(embed=embed)
        print(f"✅ Sent welcome embed to {channel.name}")

    async def delete_coach_channels(self, guild: discord.Guild):
        """
        Delete all coach channels (for league reset).

        Args:
            guild: Discord server
        """
        category_name = format_category_name()
        category = discord.utils.get(guild.categories, name=category_name)

        if not category:
            print("⚠️ Coach category not found")
            return

        # Delete all channels in category
        for channel in category.channels:
            await channel.delete()
            print(f"✅ Deleted channel: {channel.name}")

        # Delete category
        await category.delete()
        print(f"✅ Deleted category: {category_name}")

    async def remove_coach_channel(self, guild: discord.Guild, team_name: str) -> bool:
        """
        Remove a specific coach's channel.

        Args:
            guild: Discord server
            team_name: Name of the team

        Returns:
            True if channel was deleted, False if not found
        """
        category_name = format_category_name()
        category = discord.utils.get(guild.categories, name=category_name)

        if not category:
            print("⚠️ Coach category not found")
            return False

        channel_name = format_team_channel_name(team_name)
        channel = discord.utils.get(category.channels, name=channel_name)

        if channel:
            await channel.delete()
            print(f"✅ Deleted channel: {channel_name}")
            return True

        print(f"⚠️ Channel not found: {channel_name}")
        return False

    # ==================== ROLE MANAGEMENT ====================

    async def create_coach_role(self, guild: discord.Guild) -> discord.Role:
        """
        Create Coach role if it doesn't exist.

        Args:
            guild: Discord server

        Returns:
            Coach role object
        """
        role_name = "Coach"
        existing = discord.utils.get(guild.roles, name=role_name)

        if existing:
            print(f"✅ Coach role already exists")
            return existing

        # Create role
        role = await guild.create_role(
            name=role_name,
            color=discord.Color.blue(),
            mentionable=True
        )

        print(f"✅ Created Coach role")
        return role

    async def assign_coach_role(self, guild: discord.Guild, member: discord.Member):
        """
        Assign Coach role to a member.

        Args:
            guild: Discord server
            member: Discord member to assign role to
        """
        role = await self.create_coach_role(guild)
        await member.add_roles(role)
        print(f"✅ Assigned Coach role to {member.name}")

    async def remove_coach_role(self, guild: discord.Guild, member: discord.Member) -> bool:
        """
        Remove Coach role from a specific member.

        Args:
            guild: Discord server
            member: Discord member to remove role from

        Returns:
            True if role was removed, False if not found
        """
        role = discord.utils.get(guild.roles, name="Coach")

        if role and role in member.roles:
            await member.remove_roles(role)
            print(f"✅ Removed Coach role from {member.name}")
            return True

        print(f"⚠️ Member {member.name} doesn't have Coach role")
        return False

    async def remove_all_coach_roles(self, guild: discord.Guild):
        """
        Remove Coach role from all members and delete the role (for reset).

        Args:
            guild: Discord server
        """
        role = discord.utils.get(guild.roles, name="Coach")

        if not role:
            print("⚠️ Coach role not found")
            return

        # Remove from all members
        for member in role.members:
            await member.remove_roles(role)
            print(f"✅ Removed Coach role from {member.name}")

        # Delete role
        await role.delete()
        print(f"✅ Deleted Coach role")


# Example usage and testing
if __name__ == "__main__":
    print("Discord Service - Example Usage")
    print("=" * 50)

    print("\nThis service handles:")
    print("1. Creating category: ⌜🎮⌟ ᴅʀᴀꜰᴛ ʟᴇᴀɢᴜᴇ ᴄᴏᴀᴄʜᴇꜱ ⌜🎮⌟")
    print("2. Creating coach channels: 🏆┃ᴛᴇᴀᴍ-ɴᴀᴍᴇ")
    print("3. Setting channel permissions (coach + admins only)")
    print("4. Sending welcome embeds with roster and Tera Captains")
    print("5. Managing Coach role (create, assign, remove)")
    print("6. Cleaning up channels and roles for resets")
