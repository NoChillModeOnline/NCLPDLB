"""
Spreadsheet Error Diagnostics and Repair Service

Automatically detects and repairs common data integrity issues in the
Google Sheets league database.
"""

from typing import List, Dict, Tuple
from datetime import datetime
import re


class ErrorDiagnostics:
    """Detects and repairs data integrity issues in Google Sheets"""

    def __init__(self, sheets_service):
        """
        Initialize error diagnostics service.

        Args:
            sheets_service: Instance of SheetsService
        """
        self.sheets = sheets_service
        self.errors_found = []

    def run_full_diagnostic(self) -> Dict:
        """
        Run complete diagnostic check on all sheets.

        Returns:
            Dictionary with error summary and details
        """
        print("\n🔍 Running Spreadsheet Error Diagnostics...")
        print("=" * 60)

        self.errors_found = []

        # Run all diagnostic checks
        self._check_pokemon_data()
        self._check_team_data()
        self._check_tera_captains()
        self._check_draft_history()
        self._check_point_totals()
        self._check_duplicate_pokemon()
        self._check_missing_references()
        self._check_invalid_types()
        self._check_standings_consistency()

        # Log errors to Error_Diagnostics sheet
        self._log_errors()

        # Generate summary
        summary = self._generate_summary()

        print("\n" + "=" * 60)
        print(f"✅ Diagnostic complete: {len(self.errors_found)} issues found")

        return summary

    # ==================== DIAGNOSTIC CHECKS ====================

    def _check_pokemon_data(self):
        """Check for issues in Pokemon sheet"""
        try:
            pokemon = self.sheets.get_all_pokemon()

            for poke in pokemon:
                name = poke.get("Name", "")

                # Error 1: Missing required fields
                if not name:
                    self._add_error(
                        error_type="MISSING_POKEMON_NAME",
                        severity="CRITICAL",
                        description=f"Pokemon entry missing name",
                        affected_data=f"Row with data: {poke}",
                        auto_fix=False
                    )

                # Error 2: Invalid point cost
                point_cost = poke.get("Point_Cost")
                if point_cost is None or point_cost == "" or not str(point_cost).isdigit():
                    self._add_error(
                        error_type="INVALID_POINT_COST",
                        severity="HIGH",
                        description=f"Pokemon '{name}' has invalid point cost: {point_cost}",
                        affected_data=f"Pokemon: {name}, Cost: {point_cost}",
                        auto_fix=False
                    )
                elif int(point_cost) < 0 or int(point_cost) > 120:
                    self._add_error(
                        error_type="UNREALISTIC_POINT_COST",
                        severity="MEDIUM",
                        description=f"Pokemon '{name}' has unrealistic point cost: {point_cost}",
                        affected_data=f"Pokemon: {name}, Cost: {point_cost}",
                        auto_fix=False
                    )

                # Error 3: Invalid types
                type1 = poke.get("Type1", "")
                type2 = poke.get("Type2", "")

                valid_types = [
                    "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
                    "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
                    "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"
                ]

                if type1 and type1 not in valid_types:
                    self._add_error(
                        error_type="INVALID_POKEMON_TYPE",
                        severity="HIGH",
                        description=f"Pokemon '{name}' has invalid Type1: {type1}",
                        affected_data=f"Pokemon: {name}, Type1: {type1}",
                        auto_fix=False
                    )

                if type2 and type2 not in valid_types:
                    self._add_error(
                        error_type="INVALID_POKEMON_TYPE",
                        severity="HIGH",
                        description=f"Pokemon '{name}' has invalid Type2: {type2}",
                        affected_data=f"Pokemon: {name}, Type2: {type2}",
                        auto_fix=False
                    )

        except Exception as e:
            self._add_error(
                error_type="SHEET_ACCESS_ERROR",
                severity="CRITICAL",
                description=f"Could not access Pokemon sheet: {e}",
                affected_data="Pokemon sheet",
                auto_fix=False
            )

    def _check_team_data(self):
        """Check for issues in Teams sheet"""
        try:
            teams = self.sheets.get_all_teams()

            for player, team_data in teams.items():
                # Error 4: Missing team name
                if not team_data.get("team_name"):
                    self._add_error(
                        error_type="MISSING_TEAM_NAME",
                        severity="MEDIUM",
                        description=f"Player '{player}' has no team name",
                        affected_data=f"Player: {player}",
                        auto_fix=True,
                        fix_action=f"Set default: '{player}'s Team'"
                    )

                # Error 5: Empty roster
                roster = team_data.get("roster", [])
                if not roster:
                    self._add_error(
                        error_type="EMPTY_ROSTER",
                        severity="HIGH",
                        description=f"Player '{player}' has empty roster",
                        affected_data=f"Player: {player}",
                        auto_fix=False
                    )

                # Error 6: Too many/few Pokemon
                pokemon_count = len(roster)
                if pokemon_count < 10 and pokemon_count > 0:
                    self._add_error(
                        error_type="ROSTER_TOO_SMALL",
                        severity="HIGH",
                        description=f"Player '{player}' has only {pokemon_count} Pokemon (min: 10)",
                        affected_data=f"Player: {player}, Count: {pokemon_count}",
                        auto_fix=False
                    )
                elif pokemon_count > 12:
                    self._add_error(
                        error_type="ROSTER_TOO_LARGE",
                        severity="HIGH",
                        description=f"Player '{player}' has {pokemon_count} Pokemon (max: 12)",
                        affected_data=f"Player: {player}, Count: {pokemon_count}",
                        auto_fix=False
                    )

                # Error 7: Invalid team logo URL
                logo = team_data.get("team_logo", "")
                if logo and not self._is_valid_url(logo):
                    self._add_error(
                        error_type="INVALID_LOGO_URL",
                        severity="LOW",
                        description=f"Player '{player}' has invalid logo URL",
                        affected_data=f"Player: {player}, URL: {logo}",
                        auto_fix=True,
                        fix_action="Clear invalid URL"
                    )

        except Exception as e:
            self._add_error(
                error_type="SHEET_ACCESS_ERROR",
                severity="CRITICAL",
                description=f"Could not access Teams sheet: {e}",
                affected_data="Teams sheet",
                auto_fix=False
            )

    def _check_tera_captains(self):
        """Check for Tera Captain issues"""
        try:
            teams = self.sheets.get_all_teams()

            for player in teams.keys():
                tera_captains = self.sheets.get_tera_captains(player)
                team_data = teams[player]
                roster = team_data.get("roster", [])
                roster_names = [p["name"] for p in roster]

                # Error 8: Too many Tera Captains
                if len(tera_captains) > 3:
                    self._add_error(
                        error_type="TOO_MANY_TERA_CAPTAINS",
                        severity="CRITICAL",
                        description=f"Player '{player}' has {len(tera_captains)} Tera Captains (max: 3)",
                        affected_data=f"Player: {player}, Count: {len(tera_captains)}",
                        auto_fix=False
                    )

                # Error 9: Tera Captain not on roster
                for tc in tera_captains:
                    pokemon_name = tc.get("pokemon")
                    if pokemon_name not in roster_names:
                        self._add_error(
                            error_type="TERA_CAPTAIN_NOT_ON_ROSTER",
                            severity="CRITICAL",
                            description=f"Player '{player}' has Tera Captain '{pokemon_name}' not on their roster",
                            affected_data=f"Player: {player}, Pokemon: {pokemon_name}",
                            auto_fix=True,
                            fix_action=f"Remove invalid Tera Captain"
                        )

                    # Error 10: Tera Captain too expensive
                    point_cost = tc.get("point_cost", 0)
                    if point_cost > 13:
                        self._add_error(
                            error_type="TERA_CAPTAIN_TOO_EXPENSIVE",
                            severity="CRITICAL",
                            description=f"Player '{player}' has Tera Captain '{pokemon_name}' costing {point_cost} pts (max: 13)",
                            affected_data=f"Player: {player}, Pokemon: {pokemon_name}, Cost: {point_cost}",
                            auto_fix=True,
                            fix_action="Remove invalid Tera Captain"
                        )

                # Error 11: Total Tera Captain points exceed 25
                total_points = sum(tc.get("point_cost", 0) for tc in tera_captains)
                if total_points > 25:
                    self._add_error(
                        error_type="TERA_CAPTAIN_POINTS_EXCEEDED",
                        severity="CRITICAL",
                        description=f"Player '{player}' Tera Captains total {total_points} pts (max: 25)",
                        affected_data=f"Player: {player}, Total: {total_points}",
                        auto_fix=False
                    )

                # Error 12: Invalid Tera type
                valid_tera_types = [
                    "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
                    "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
                    "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy", "Stellar"
                ]

                for tc in tera_captains:
                    tera_type = tc.get("tera_type")
                    if tera_type not in valid_tera_types:
                        self._add_error(
                            error_type="INVALID_TERA_TYPE",
                            severity="HIGH",
                            description=f"Player '{player}' has invalid Tera type '{tera_type}' for {tc.get('pokemon')}",
                            affected_data=f"Player: {player}, Pokemon: {tc.get('pokemon')}, Type: {tera_type}",
                            auto_fix=False
                        )

        except Exception as e:
            self._add_error(
                error_type="SHEET_ACCESS_ERROR",
                severity="CRITICAL",
                description=f"Could not access Tera_Captains sheet: {e}",
                affected_data="Tera_Captains sheet",
                auto_fix=False
            )

    def _check_draft_history(self):
        """Check for draft history issues"""
        try:
            draft_history = self.sheets.get_draft_history()
            teams = self.sheets.get_all_teams()

            # Error 13: Duplicate draft picks
            picked_pokemon = []
            for pick in draft_history:
                pokemon = pick.get("Pokemon")
                if pokemon in picked_pokemon:
                    self._add_error(
                        error_type="DUPLICATE_DRAFT_PICK",
                        severity="CRITICAL",
                        description=f"Pokemon '{pokemon}' was drafted multiple times",
                        affected_data=f"Pokemon: {pokemon}",
                        auto_fix=False
                    )
                picked_pokemon.append(pokemon)

            # Error 14: Draft pick doesn't match roster
            for player, team_data in teams.items():
                roster_names = [p["name"] for p in team_data.get("roster", [])]
                player_picks = [p.get("Pokemon") for p in draft_history if p.get("Player") == player]

                for pick in player_picks:
                    if pick not in roster_names:
                        self._add_error(
                            error_type="DRAFT_ROSTER_MISMATCH",
                            severity="HIGH",
                            description=f"Player '{player}' drafted '{pick}' but it's not on their roster",
                            affected_data=f"Player: {player}, Pokemon: {pick}",
                            auto_fix=False
                        )

        except Exception as e:
            self._add_error(
                error_type="SHEET_ACCESS_ERROR",
                severity="MEDIUM",
                description=f"Could not access Draft_History sheet: {e}",
                affected_data="Draft_History sheet",
                auto_fix=False
            )

    def _check_point_totals(self):
        """Check if point totals are correct"""
        try:
            teams = self.sheets.get_all_teams()

            for player, team_data in teams.items():
                roster = team_data.get("roster", [])
                recorded_total = team_data.get("total_points_used", 0)

                # Calculate actual total
                actual_total = sum(p.get("point_cost", 0) for p in roster)

                # Error 15: Point total mismatch
                if recorded_total != actual_total:
                    self._add_error(
                        error_type="POINT_TOTAL_MISMATCH",
                        severity="HIGH",
                        description=f"Player '{player}' recorded points ({recorded_total}) don't match actual ({actual_total})",
                        affected_data=f"Player: {player}, Recorded: {recorded_total}, Actual: {actual_total}",
                        auto_fix=True,
                        fix_action=f"Update to {actual_total} points"
                    )

                # Error 16: Points exceed budget
                if actual_total > 120:
                    self._add_error(
                        error_type="POINTS_EXCEED_BUDGET",
                        severity="CRITICAL",
                        description=f"Player '{player}' has {actual_total} points (max: 120)",
                        affected_data=f"Player: {player}, Total: {actual_total}",
                        auto_fix=False
                    )

        except Exception as e:
            self._add_error(
                error_type="CALCULATION_ERROR",
                severity="MEDIUM",
                description=f"Could not calculate point totals: {e}",
                affected_data="Teams sheet",
                auto_fix=False
            )

    def _check_duplicate_pokemon(self):
        """Check for duplicate Pokemon across teams"""
        try:
            teams = self.sheets.get_all_teams()
            pokemon_owners = {}

            for player, team_data in teams.items():
                roster = team_data.get("roster", [])

                for pokemon in roster:
                    name = pokemon.get("name")
                    if name in pokemon_owners:
                        # Error 17: Pokemon on multiple teams
                        self._add_error(
                            error_type="DUPLICATE_POKEMON_OWNERSHIP",
                            severity="CRITICAL",
                            description=f"Pokemon '{name}' is on multiple teams: {pokemon_owners[name]} and {player}",
                            affected_data=f"Pokemon: {name}, Players: {pokemon_owners[name]}, {player}",
                            auto_fix=False
                        )
                    else:
                        pokemon_owners[name] = player

        except Exception as e:
            self._add_error(
                error_type="CHECK_ERROR",
                severity="MEDIUM",
                description=f"Could not check duplicate Pokemon: {e}",
                affected_data="Teams sheet",
                auto_fix=False
            )

    def _check_missing_references(self):
        """Check for broken references between sheets"""
        try:
            teams = self.sheets.get_all_teams()
            all_pokemon = [p.get("Name") for p in self.sheets.get_all_pokemon()]

            for player, team_data in teams.items():
                roster = team_data.get("roster", [])

                for pokemon in roster:
                    name = pokemon.get("name")

                    # Error 18: Pokemon not in Pokemon sheet
                    if name and name not in all_pokemon:
                        self._add_error(
                            error_type="MISSING_POKEMON_REFERENCE",
                            severity="HIGH",
                            description=f"Player '{player}' has Pokemon '{name}' not found in Pokemon sheet",
                            affected_data=f"Player: {player}, Pokemon: {name}",
                            auto_fix=False
                        )

        except Exception as e:
            self._add_error(
                error_type="CHECK_ERROR",
                severity="MEDIUM",
                description=f"Could not check references: {e}",
                affected_data="Cross-sheet references",
                auto_fix=False
            )

    def _check_invalid_types(self):
        """Check for invalid Tera types and Pokemon types"""
        # Already covered in _check_pokemon_data and _check_tera_captains
        pass

    def _check_standings_consistency(self):
        """Check if standings data is consistent"""
        try:
            # This would check that wins/losses match match history
            # Placeholder for future implementation
            pass
        except Exception as e:
            pass

    # ==================== HELPER METHODS ====================

    def _add_error(self, error_type: str, severity: str, description: str,
                   affected_data: str, auto_fix: bool, fix_action: str = ""):
        """Add an error to the errors list"""
        error = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error_type": error_type,
            "severity": severity,
            "description": description,
            "affected_data": affected_data,
            "auto_fix_available": auto_fix,
            "fix_action": fix_action,
            "status": "DETECTED"
        }
        self.errors_found.append(error)

        # Print to console
        severity_emoji = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️",
            "MEDIUM": "⚡",
            "LOW": "ℹ️"
        }
        emoji = severity_emoji.get(severity, "❓")

        print(f"{emoji} [{severity}] {error_type}: {description}")

    def _is_valid_url(self, url: str) -> bool:
        """Check if string is a valid URL"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None

    def _log_errors(self):
        """Log all errors to Error_Diagnostics sheet"""
        if not self.errors_found:
            return

        try:
            sheet = self.sheets._get_worksheet("Error_Diagnostics")

            # Add headers if sheet is empty
            if sheet.row_count == 0:
                sheet.append_row([
                    "Timestamp", "Error_Type", "Severity", "Description",
                    "Affected_Data", "Auto_Fix_Available", "Fix_Action", "Status"
                ])

            # Add errors
            for error in self.errors_found:
                sheet.append_row([
                    error["timestamp"],
                    error["error_type"],
                    error["severity"],
                    error["description"],
                    error["affected_data"],
                    "Yes" if error["auto_fix_available"] else "No",
                    error.get("fix_action", ""),
                    error["status"]
                ])

            print(f"\n📝 Logged {len(self.errors_found)} errors to Error_Diagnostics sheet")

        except Exception as e:
            print(f"⚠️ Could not log errors to sheet: {e}")

    def _generate_summary(self) -> Dict:
        """Generate error summary"""
        summary = {
            "total_errors": len(self.errors_found),
            "by_severity": {
                "CRITICAL": 0,
                "HIGH": 0,
                "MEDIUM": 0,
                "LOW": 0
            },
            "auto_fixable": 0,
            "errors": self.errors_found
        }

        for error in self.errors_found:
            severity = error["severity"]
            summary["by_severity"][severity] += 1

            if error["auto_fix_available"]:
                summary["auto_fixable"] += 1

        return summary


# Example usage
if __name__ == "__main__":
    print("Error Diagnostics Service")
    print("Detects and reports data integrity issues in Google Sheets")
