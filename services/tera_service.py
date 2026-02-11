"""
Tera Captain service for Pokemon Draft League Bot.

Handles Tera Captain designation, validation, and management.
"""

from typing import List, Dict
from services.sheets_service import SheetsService
from utils.constants import (
    VALID_TERA_TYPES,
    TYPE_EMOJI,
    DEFAULT_MAX_TERA_CAPTAINS,
    DEFAULT_MAX_TERA_CAPTAIN_COST,
    DEFAULT_MAX_TERA_TOTAL_POINTS
)


class TeraService:
    """Handles Tera Captain operations with validation"""

    def __init__(self, sheets_service: SheetsService):
        """
        Initialize Tera service.

        Args:
            sheets_service: Google Sheets service instance
        """
        self.sheets = sheets_service

    # ==================== TERA CAPTAIN MANAGEMENT ====================

    def set_tera_captain(self, player: str, pokemon: str, tera_type: str) -> Dict:
        """
        Designate a Pokémon as a Tera Captain with chosen type.

        Args:
            player: Player name
            pokemon: Pokemon name
            tera_type: Desired Tera type

        Returns:
            Success dictionary with captain data

        Raises:
            ValueError: If validation fails
        """
        # Validate pokemon is on player's roster
        team_data = self.sheets.get_team_by_player(player)
        roster = team_data.get("roster", [])

        pokemon_data = None
        for poke in roster:
            if poke["name"].lower() == pokemon.lower():
                pokemon_data = poke
                break

        if not pokemon_data:
            raise ValueError(
                f"❌ {pokemon} is not on your roster! "
                f"You can only designate Pokémon you've drafted."
            )

        # Get Pokemon point cost
        point_cost = pokemon_data["point_cost"]

        # CRITICAL: Validate point cost is ≤ 13
        if point_cost > DEFAULT_MAX_TERA_CAPTAIN_COST:
            raise ValueError(
                f"❌ {pokemon} costs {point_cost} points. "
                f"Only Pokémon with {DEFAULT_MAX_TERA_CAPTAIN_COST} points or less can be Tera Captains."
            )

        # Validate tera_type is valid (19 types including Stellar)
        if tera_type.title() not in VALID_TERA_TYPES:
            valid_types_str = ", ".join(VALID_TERA_TYPES)
            raise ValueError(
                f"❌ Invalid Tera type: {tera_type}\n"
                f"Valid types: {valid_types_str}\n"
                f"Use `!tera types` to see all valid types."
            )

        # Check if Pokemon is already a Tera Captain
        current_captains = self.sheets.get_tera_captains(player)
        for captain in current_captains:
            if captain["pokemon"].lower() == pokemon.lower():
                raise ValueError(
                    f"❌ {pokemon} is already a Tera Captain! "
                    f"Use `!tera change {pokemon} <new_type>` to change its Tera type."
                )

        # Check exactly 3 Tera Captains limit
        if len(current_captains) >= DEFAULT_MAX_TERA_CAPTAINS:
            captain_names = ", ".join([c["pokemon"] for c in current_captains])
            raise ValueError(
                f"❌ Maximum Tera Captains limit reached! "
                f"You already have {len(current_captains)}/{DEFAULT_MAX_TERA_CAPTAINS} Tera Captains:\n"
                f"{captain_names}\n\n"
                f"Use `!tera remove <pokemon>` to free up a slot."
            )

        # Validate total points ≤ 25
        current_total = sum(c["point_cost"] for c in current_captains)
        new_total = current_total + point_cost

        if new_total > DEFAULT_MAX_TERA_TOTAL_POINTS:
            raise ValueError(
                f"❌ Total Tera Captain points would be {new_total}. "
                f"Maximum allowed is {DEFAULT_MAX_TERA_TOTAL_POINTS} points.\n"
                f"Current total: {current_total} points."
            )

        # Record in Tera_Captains sheet (includes point_cost)
        self.sheets.add_tera_captain(player, pokemon, tera_type.title(), point_cost)

        return {
            "success": True,
            "player": player,
            "pokemon": pokemon,
            "tera_type": tera_type.title(),
            "point_cost": point_cost,
            "total_captains": len(current_captains) + 1,
            "total_points": new_total
        }

    def change_tera_type(self, player: str, pokemon: str, new_type: str) -> Dict:
        """
        Change a Tera Captain's Tera Type.

        Args:
            player: Player name
            pokemon: Pokemon name
            new_type: New Tera type

        Returns:
            Success dictionary

        Raises:
            ValueError: If validation fails
        """
        # Validate pokemon is a Tera Captain
        captains = self.sheets.get_tera_captains(player)

        captain_data = None
        for captain in captains:
            if captain["pokemon"].lower() == pokemon.lower():
                captain_data = captain
                break

        if not captain_data:
            captain_names = ", ".join([c["pokemon"] for c in captains]) if captains else "None"
            raise ValueError(
                f"❌ {pokemon} is not a Tera Captain!\n"
                f"Your current Tera Captains: {captain_names}"
            )

        # Validate new type
        if new_type.title() not in VALID_TERA_TYPES:
            valid_types_str = ", ".join(VALID_TERA_TYPES)
            raise ValueError(
                f"❌ Invalid Tera type: {new_type}\n"
                f"Valid types: {valid_types_str}\n"
                f"Use `!tera types` to see all valid types."
            )

        # Update in Sheets
        old_type = captain_data["tera_type"]
        self.sheets.update_tera_type(player, pokemon, new_type.title())

        return {
            "success": True,
            "player": player,
            "pokemon": pokemon,
            "old_type": old_type,
            "new_type": new_type.title()
        }

    def remove_tera_captain(self, player: str, pokemon: str) -> Dict:
        """
        Remove Tera Captain designation.

        Args:
            player: Player name
            pokemon: Pokemon name

        Returns:
            Success dictionary

        Raises:
            ValueError: If validation fails
        """
        # Validate pokemon is a Tera Captain
        captains = self.sheets.get_tera_captains(player)

        captain_data = None
        for captain in captains:
            if captain["pokemon"].lower() == pokemon.lower():
                captain_data = captain
                break

        if not captain_data:
            captain_names = ", ".join([c["pokemon"] for c in captains]) if captains else "None"
            raise ValueError(
                f"❌ {pokemon} is not a Tera Captain!\n"
                f"Your current Tera Captains: {captain_names}"
            )

        # Remove from Sheets
        self.sheets.delete_tera_captain(player, pokemon)

        remaining_total = sum(c["point_cost"] for c in captains if c["pokemon"] != pokemon)

        return {
            "success": True,
            "player": player,
            "pokemon": pokemon,
            "tera_type": captain_data["tera_type"],
            "point_cost": captain_data["point_cost"],
            "remaining_captains": len(captains) - 1,
            "remaining_points": remaining_total
        }

    # ==================== VIEWING TERA CAPTAINS ====================

    def get_player_tera_captains(self, player: str) -> List[Dict]:
        """
        Get all Tera Captains for a player with enriched data.

        Args:
            player: Player name

        Returns:
            List of Tera Captain dictionaries with type emojis
        """
        captains = self.sheets.get_tera_captains(player)

        # Enrich with emojis and format data
        enriched = []
        for captain in captains:
            tera_type = captain["tera_type"]
            emoji = TYPE_EMOJI.get(tera_type, "⭐")

            # Get original types from Pokemon data
            try:
                pokemon_data = self.sheets.get_pokemon_data(captain["pokemon"])
                type1 = pokemon_data.get("type1", "")
                type2 = pokemon_data.get("type2", "")
                original_types = type1 + (f"/{type2}" if type2 else "")
            except:
                original_types = "Unknown"

            enriched.append({
                "pokemon": captain["pokemon"],
                "tera_type": tera_type,
                "emoji": emoji,
                "point_cost": captain["point_cost"],
                "original_types": original_types
            })

        return enriched

    def get_all_tera_captains(self) -> Dict[str, List[Dict]]:
        """
        Get all Tera Captains grouped by player.

        Returns:
            Dictionary mapping player names to their Tera Captains
        """
        # Get all teams
        teams = self.sheets.get_all_teams()

        result = {}
        for player in teams.keys():
            captains = self.get_player_tera_captains(player)
            if captains:  # Only include players who have Tera Captains
                result[player] = captains

        return result

    # ==================== VALIDATION HELPERS ====================

    def validate_tera_captain_requirements(self, player: str) -> Dict:
        """
        Check if player has met Tera Captain requirements (exactly 3).

        Args:
            player: Player name

        Returns:
            Validation status dictionary
        """
        captains = self.sheets.get_tera_captains(player)
        count = len(captains)
        total_points = sum(c["point_cost"] for c in captains)

        is_valid = count == DEFAULT_MAX_TERA_CAPTAINS
        is_complete = count == DEFAULT_MAX_TERA_CAPTAINS

        return {
            "is_valid": is_valid,
            "is_complete": is_complete,
            "count": count,
            "required": DEFAULT_MAX_TERA_CAPTAINS,
            "total_points": total_points,
            "max_points": DEFAULT_MAX_TERA_TOTAL_POINTS,
            "captains": [c["pokemon"] for c in captains]
        }

    # ==================== UTILITY FUNCTIONS ====================

    def get_valid_types_display(self) -> str:
        """
        Format all valid Tera types for display.

        Returns:
            Formatted string with all types and emojis
        """
        lines = []
        types_per_line = 4

        for i in range(0, len(VALID_TERA_TYPES), types_per_line):
            chunk = VALID_TERA_TYPES[i:i + types_per_line]
            line = "  ".join([
                f"{TYPE_EMOJI.get(t, '⭐')} {t}"
                for t in chunk
            ])
            lines.append(line)

        return "\n".join(lines)


# Example usage and testing
if __name__ == "__main__":
    print("Tera Captain Service - Example Usage")
    print("=" * 50)

    print("\nThis service handles:")
    print("1. Tera Captain designation with point validation")
    print("2. Exactly 3 Tera Captains per team")
    print("3. Only Pokémon ≤13 points can be Tera Captains")
    print("4. Total Tera Captain points ≤25")
    print("5. 19 valid Tera types (18 standard + Stellar)")
    print("6. Tera type changes")
    print("7. Tera Captain removal")
