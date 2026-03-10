"""Tests for src/data/sheets.py — SheetsClient methods (gspread mocked)."""
import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

from src.data.sheets import SheetsClient, Tab, sheets


# ── Fixture: worksheet mock ──────────────────────────────────────────────────

@pytest.fixture
def mock_ws():
    ws = MagicMock()
    ws.get_all_records.return_value = []
    ws.row_values.return_value = []
    return ws


@pytest.fixture
def patched_get_tab(mock_ws):
    """Patches sheets.get_tab to return mock_ws without touching Google."""
    with patch.object(sheets, "get_tab", return_value=mock_ws) as p:
        yield mock_ws, p


# ── connect() ────────────────────────────────────────────────────────────────

def test_connect_file_not_found(tmp_path):
    """connect() raises FileNotFoundError when credentials file is missing."""
    fresh = SheetsClient.__new__(SheetsClient)
    fresh._spreadsheet = None
    fresh._client = None
    with patch("src.data.sheets.settings") as ms:
        ms.google_sheets_credentials_file = tmp_path / "missing.json"
        ms.google_sheets_spreadsheet_id = "x"
        with pytest.raises(FileNotFoundError):
            fresh.connect()


def test_connect_success(tmp_path):
    """connect() sets _spreadsheet on success."""
    creds_file = tmp_path / "credentials.json"
    creds_file.write_text('{"type":"service_account"}')

    fresh = SheetsClient.__new__(SheetsClient)
    fresh._spreadsheet = None
    fresh._client = None

    with patch("src.data.sheets.settings") as ms, \
         patch("src.data.sheets.Credentials.from_service_account_file") as mock_creds, \
         patch("src.data.sheets.gspread.authorize") as mock_auth:
        ms.google_sheets_credentials_file = creds_file
        ms.google_sheets_spreadsheet_id = "test-id"
        mock_sp = MagicMock()
        mock_sp.title = "Test Sheet"
        mock_auth.return_value.open_by_key.return_value = mock_sp
        fresh.connect()
    assert fresh._spreadsheet is mock_sp


# ── spreadsheet property ──────────────────────────────────────────────────────

def test_spreadsheet_property_calls_connect_when_none():
    """spreadsheet property triggers connect() if _spreadsheet is None."""
    fresh = SheetsClient.__new__(SheetsClient)
    fresh._spreadsheet = None
    fresh._client = None
    mock_sp = MagicMock()
    mock_sp.title = "T"
    with patch.object(fresh, "connect", side_effect=lambda: setattr(fresh, "_spreadsheet", mock_sp)):
        sp = fresh.spreadsheet
    assert sp is mock_sp


# ── get_tab() ─────────────────────────────────────────────────────────────────

def test_get_tab_found():
    """get_tab returns worksheet when it exists."""
    fresh = SheetsClient.__new__(SheetsClient)
    mock_sp = MagicMock()
    mock_ws = MagicMock()
    mock_sp.worksheet.return_value = mock_ws
    fresh._spreadsheet = mock_sp
    result = fresh.get_tab(Tab.SETUP)
    assert result is mock_ws


def test_get_tab_creates_when_not_found():
    """get_tab creates the tab when WorksheetNotFound is raised."""
    import gspread
    fresh = SheetsClient.__new__(SheetsClient)
    mock_sp = MagicMock()
    new_ws = MagicMock()
    mock_sp.worksheet.side_effect = gspread.WorksheetNotFound
    mock_sp.add_worksheet.return_value = new_ws
    fresh._spreadsheet = mock_sp
    result = fresh.get_tab(Tab.SETUP)
    assert result is new_ws
    new_ws.append_row.assert_called_once()


# ── read_all / append_row / update_row ───────────────────────────────────────

def test_read_all(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [{"key": "val"}]
    result = sheets.read_all(Tab.SETUP)
    assert result == [{"key": "val"}]


def test_append_row(patched_get_tab):
    mock_ws, _ = patched_get_tab
    sheets.append_row(Tab.DRAFT, ["a", "b", "c"])
    mock_ws.append_row.assert_called_once_with(["a", "b", "c"], value_input_option="USER_ENTERED")


def test_update_row(patched_get_tab):
    mock_ws, _ = patched_get_tab
    sheets.update_row(Tab.STANDINGS, 3, ["x", "y"])
    mock_ws.update.assert_called_once_with("A3", [["x", "y"]])


# ── find_row / find_rows ──────────────────────────────────────────────────────

def test_find_row_found(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [
        {"player_id": "p1", "name": "Alice"},
        {"player_id": "p2", "name": "Bob"},
    ]
    result = sheets.find_row(Tab.STANDINGS, "player_id", "p1")
    assert result["name"] == "Alice"


def test_find_row_not_found(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    assert sheets.find_row(Tab.STANDINGS, "player_id", "missing") is None


def test_find_rows(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [
        {"draft_id": "d1", "pick": "Garchomp"},
        {"draft_id": "d1", "pick": "Corviknight"},
        {"draft_id": "d2", "pick": "Toxapex"},
    ]
    result = sheets.find_rows(Tab.DRAFT, "draft_id", "d1")
    assert len(result) == 2


# ── upsert_row ────────────────────────────────────────────────────────────────

def test_upsert_row_appends_when_not_found(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["player_id", "name"]
    sheets.upsert_row(Tab.STANDINGS, "player_id", "p99", ["p99", "New Guy"])
    mock_ws.append_row.assert_called()


def test_upsert_row_updates_when_found(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [{"player_id": "p1", "name": "Alice"}]
    mock_ws.row_values.return_value = ["player_id", "name"]
    sheets.upsert_row(Tab.STANDINGS, "player_id", "p1", ["p1", "Alice Updated"])
    mock_ws.update.assert_called()


def test_upsert_row_appends_when_col_not_in_headers(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["other_col"]
    sheets.upsert_row(Tab.STANDINGS, "player_id", "p1", ["p1", "Alice"])
    mock_ws.append_row.assert_called()


# ── Domain methods ────────────────────────────────────────────────────────────

def test_save_league_setup(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["server_id"]
    sheets.save_league_setup({
        "league_id": "L1", "server_id": "S1", "league_name": "Test League",
        "commissioner_id": "C1", "commissioner_name": "Admin",
    })
    mock_ws.append_row.assert_called()


def test_save_pick(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = []
    sheets.save_pick({"pick_id": "pk1", "draft_id": "d1", "pokemon_name": "Garchomp"})
    mock_ws.append_row.assert_called()


def test_get_draft_picks(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [
        {"draft_id": "d1", "pokemon": "Garchomp"},
        {"draft_id": "d2", "pokemon": "Other"},
    ]
    result = sheets.get_draft_picks("d1")
    assert len(result) == 1


def test_update_pool_roster_pool_a(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["player_id"]
    sheets.update_pool_roster("A", {"player_id": "p1", "player_name": "Alice", "team_name": "Team A"}, ["Garchomp"])
    mock_ws.append_row.assert_called()


def test_update_pool_roster_pool_b(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["player_id"]
    sheets.update_pool_roster("B", {"player_id": "p2", "player_name": "Bob", "team_name": "Team B"}, [])
    mock_ws.append_row.assert_called()


def test_save_schedule_match(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["match_id"]
    sheets.save_schedule_match({"match_id": "m1", "week": 1, "player1_id": "p1", "player2_id": "p2"})
    mock_ws.append_row.assert_called()


def test_save_match_stats(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["match_id"]
    sheets.save_match_stats({
        "match_id": "m1", "league_id": "L1",
        "p1_team": ["Garchomp"], "p2_team": ["Corviknight"],
    })
    mock_ws.append_row.assert_called()


def test_upsert_standing(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["player_id"]
    sheets.upsert_standing({"player_id": "p1", "elo": 1050, "wins": 3, "losses": 1})
    mock_ws.append_row.assert_called()


def test_get_league_setup_found(patched_get_tab):
    """get_league_setup returns the matching row for a server_id."""
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [
        {"server_id": "S1", "league_name": "Test League"},
        {"server_id": "S2", "league_name": "Other"},
    ]
    result = sheets.get_league_setup("S1")
    assert result is not None
    assert result["league_name"] == "Test League"


def test_get_standings_all(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [
        {"rank": 1, "pool": "A", "player_id": "p1"},
        {"rank": 2, "pool": "B", "player_id": "p2"},
    ]
    result = sheets.get_standings()
    assert len(result) == 2


def test_get_standings_filtered_by_pool(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [
        {"rank": 1, "pool": "A", "player_id": "p1"},
        {"rank": 2, "pool": "B", "player_id": "p2"},
    ]
    result = sheets.get_standings(pool="A")
    assert len(result) == 1
    assert result[0]["player_id"] == "p1"


def test_update_pokemon_stat(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["stat_id"]
    sheets.update_pokemon_stat({"stat_id": "s1", "pokemon": "Garchomp", "wins": 5})
    mock_ws.append_row.assert_called()


def test_refresh_mvp_race(patched_get_tab):
    mock_ws, _ = patched_get_tab
    entries = [{"rank": 1, "player_id": "p1", "mvp_pokemon": "Garchomp", "mvp_count": 3}]
    sheets.refresh_mvp_race(entries)
    mock_ws.resize.assert_called()
    mock_ws.append_row.assert_called()


def test_save_transaction(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["transaction_id"]
    sheets.save_transaction({"transaction_id": "t1", "type": "trade", "status": "pending"})
    mock_ws.append_row.assert_called()


def test_save_playoff_match(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["bracket_id"]
    sheets.save_playoff_match({"bracket_id": "b1", "round": "QF", "match_number": 1})
    mock_ws.append_row.assert_called()


def test_bulk_write_pokedex(patched_get_tab):
    mock_ws, _ = patched_get_tab
    pokemon_list = [
        {
            "national_dex": 1, "name": "Bulbasaur",
            "types": ["grass", "poison"],
            "base_stats": {"hp": 45, "atk": 49, "def": 49, "spa": 65, "spd": 65, "spe": 45},
            "showdown_tier": "NU", "generation": 1,
            "is_legendary": False, "is_mythical": False,
            "vgc_legal": True, "console_legal": {"sv": True, "swsh": False},
            "sprite_url": "",
        }
    ]
    sheets.bulk_write_pokedex(pokemon_list)
    mock_ws.clear.assert_called_once()
    mock_ws.append_rows.assert_called_once()


def test_bulk_write_pokedex_empty(patched_get_tab):
    mock_ws, _ = patched_get_tab
    sheets.bulk_write_pokedex([])
    mock_ws.clear.assert_called_once()
    mock_ws.append_rows.assert_not_called()


def test_upsert_team_page(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["player_id"]
    sheets.upsert_team_page({
        "player_id": "p1", "player_name": "Alice", "team_name": "Team A",
        "slots": [("Garchomp", "Dragon"), ("Corviknight", "Flying")],
    })
    mock_ws.append_row.assert_called()


def test_upsert_team_page_no_slots(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["player_id"]
    sheets.upsert_team_page({"player_id": "p1", "player_name": "Alice", "team_name": "T"})
    mock_ws.append_row.assert_called()


def test_set_data(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["key"]
    sheets.set_data("season", "3", "string", "Current season")
    mock_ws.append_row.assert_called()


def test_get_data_found(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [{"key": "season", "value": "3"}]
    result = sheets.get_data("season")
    assert result == "3"


def test_get_data_not_found(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    assert sheets.get_data("missing_key") is None


def test_save_replay_no_existing_match(patched_get_tab):
    """save_replay does nothing when match is not found."""
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    # Should not raise
    sheets.save_replay({"match_id": "m999", "url": "https://replay.ps.com/r1", "p1_team": [], "p2_team": [], "turns": 10})


def test_save_replay_updates_existing(patched_get_tab):
    """save_replay updates match row when match_id found."""
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = [
        {"match_id": "m1", "league_id": "L1", "week": 1, "pool": "A",
         "player1_id": "p1", "player1_name": "Alice",
         "player2_id": "p2", "player2_name": "Bob",
         "winner_id": "p1", "winner_name": "Alice",
         "game_format": "showdown", "replay_url": "", "video_url": ""},
    ]
    mock_ws.row_values.return_value = ["match_id"]
    sheets.save_replay({
        "match_id": "m1", "url": "https://replay.ps.com/r1",
        "p1_team": ["Garchomp"], "p2_team": ["Corviknight"], "turns": 25,
    })
    mock_ws.update.assert_called()


def test_save_video(patched_get_tab):
    mock_ws, _ = patched_get_tab
    mock_ws.get_all_records.return_value = []
    mock_ws.row_values.return_value = ["match_id"]
    sheets.save_video({
        "match_id": "m1", "league_id": "L1",
        "uploader_id": "p1", "opponent_id": "p2",
        "storage_url": "https://r2.example.com/video.mp4",
    })
    mock_ws.append_row.assert_called()
