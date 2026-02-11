"""
Constants for Pokemon Draft League Bot.

Contains all Pokémon types, type emojis, and other league constants.
"""

# ==================== TERA TYPES ====================

# All valid Tera types (18 standard + Stellar)
VALID_TERA_TYPES = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
    "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy",
    "Stellar"  # Special Tera type from Scarlet/Violet
]

# Type emoji mapping for Discord embeds
TYPE_EMOJI = {
    "Normal": "⚪",
    "Fire": "🔥",
    "Water": "💧",
    "Electric": "⚡",
    "Grass": "🌿",
    "Ice": "❄️",
    "Fighting": "🥊",
    "Poison": "☠️",
    "Ground": "🌍",
    "Flying": "🦅",
    "Psychic": "🔮",
    "Bug": "🐛",
    "Rock": "🪨",
    "Ghost": "👻",
    "Dragon": "🐉",
    "Dark": "🌑",
    "Steel": "⚙️",
    "Fairy": "🧚",
    "Stellar": "✨"
}

# Type effectiveness chart (Attacking Type → Defending Type → Multiplier)
# 2.0 = Super Effective, 0.5 = Not Very Effective, 0.0 = No Effect
TYPE_CHART = {
    "Normal": {
        "Rock": 0.5, "Ghost": 0.0, "Steel": 0.5
    },
    "Fire": {
        "Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0,
        "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0
    },
    "Water": {
        "Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0,
        "Rock": 2.0, "Dragon": 0.5
    },
    "Electric": {
        "Water": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0,
        "Flying": 2.0, "Dragon": 0.5
    },
    "Grass": {
        "Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5,
        "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0,
        "Dragon": 0.5, "Steel": 0.5
    },
    "Ice": {
        "Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5,
        "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5
    },
    "Fighting": {
        "Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5,
        "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0,
        "Dark": 2.0, "Steel": 2.0, "Fairy": 0.5
    },
    "Poison": {
        "Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5,
        "Ghost": 0.5, "Steel": 0.0, "Fairy": 2.0
    },
    "Ground": {
        "Fire": 2.0, "Electric": 2.0, "Grass": 0.5, "Poison": 2.0,
        "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0
    },
    "Flying": {
        "Electric": 0.5, "Grass": 2.0, "Fighting": 2.0, "Bug": 2.0,
        "Rock": 0.5, "Steel": 0.5
    },
    "Psychic": {
        "Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0,
        "Steel": 0.5
    },
    "Bug": {
        "Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5,
        "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0,
        "Steel": 0.5, "Fairy": 0.5
    },
    "Rock": {
        "Fire": 2.0, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5,
        "Flying": 2.0, "Bug": 2.0, "Steel": 0.5
    },
    "Ghost": {
        "Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5
    },
    "Dragon": {
        "Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0
    },
    "Dark": {
        "Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5,
        "Fairy": 0.5
    },
    "Steel": {
        "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2.0,
        "Rock": 2.0, "Steel": 0.5, "Fairy": 2.0
    },
    "Fairy": {
        "Fire": 0.5, "Fighting": 2.0, "Poison": 0.5, "Dragon": 2.0,
        "Dark": 2.0, "Steel": 0.5
    }
}

# ==================== DRAFT CONSTANTS ====================

# Point-based draft system
DEFAULT_TOTAL_POINTS = 120
DEFAULT_MIN_POKEMON = 10
DEFAULT_MAX_POKEMON = 12

# Tera Captain restrictions
DEFAULT_MAX_TERA_CAPTAINS = 3
DEFAULT_MAX_TERA_CAPTAIN_COST = 13  # Max cost per Tera Captain
DEFAULT_MAX_TERA_TOTAL_POINTS = 25  # Max total points for all Tera Captains

# Draft timing
PICK_TIMEOUT_SECONDS = 300  # 5 minutes per pick

# ==================== TRADE CONSTANTS ====================

# Trade limits by week
WEEK_1_TRADE_LIMIT = None  # Unlimited
WEEKS_2_5_TRADE_LIMIT = 5   # Max 5 trades

# Days of the week (for trade timing)
IMMEDIATE_TRADE_DAYS = ["Sunday", "Monday", "Tuesday"]
DELAYED_TRADE_DAYS = ["Wednesday", "Thursday", "Friday", "Saturday"]

# ==================== BATTLE CONSTANTS ====================

# Battle format
BATTLE_FORMAT = "Double Battles, Best-of-Three"
TEAM_SIZE = 6  # Bring 6, choose 4 for each battle
ACTIVE_POKEMON = 4

# Battle clauses
BATTLE_CLAUSES = [
    "Species Clause",
    "Sleep Clause",
    "Evasion Clause",
    "OHKO Clause",
    "Moody Clause",
    "Endless Battle Clause",
    "Baton Pass Clause",
    "Item Clause"
]

# ==================== FORM-VARIANT POKEMON ====================

# Pokémon with multiple forms (can access all, bring 1 per battle)
FORM_VARIANT_POKEMON = [
    "Pikachu",
    "Basculin",
    "Oricorio",
    "Toxtricity",
    "Indeedee",
    "Basculegion",
    "Oinkologne",
    "Squawkabilly",
    "Tatsugiri",
    "Meowstic"
]

# ==================== DISCORD CONSTANTS ====================

# Role names
COACH_ROLE_NAME = "Coach"

# Category/Channel formatting
CATEGORY_NAME = "⌜🎮⌟ ᴅʀᴀꜰᴛ ʟᴇᴀɢᴜᴇ ᴄᴏᴀᴄʜᴇꜱ ⌜🎮⌟"
CHANNEL_PREFIX = "🏆┃"

# Colors for embeds
EMBED_COLOR_SUCCESS = 0x2ECC71  # Green
EMBED_COLOR_ERROR = 0xE74C3C    # Red
EMBED_COLOR_WARNING = 0xF39C12  # Orange
EMBED_COLOR_INFO = 0x3498DB     # Blue
EMBED_COLOR_TERA = 0x9B59B6     # Purple

# ==================== GOOGLE SHEETS TAB NAMES ====================

SHEET_CONFIG = "Config"
SHEET_POKEMON = "Pokemon"
SHEET_TEAMS = "Teams"
SHEET_TERA_CAPTAINS = "Tera_Captains"
SHEET_DRAFT_HISTORY = "Draft_History"
SHEET_MATCHES = "Matches"
SHEET_STANDINGS = "Standings"
SHEET_STATS = "Stats"
SHEET_TRADES = "Trades"
SHEET_ARCHIVED_TEAMS = "Archived_Teams"

# ==================== HELPER FUNCTIONS ====================

def get_type_emoji(type_name: str) -> str:
    """
    Get emoji for a Pokémon type.

    Args:
        type_name: Name of the type

    Returns:
        Emoji string, or ⭐ if not found
    """
    return TYPE_EMOJI.get(type_name, "⭐")


def is_valid_tera_type(type_name: str) -> bool:
    """
    Check if a type name is valid for Tera typing.

    Args:
        type_name: Name of the type to check

    Returns:
        True if valid, False otherwise
    """
    return type_name.title() in VALID_TERA_TYPES


def format_tera_types_display() -> str:
    """
    Format all Tera types for display in Discord.

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


def get_battle_clauses_display() -> str:
    """
    Format battle clauses for display.

    Returns:
        Formatted string with all clauses
    """
    return "\n".join([f"• {clause}" for clause in BATTLE_CLAUSES])


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    print("Pokemon Draft League Bot - Constants")
    print("=" * 50)

    print("\n📊 Draft System:")
    print(f"   Total Points: {DEFAULT_TOTAL_POINTS}")
    print(f"   Pokémon Range: {DEFAULT_MIN_POKEMON}-{DEFAULT_MAX_POKEMON}")
    print(f"   Tera Captains: {DEFAULT_MAX_TERA_CAPTAINS}")
    print(f"   Max Tera Points: {DEFAULT_MAX_TERA_TOTAL_POINTS}")

    print("\n⚡ Tera Types:")
    print(format_tera_types_display())

    print("\n⚔️ Battle Format:")
    print(f"   {BATTLE_FORMAT}")
    print(f"   Team: {TEAM_SIZE} Pokémon, Choose {ACTIVE_POKEMON}")

    print("\n📜 Battle Clauses:")
    print(get_battle_clauses_display())

    print("\n🔄 Form-Variant Pokémon:")
    for poke in FORM_VARIANT_POKEMON:
        print(f"   • {poke}")
