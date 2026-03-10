"""Tests for src/data/models.py — model properties not covered elsewhere."""
import pytest
from src.data.models import Draft, DraftFormat, DraftStatus, TeamRoster, PlayerElo


def test_total_picks_empty():
    d = Draft(
        draft_id="d1", guild_id="g1", commissioner_id="p1",
        format=DraftFormat.SNAKE, status=DraftStatus.ACTIVE,
        total_rounds=3, player_order=["p1", "p2"],
    )
    assert d.total_picks == 0


def test_total_picks_after_picks(make_pokemon):
    from src.data.models import DraftPick
    d = Draft(
        draft_id="d1", guild_id="g1", commissioner_id="p1",
        format=DraftFormat.SNAKE, status=DraftStatus.ACTIVE,
        total_rounds=3, player_order=["p1", "p2"],
    )
    d.picks.append(DraftPick(draft_id="d1", player_id="p1", pokemon_name="Garchomp", round=1, pick_number=1))
    d.picks.append(DraftPick(draft_id="d1", player_id="p2", pokemon_name="Corviknight", round=1, pick_number=2))
    assert d.total_picks == 2


def test_current_player_id_even_round_reversal():
    """In snake draft, even rounds reverse the order."""
    d = Draft(
        draft_id="d1", guild_id="g1", commissioner_id="p1",
        format=DraftFormat.SNAKE, status=DraftStatus.ACTIVE,
        total_rounds=4, player_order=["p1", "p2", "p3"],
        current_round=2, current_pick_index=0,
    )
    # Round 2 (even) → reversed: index 0 maps to len-1-0 = 2 → player_order[2] = "p3"
    assert d.current_player_id == "p3"


def test_current_player_id_even_round_middle():
    """Even round, pick index 1 of 3 players → len-1-1 = 1 → middle player."""
    d = Draft(
        draft_id="d1", guild_id="g1", commissioner_id="p1",
        format=DraftFormat.SNAKE, status=DraftStatus.ACTIVE,
        total_rounds=4, player_order=["p1", "p2", "p3"],
        current_round=2, current_pick_index=1,
    )
    assert d.current_player_id == "p2"


def test_type_coverage_property(make_pokemon):
    """TeamRoster.type_coverage returns sorted unique types."""
    garchomp = make_pokemon(name="Garchomp", types=["dragon", "ground"])
    corviknight = make_pokemon(name="Corviknight", types=["flying", "steel"])
    roster = TeamRoster(player_id="p1", guild_id="g1", pokemon=[garchomp, corviknight])
    coverage = roster.type_coverage
    assert "dragon" in coverage
    assert "ground" in coverage
    assert "flying" in coverage
    assert "steel" in coverage
    assert coverage == sorted(coverage)


def test_type_coverage_deduplicates(make_pokemon):
    """Duplicate types across Pokemon are deduplicated."""
    a = make_pokemon(name="A", types=["fire", "flying"])
    b = make_pokemon(name="B", types=["fire", "steel"])
    roster = TeamRoster(player_id="p1", guild_id="g1", pokemon=[a, b])
    assert roster.type_coverage.count("fire") == 1


def test_win_rate_with_games():
    elo = PlayerElo(player_id="p1", guild_id="g1", wins=3, losses=1)
    assert elo.win_rate == 75.0


def test_win_rate_no_games():
    elo = PlayerElo(player_id="p1", guild_id="g1", wins=0, losses=0)
    assert elo.win_rate == 0.0


def test_win_rate_all_wins():
    elo = PlayerElo(player_id="p1", guild_id="g1", wins=5, losses=0)
    assert elo.win_rate == 100.0


def test_current_player_id_empty_player_order():
    """current_player_id returns None when player_order is empty."""
    d = Draft(
        draft_id="d1", guild_id="g1", commissioner_id="p1",
        format=DraftFormat.SNAKE, status=DraftStatus.SETUP,
        total_rounds=3, player_order=[],
    )
    assert d.current_player_id is None
