"""
Google Sheets service for Pokemon Draft League Bot.

Handles all interactions with Google Sheets API including reading/writing
league data, draft history, team rosters, and match results.

Optimizations:
- Worksheet caching to reduce API calls
- Pokemon data caching (5-minute TTL)
- Config caching (10-minute TTL)
- Batch operations for multiple updates
"""

import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Optional
from datetime import datetime
import time


class SheetsService:
    """Handles all Google Sheets operations for the draft league"""

    # Google Sheets API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self, credentials_path: str, spreadsheet_id: str):
        """
        Initialize Google Sheets service.

        Args:
            credentials_path: Path to Google service account credentials JSON
            spreadsheet_id: ID of the Google Spreadsheet to use
        """
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.client = None
        self.spreadsheet = None

        # Caching for performance
        self._worksheet_cache: Dict = {}
        self._pokemon_cache: Optional[Dict] = None
        self._pokemon_cache_time: float = 0
        self._pokemon_cache_ttl: int = 300  # 5 minutes

        self._config_cache: Dict = {}
        self._config_cache_time: float = 0
        self._config_cache_ttl: int = 600  # 10 minutes

        self._connect()

    def _connect(self):
        """Establish connection to Google Sheets API"""
        try:
            # Load credentials
            creds = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )

            # Initialize gspread client
            self.client = gspread.authorize(creds)

            # Open spreadsheet
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)

            print(f"✅ Connected to Google Sheets: {self.spreadsheet.title}")

        except FileNotFoundError:
            print(f"❌ Error: Credentials file not found at {self.credentials_path}")
            raise
        except Exception as e:
            print(f"❌ Error connecting to Google Sheets: {e}")
            raise

    def _get_worksheet(self, name: str):
        """
        Get worksheet by name with caching.

        Args:
            name: Name of the worksheet

        Returns:
            Worksheet object
        """
        if name not in self._worksheet_cache:
            try:
                self._worksheet_cache[name] = self.spreadsheet.worksheet(name)
            except gspread.WorksheetNotFound:
                print(f"⚠️ Warning: Worksheet '{name}' not found. Creating it...")
                # Create worksheet if it doesn't exist
                self._worksheet_cache[name] = self.spreadsheet.add_worksheet(
                    title=name,
                    rows=1000,
                    cols=20
                )

        return self._worksheet_cache[name]

    # ==================== CONFIG OPERATIONS ====================

    def get_config_value(self, key: str, default=None):
        """
        Get a configuration value from Config sheet with caching.

        Args:
            key: Configuration key to look up
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        try:
            # Check cache validity
            current_time = time.time()
            cache_age = current_time - self._config_cache_time

            # Refresh cache if expired
            if cache_age > self._config_cache_ttl or not self._config_cache:
                sheet = self._get_worksheet('Config')
                records = sheet.get_all_records()
                self._config_cache = {record.get('Key'): record.get('Value') for record in records if 'Key' in record}
                self._config_cache_time = current_time
                print(f'📋 Config cache refreshed ({len(self._config_cache)} entries)')

            return self._config_cache.get(key, default)

        except Exception as e:
            print(f"⚠️ Error getting config value '{key}': {e}")
            return default

    def clear_config_cache(self):
        """Clear config cache to force refresh"""
        self._config_cache = {}
        self._config_cache_time = 0

    # ==================== POKEMON OPERATIONS ====================

    def get_all_pokemon(self, force_refresh: bool = False) -> List[Dict]:
        """
        Get all available Pokémon from the Pokemon sheet with caching.

        Args:
            force_refresh: Force cache refresh if True

        Returns:
            List of Pokémon dictionaries with all data
        """
        try:
            # Check cache validity
            current_time = time.time()
            cache_age = current_time - self._pokemon_cache_time

            # Use cache if valid
            if not force_refresh and self._pokemon_cache is not None and cache_age < self._pokemon_cache_ttl:
                return list(self._pokemon_cache.values())

            # Refresh cache
            sheet = self._get_worksheet('Pokemon')
            records = sheet.get_all_records()

            # Build cache as dictionary for O(1) lookups
            self._pokemon_cache = {
                record.get('Name', '').lower(): record
                for record in records if 'Name' in record
            }
            self._pokemon_cache_time = current_time

            print(f'📋 Pokemon cache refreshed ({len(self._pokemon_cache)} entries)')

            return records

        except Exception as e:
            print(f'❌ Error getting all Pokémon: {e}')
            # Return cached data even if expired on error
            if self._pokemon_cache:
                print('⚠️ Using stale cache due to error')
                return list(self._pokemon_cache.values())
            return []

    def clear_pokemon_cache(self):
        """Clear Pokemon cache to force refresh"""
        self._pokemon_cache = None
        self._pokemon_cache_time = 0

    def get_pokemon_data(self, pokemon_name: str) -> Dict:
        """
        Get full data for a specific Pokémon with caching.

        Args:
            pokemon_name: Name of the Pokémon

        Returns:
            Dictionary with Pokémon data

        Raises:
            ValueError: If Pokémon not found
        """
        try:
            # Ensure cache is populated
            self.get_all_pokemon()

            # O(1) lookup from cache
            pokemon_lower = pokemon_name.lower()
            if pokemon_lower in self._pokemon_cache:
                record = self._pokemon_cache[pokemon_lower]
                return {
                    'name': record['Name'],
                    'tier': record.get('Tier', ''),
                    'type1': record.get('Type1', ''),
                    'type2': record.get('Type2', ''),
                    'point_cost': int(record.get('Point_Cost', 0)),
                    'hp': record.get('HP', ''),
                    'attack': record.get('Attack', ''),
                    'defense': record.get('Defense', ''),
                    'sp_attack': record.get('SpAttack', ''),
                    'sp_defense': record.get('SpDefense', ''),
                        "speed": record.get("Speed", "")
                    }

            raise ValueError(f"Pokémon not found: {pokemon_name}")

        except Exception as e:
            print(f"❌ Error getting Pokémon data for '{pokemon_name}': {e}")
            raise

    def get_pokemon_cost(self, pokemon_name: str) -> int:
        """
        Get point cost for a specific Pokémon.

        Args:
            pokemon_name: Name of the Pokémon

        Returns:
            Point cost as integer
        """
        data = self.get_pokemon_data(pokemon_name)
        return data["point_cost"]

    # ==================== TEAM OPERATIONS ====================

    def get_team_by_player(self, player_name: str) -> Dict:
        """
        Get team data for a specific player.

        Args:
            player_name: Discord username of the player

        Returns:
            Dictionary with team data including roster

        Raises:
            ValueError: If team not found
        """
        try:
            sheet = self._get_worksheet("Teams")
            records = sheet.get_all_records()

            for record in records:
                if record["Player"] == player_name:
                    # Parse Pokemon_List (comma-separated) into roster
                    pokemon_list = record.get("Pokemon_List", "")
                    pokemon_names = [p.strip() for p in pokemon_list.split(",") if p.strip()]

                    roster = []
                    for name in pokemon_names:
                        try:
                            poke_data = self.get_pokemon_data(name)
                            roster.append(poke_data)
                        except ValueError:
                            print(f"⚠️ Warning: Pokémon '{name}' not found in Pokemon sheet")

                    return {
                        "player": record["Player"],
                        "team_name": record["Team_Name"],
                        "team_logo": record.get("Team_Logo", ""),
                        "roster": roster,
                        "total_points_used": int(record.get("Total_Points_Used", 0))
                    }

            raise ValueError(f"No team data found for player: {player_name}")

        except Exception as e:
            print(f"❌ Error getting team for '{player_name}': {e}")
            raise

    def get_all_teams(self) -> Dict[str, Dict]:
        """
        Get all teams in the league.

        Returns:
            Dictionary mapping player names to team data
        """
        try:
            sheet = self._get_worksheet("Teams")
            records = sheet.get_all_records()

            teams = {}
            for record in records:
                player_name = record["Player"]
                if player_name:  # Skip empty rows
                    try:
                        teams[player_name] = self.get_team_by_player(player_name)
                    except ValueError:
                        continue

            return teams

        except Exception as e:
            print(f"❌ Error getting all teams: {e}")
            return {}

    def update_team_roster(self, player: str, pokemon_list: List[str], total_points: int):
        """
        Update a player's roster in the Teams sheet.

        Args:
            player: Player name
            pokemon_list: List of Pokémon names
            total_points: Total points used
        """
        try:
            sheet = self._get_worksheet("Teams")
            cell = sheet.find(player)

            if cell:
                # Update existing row
                row = cell.row
                sheet.update_cell(row, 4, ", ".join(pokemon_list))  # Pokemon_List column
                sheet.update_cell(row, 5, total_points)  # Total_Points_Used column
            else:
                # Add new row
                sheet.append_row([
                    player,
                    f"{player}'s Team",  # Default team name
                    "",  # Empty logo
                    ", ".join(pokemon_list),
                    total_points
                ])

            print(f"✅ Updated roster for {player}")

        except Exception as e:
            print(f"❌ Error updating team roster for '{player}': {e}")
            raise

    # ==================== TERA CAPTAIN OPERATIONS ====================

    def get_tera_captains(self, player: str) -> List[Dict]:
        """
        Get all Tera Captains for a player.

        Args:
            player: Player name

        Returns:
            List of Tera Captain dictionaries
        """
        try:
            sheet = self._get_worksheet("Tera_Captains")
            records = sheet.get_all_records()

            captains = []
            for record in records:
                if record["Player"] == player:
                    captains.append({
                        "pokemon": record["Pokemon"],
                        "tera_type": record["Tera_Type"],
                        "point_cost": int(record.get("Point_Cost", 0))
                    })

            return captains

        except Exception as e:
            print(f"❌ Error getting Tera Captains for '{player}': {e}")
            return []

    def add_tera_captain(self, player: str, pokemon: str, tera_type: str, point_cost: int):
        """Add a Tera Captain to the sheet"""
        try:
            sheet = self._get_worksheet("Tera_Captains")
            sheet.append_row([player, pokemon, tera_type, point_cost])
            print(f"✅ Added Tera Captain: {player} - {pokemon} ({tera_type})")
        except Exception as e:
            print(f"❌ Error adding Tera Captain: {e}")
            raise

    def update_tera_type(self, player: str, pokemon: str, new_type: str):
        """Update a Tera Captain's type"""
        try:
            sheet = self._get_worksheet("Tera_Captains")
            cell = sheet.find(pokemon)

            if cell:
                sheet.update_cell(cell.row, 3, new_type)  # Column 3 is Tera_Type
                print(f"✅ Updated Tera type for {pokemon} to {new_type}")
            else:
                raise ValueError(f"Tera Captain not found: {pokemon}")

        except Exception as e:
            print(f"❌ Error updating Tera type: {e}")
            raise

    def delete_tera_captain(self, player: str, pokemon: str):
        """Remove a Tera Captain"""
        try:
            sheet = self._get_worksheet("Tera_Captains")
            cell = sheet.find(pokemon)

            if cell:
                sheet.delete_rows(cell.row)
                print(f"✅ Removed Tera Captain: {pokemon}")
            else:
                raise ValueError(f"Tera Captain not found: {pokemon}")

        except Exception as e:
            print(f"❌ Error deleting Tera Captain: {e}")
            raise

    def clear_tera_captains(self, player_name: str):
        """Remove all Tera Captain entries for a player"""
        try:
            sheet = self._get_worksheet("Tera_Captains")
            records = sheet.get_all_records()

            # Find all rows for this player (in reverse to avoid index issues)
            rows_to_delete = []
            for i, record in enumerate(records, start=2):  # Start at 2 (skip header)
                if record["Player"] == player_name:
                    rows_to_delete.append(i)

            # Delete rows in reverse order
            for row in reversed(rows_to_delete):
                sheet.delete_rows(row)

            print(f"✅ Cleared all Tera Captains for {player_name}")

        except Exception as e:
            print(f"❌ Error clearing Tera Captains: {e}")
            raise

    # ==================== DRAFT OPERATIONS ====================

    def record_draft_pick(self, pick_num: int, player: str, pokemon: str, point_cost: int):
        """
        Record a draft pick in Draft_History sheet.

        Args:
            pick_num: Pick number in the draft
            player: Player making the pick
            pokemon: Pokémon being drafted
            point_cost: Cost in points
        """
        try:
            sheet = self._get_worksheet("Draft_History")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sheet.append_row([pick_num, player, pokemon, point_cost, timestamp])
            print(f"✅ Recorded draft pick: {player} picked {pokemon} ({point_cost} pts)")

        except Exception as e:
            print(f"❌ Error recording draft pick: {e}")
            raise

    def get_draft_history(self) -> List[Dict]:
        """Get all draft picks"""
        try:
            sheet = self._get_worksheet("Draft_History")
            records = sheet.get_all_records()
            return records
        except Exception as e:
            print(f"❌ Error getting draft history: {e}")
            return []

    # ==================== COACH MANAGEMENT ====================

    def archive_team(self, player_name: str, team_data: Dict):
        """Archive team data to Archived_Teams sheet"""
        try:
            # Get or create Archived_Teams sheet
            try:
                sheet = self._get_worksheet("Archived_Teams")
            except:
                sheet = self.spreadsheet.add_worksheet(
                    title="Archived_Teams",
                    rows=1000,
                    cols=10
                )
                # Add headers
                sheet.append_row([
                    "Archived_Date", "Player", "Team_Name", "Team_Logo",
                    "Pokemon_List", "Total_Points_Used"
                ])

            # Archive the data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pokemon_names = ", ".join([p["name"] for p in team_data["roster"]])

            sheet.append_row([
                timestamp,
                player_name,
                team_data["team_name"],
                team_data.get("team_logo", ""),
                pokemon_names,
                team_data.get("total_points_used", 0)
            ])

            print(f"✅ Archived team data for {player_name}")

        except Exception as e:
            print(f"❌ Error archiving team: {e}")
            raise

    def mark_team_inactive(self, player_name: str):
        """Mark a team as inactive in Standings (preserves stats)"""
        try:
            sheet = self._get_worksheet("Standings")
            cell = sheet.find(player_name)

            if cell:
                current_name = sheet.cell(cell.row, cell.col).value
                if "(Inactive)" not in current_name:
                    sheet.update_cell(cell.row, cell.col, f"{current_name} (Inactive)")
                    print(f"✅ Marked {player_name} as inactive in standings")

        except Exception as e:
            print(f"❌ Error marking team inactive: {e}")
            raise

    # ==================== HELPER METHODS ====================

    def _append_row(self, sheet_name: str, row_data: List):
        """Append a row to a worksheet"""
        sheet = self._get_worksheet(sheet_name)
        sheet.append_row(row_data)

    def _update_cell(self, sheet_name: str, row: int, col: int, value):
        """Update a specific cell"""
        sheet = self._get_worksheet(sheet_name)
        sheet.update_cell(row, col, value)


# Example usage and testing
if __name__ == "__main__":
    print("Google Sheets Service - Example Usage")
    print("=" * 50)

    # This would normally use actual credentials
    print("\nTo use this service:")
    print("1. Set up Google Cloud project")
    print("2. Enable Google Sheets API")
    print("3. Create service account and download credentials")
    print("4. Share your spreadsheet with the service account email")
    print("5. Initialize: service = SheetsService('.credentials.json', 'SHEET_ID')")
