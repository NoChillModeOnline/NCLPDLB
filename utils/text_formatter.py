"""
Text formatting utilities for Discord channel and category names.

Provides Unicode small caps conversion for consistent aesthetic styling.
"""


def to_small_caps(text: str) -> str:
    """
    Convert text to Unicode small caps for aesthetic channel names.

    Example:
        "Fire Fighters" -> "ꜰɪʀᴇ ꜰɪɢʜᴛᴇʀꜱ"

    Args:
        text: Input text to convert

    Returns:
        Text converted to small caps Unicode characters
    """
    # Small caps mapping (lowercase letters only for consistency)
    small_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ',
        'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ',
        'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ',
        'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ',
        'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ',
        'z': 'ᴢ',
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ',
        'F': 'ꜰ', 'G': 'ɢ', 'H': 'ʜ', 'I': 'ɪ', 'J': 'ᴊ',
        'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ',
        'P': 'ᴘ', 'Q': 'ǫ', 'R': 'ʀ', 'S': 'ꜱ', 'T': 'ᴛ',
        'U': 'ᴜ', 'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ',
        'Z': 'ᴢ'
    }

    # Convert each character
    result = []
    for char in text:
        result.append(small_caps_map.get(char, char))

    return ''.join(result)


def format_team_channel_name(team_name: str) -> str:
    """
    Format a team name for use as a Discord channel name.

    Example:
        "Fire Fighters" -> "🏆┃ꜰɪʀᴇ-ꜰɪɢʜᴛᴱʀꜱ"

    Args:
        team_name: Original team name

    Returns:
        Formatted channel name with trophy emoji and small caps
    """
    # Convert to lowercase and replace spaces with hyphens
    sanitized = team_name.lower().replace(' ', '-')

    # Remove special characters (keep alphanumeric and hyphens)
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '-')

    # Convert to small caps
    small_caps = to_small_caps(sanitized)

    # Add trophy emoji and separator
    return f"🏆┃{small_caps}"


def format_category_name() -> str:
    """
    Get the standardized category name for draft league coaches.

    Returns:
        "⌜🎮⌟ ᴅʀᴀꜰᴛ ʟᴇᴀɢᴜᴇ ᴄᴏᴀᴄʜᴇꜱ ⌜🎮⌟"
    """
    return "⌜🎮⌟ ᴅʀᴀꜰᴛ ʟᴇᴀɢᴜᴇ ᴄᴏᴀᴄʜᴇꜱ ⌜🎮⌟"


# Example usage and tests
if __name__ == "__main__":
    print("Text Formatter Examples:")
    print(f"Category: {format_category_name()}")
    print(f"Team 'Fire Fighters': {format_team_channel_name('Fire Fighters')}")
    print(f"Team 'Team Rocket': {format_team_channel_name('Team Rocket')}")
    print(f"Team 'Ice Warriors': {format_team_channel_name('Ice Warriors')}")
