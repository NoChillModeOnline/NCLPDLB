"""
Draft service for Pokemon Draft League Bot.

Handles all draft logic including point-based budgets, pick validation,
draft order management, and late pick recovery.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random

from services.sheets_service import SheetsService
from utils.constants import (
    DEFAULT_TOTAL_POINTS,
    DEFAULT_MIN_POKEMON,
    DEFAULT_MAX_POKEMON,
    PICK_TIMEOUT_SECONDS
)


class DraftService:
    """Handles draft operations with point-based system"""

    def __init__(self, sheets_service: SheetsService):
        """
        Initialize draft service.

        Args:
            sheets_service: Google Sheets service instance
        """
        self.sheets = sheets_service
        self.draft_state = None
        self.pick_timers = {}  # Track when each pick started

    # ==================== DRAFT INITIALIZATION ====================

    def start_draft(self, players: List[str], draft_type: str = "snake") -> Dict:
        """
        Start a new draft.

        Args:
            players: List of player names
            draft_type: "snake" or "linear" (snake reverses each round)

        Returns:
            Draft state dictionary

        Raises:
            ValueError: If invalid parameters
        """
        if len(players) < 2:
            raise ValueError("Need at least 2 players to start a draft")

        if draft_type not in ["snake", "linear"]:
            raise ValueError("Draft type must be 'snake' or 'linear'")

        # Shuffle players for fairness
        shuffled_players = players.copy()
        random.shuffle(shuffled_players)

        # Initialize draft state
        self.draft_state = {
            "players": shuffled_players,
            "draft_type": draft_type,
            "current_round": 1,
            "current_pick": 1,
            "total_picks": 0,
            "is_active": True,
            "started_at": datetime.now().isoformat(),
            "player_budgets": {player: DEFAULT_TOTAL_POINTS for player in shuffled_players},
            "player_pokemon_counts": {player: 0 for player in shuffled_players},
            "drafted_pokemon": [],  # List of drafted Pokemon names
            "pick_history": []  # List of all picks made
        }

        # Start timer for first pick
        self._start_pick_timer(self._get_current_player())

        return self.draft_state

    # ==================== DRAFT PICKS ====================

    def make_pick(self, player: str, pokemon: str) -> Dict:
        """
        Make a draft pick.

        Args:
            player: Player name making the pick
            pokemon: Pokemon name being drafted

        Returns:
            Pick result dictionary

        Raises:
            ValueError: If pick is invalid
        """
        if not self.draft_state or not self.draft_state["is_active"]:
            raise ValueError("No active draft")

        current_player = self._get_current_player()

        # Allow late picks (pick recovery)
        # If it's not the player's turn but they missed earlier, allow it
        if player != current_player:
            if player not in self.draft_state["players"]:
                raise ValueError(f"{player} is not in this draft")

            # Check if this player has a pending pick
            if not self._has_pending_pick(player):
                raise ValueError(f"It's not {player}'s turn. Current player: {current_player}")

        # Get Pokemon data and cost
        try:
            pokemon_data = self.sheets.get_pokemon_data(pokemon)
            cost = pokemon_data["point_cost"]
        except Exception as e:
            raise ValueError(f"Pokemon not found: {pokemon}")

        # Validate pick
        self._validate_pick(player, pokemon, cost)

        # Record the pick
        pick_number = self.draft_state["total_picks"] + 1
        pick_data = {
            "pick_number": pick_number,
            "player": player,
            "pokemon": pokemon,
            "cost": cost,
            "timestamp": datetime.now().isoformat(),
            "round": self.draft_state["current_round"]
        }

        # Update draft state
        self.draft_state["drafted_pokemon"].append(pokemon)
        self.draft_state["pick_history"].append(pick_data)
        self.draft_state["player_budgets"][player] -= cost
        self.draft_state["player_pokemon_counts"][player] += 1
        self.draft_state["total_picks"] += 1

        # Record in Google Sheets
        self.sheets.record_draft_pick(
            pick_num=pick_number,
            player=player,
            pokemon=pokemon,
            point_cost=cost
        )

        # Update player's roster in Teams sheet
        self._update_player_roster(player)

        # Advance to next pick (if not late pick recovery)
        if player == current_player:
            self._advance_turn()

        return {
            "success": True,
            "pick_data": pick_data,
            "remaining_budget": self.draft_state["player_budgets"][player],
            "pokemon_count": self.draft_state["player_pokemon_counts"][player],
            "next_player": self._get_current_player() if self.draft_state["is_active"] else None
        }

    def _validate_pick(self, player: str, pokemon: str, cost: int):
        """
        Validate a draft pick.

        Args:
            player: Player making the pick
            pokemon: Pokemon being picked
            cost: Pokemon point cost

        Raises:
            ValueError: If pick is invalid
        """
        # Check if Pokemon already drafted
        if pokemon in self.draft_state["drafted_pokemon"]:
            raise ValueError(f"{pokemon} has already been drafted!")

        # Check budget
        current_budget = self.draft_state["player_budgets"][player]
        if cost > current_budget:
            raise ValueError(
                f"Not enough points! {pokemon} costs {cost} points, "
                f"but you only have {current_budget} points remaining."
            )

        # Check max Pokemon limit
        current_count = self.draft_state["player_pokemon_counts"][player]
        if current_count >= DEFAULT_MAX_POKEMON:
            raise ValueError(
                f"Maximum Pokemon limit reached! You already have {current_count} Pokemon. "
                f"Maximum allowed is {DEFAULT_MAX_POKEMON}."
            )

        # Check if player will have enough budget for remaining slots
        remaining_slots = DEFAULT_MIN_POKEMON - current_count - 1  # -1 for current pick
        if remaining_slots > 0:
            remaining_budget_after_pick = current_budget - cost
            # Assume minimum cost of 1 point per Pokemon
            if remaining_budget_after_pick < remaining_slots:
                raise ValueError(
                    f"This pick would leave you without enough points for minimum team size! "
                    f"You need at least {DEFAULT_MIN_POKEMON} Pokemon."
                )

    def _update_player_roster(self, player: str):
        """
        Update player's roster in Google Sheets.

        Args:
            player: Player name
        """
        # Get all Pokemon drafted by this player
        player_picks = [
            pick["pokemon"]
            for pick in self.draft_state["pick_history"]
            if pick["player"] == player
        ]

        # Calculate total points used
        total_points = DEFAULT_TOTAL_POINTS - self.draft_state["player_budgets"][player]

        # Update in sheets
        self.sheets.update_team_roster(player, player_picks, total_points)

    # ==================== DRAFT NAVIGATION ====================

    def _get_current_player(self) -> str:
        """
        Get the current player whose turn it is.

        Returns:
            Player name
        """
        if not self.draft_state or not self.draft_state["is_active"]:
            return None

        players = self.draft_state["players"]
        current_round = self.draft_state["current_round"]
        current_pick = self.draft_state["current_pick"]
        draft_type = self.draft_state["draft_type"]

        # Snake draft: reverse order on even rounds
        if draft_type == "snake" and current_round % 2 == 0:
            player_index = len(players) - current_pick
        else:
            player_index = current_pick - 1

        return players[player_index]

    def _advance_turn(self):
        """Advance to the next pick in the draft."""
        players_count = len(self.draft_state["players"])

        # Check if round is complete
        if self.draft_state["current_pick"] >= players_count:
            self.draft_state["current_round"] += 1
            self.draft_state["current_pick"] = 1
        else:
            self.draft_state["current_pick"] += 1

        # Check if draft should end
        if self._should_end_draft():
            self.draft_state["is_active"] = False
            self.draft_state["ended_at"] = datetime.now().isoformat()
        else:
            # Start timer for next player
            next_player = self._get_current_player()
            self._start_pick_timer(next_player)

    def _should_end_draft(self) -> bool:
        """
        Check if draft should end.

        Returns:
            True if all players have minimum Pokemon or can't afford more
        """
        for player in self.draft_state["players"]:
            count = self.draft_state["player_pokemon_counts"][player]
            budget = self.draft_state["player_budgets"][player]

            # Player still needs more Pokemon and has budget
            if count < DEFAULT_MIN_POKEMON and budget > 0:
                return False

            # Player can still pick more (under max and has budget)
            if count < DEFAULT_MAX_POKEMON and budget > 0:
                # Check if there are any available Pokemon they can afford
                if self._has_affordable_pokemon(budget):
                    return False

        return True

    def _has_affordable_pokemon(self, budget: int) -> bool:
        """
        Check if there are any Pokemon available within budget.

        Args:
            budget: Available points

        Returns:
            True if there are affordable Pokemon available
        """
        all_pokemon = self.sheets.get_all_pokemon()
        drafted = self.draft_state["drafted_pokemon"]

        for pokemon in all_pokemon:
            if pokemon["Name"] not in drafted and pokemon.get("Point_Cost", 999) <= budget:
                return True

        return False

    # ==================== PICK TIMER MANAGEMENT ====================

    def _start_pick_timer(self, player: str):
        """
        Start pick timer for a player.

        Args:
            player: Player name
        """
        self.pick_timers[player] = datetime.now()

    def check_pick_timeout(self, player: str) -> bool:
        """
        Check if a player's pick has timed out.

        Args:
            player: Player name

        Returns:
            True if pick has timed out (> 5 minutes)
        """
        if player not in self.pick_timers:
            return False

        elapsed = datetime.now() - self.pick_timers[player]
        return elapsed.total_seconds() > PICK_TIMEOUT_SECONDS

    def _has_pending_pick(self, player: str) -> bool:
        """
        Check if a player has a pending pick (late pick recovery).

        Args:
            player: Player name

        Returns:
            True if player missed their turn and can still pick
        """
        # Count how many picks this player should have made by now
        total_picks_so_far = self.draft_state["total_picks"]
        players_count = len(self.draft_state["players"])

        # Calculate expected picks for this player
        player_index = self.draft_state["players"].index(player)
        expected_picks = 0

        for pick_num in range(1, total_picks_so_far + 1):
            round_num = ((pick_num - 1) // players_count) + 1
            pick_in_round = ((pick_num - 1) % players_count) + 1

            if self.draft_state["draft_type"] == "snake" and round_num % 2 == 0:
                expected_index = players_count - pick_in_round
            else:
                expected_index = pick_in_round - 1

            if expected_index == player_index:
                expected_picks += 1

        # Check actual picks made
        actual_picks = self.draft_state["player_pokemon_counts"][player]

        return actual_picks < expected_picks

    # ==================== DRAFT STATUS ====================

    def get_draft_status(self) -> Dict:
        """
        Get current draft status.

        Returns:
            Draft status dictionary
        """
        if not self.draft_state:
            return {
                "is_active": False,
                "message": "No draft in progress"
            }

        current_player = self._get_current_player()

        return {
            "is_active": self.draft_state["is_active"],
            "current_round": self.draft_state["current_round"],
            "current_pick": self.draft_state["current_pick"],
            "current_player": current_player,
            "total_picks": self.draft_state["total_picks"],
            "players": self.draft_state["players"],
            "draft_type": self.draft_state["draft_type"],
            "pick_timeout": self.check_pick_timeout(current_player) if current_player else False
        }

    def get_player_budget(self, player: str) -> Dict:
        """
        Get a player's budget status.

        Args:
            player: Player name

        Returns:
            Budget status dictionary
        """
        if not self.draft_state:
            raise ValueError("No active draft")

        if player not in self.draft_state["players"]:
            raise ValueError(f"{player} is not in this draft")

        budget = self.draft_state["player_budgets"][player]
        used = DEFAULT_TOTAL_POINTS - budget
        count = self.draft_state["player_pokemon_counts"][player]

        # Get player's drafted Pokemon
        player_picks = [
            pick for pick in self.draft_state["pick_history"]
            if pick["player"] == player
        ]

        return {
            "player": player,
            "total_points": DEFAULT_TOTAL_POINTS,
            "points_used": used,
            "points_remaining": budget,
            "pokemon_count": count,
            "min_pokemon": DEFAULT_MIN_POKEMON,
            "max_pokemon": DEFAULT_MAX_POKEMON,
            "drafted_pokemon": player_picks
        }

    def get_available_pokemon(self, max_cost: Optional[int] = None) -> List[Dict]:
        """
        Get list of available Pokemon.

        Args:
            max_cost: Optional maximum cost filter

        Returns:
            List of available Pokemon dictionaries
        """
        if not self.draft_state:
            raise ValueError("No active draft")

        all_pokemon = self.sheets.get_all_pokemon()
        drafted = self.draft_state["drafted_pokemon"]

        available = [
            {
                "name": p["Name"],
                "tier": p.get("Tier", ""),
                "type1": p.get("Type1", ""),
                "type2": p.get("Type2", ""),
                "cost": p.get("Point_Cost", 0)
            }
            for p in all_pokemon
            if p["Name"] not in drafted
        ]

        # Apply cost filter if specified
        if max_cost is not None:
            available = [p for p in available if p["cost"] <= max_cost]

        # Sort by cost descending
        available.sort(key=lambda x: x["cost"], reverse=True)

        return available

    # ==================== DRAFT MANAGEMENT ====================

    def undo_last_pick(self) -> Dict:
        """
        Undo the last draft pick (admin function).

        Returns:
            Undone pick data

        Raises:
            ValueError: If no picks to undo
        """
        if not self.draft_state or not self.draft_state["pick_history"]:
            raise ValueError("No picks to undo")

        # Get last pick
        last_pick = self.draft_state["pick_history"].pop()

        # Restore state
        self.draft_state["drafted_pokemon"].remove(last_pick["pokemon"])
        self.draft_state["player_budgets"][last_pick["player"]] += last_pick["cost"]
        self.draft_state["player_pokemon_counts"][last_pick["player"]] -= 1
        self.draft_state["total_picks"] -= 1

        # If draft had ended, reactivate it
        if not self.draft_state["is_active"]:
            self.draft_state["is_active"] = True
            if "ended_at" in self.draft_state:
                del self.draft_state["ended_at"]

        # Update roster in sheets
        self._update_player_roster(last_pick["player"])

        return last_pick

    def end_draft(self):
        """End the draft manually (admin function)."""
        if not self.draft_state:
            raise ValueError("No active draft")

        self.draft_state["is_active"] = False
        self.draft_state["ended_at"] = datetime.now().isoformat()


# Example usage and testing
if __name__ == "__main__":
    print("Draft Service - Example Usage")
    print("=" * 50)

    print("\nThis service handles:")
    print("1. Point-based draft system (120 points per player)")
    print("2. Snake draft order (reverses each round)")
    print("3. Pick validation (budget, limits, availability)")
    print("4. Late pick recovery (missed picks can be made later)")
    print("5. Pick timer management (5-minute timeout per pick)")
    print("6. Draft status tracking")
