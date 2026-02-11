# Pokémon Draft League Discord Bot

A Discord bot for managing Pokémon Draft Leagues with Google Sheets integration. Handle point-based drafts, Tera Captains, team management, battle tracking, and league statistics!

## Features

✨ **Point-Based Draft System** - 120 points per player, 10-12 Pokémon per team
⚡ **Tera Captain Management** - Designate up to 3 Tera Captains with type selection
📊 **Google Sheets Integration** - All data stored in easy-to-view/edit spreadsheet
🔄 **Trade System** - Unlimited Week 1 trades, 5 max Weeks 2-5
⚔️ **Battle Tracking** - Record matches, view standings, track stats
📈 **Analytics** - Usage stats, tier lists, player statistics

## Prerequisites

- Python 3.8 or higher
- Discord account with server admin access
- Google Cloud account (free tier works!)
- Git (optional, for version control)

## Quick Start Guide

### Step 1: Clone/Download the Project

```bash
cd "F:\Claude Code\Claude\Claude Chats"
# Project is already here at pokemon-draft-bot/
```

### Step 2: Install Dependencies

```bash
cd pokemon-draft-bot
python -m venv venv
# Activate virtual environment:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Set Up Google Sheets API

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** (e.g., "Pokemon Draft Bot")
3. **Enable Google Sheets API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. **Create Service Account**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Name it "pokemon-draft-bot"
   - Click "Create and Continue"
   - Skip role assignment (click "Continue")
   - Click "Done"
5. **Generate JSON Key**:
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" → "Create New Key"
   - Choose "JSON"
   - Save the downloaded file as `.credentials.json` in the project root

### Step 4: Create Google Sheet

1. **Create a new Google Sheet**: https://sheets.google.com
2. **Share with service account**:
   - Open the `.credentials.json` file
   - Copy the `client_email` value (looks like: `pokemon-draft-bot@...iam.gserviceaccount.com`)
   - Click "Share" in your Google Sheet
   - Paste the service account email
   - Give it "Editor" permissions
   - Click "Send"
3. **Copy Spreadsheet ID**:
   - From the URL: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`
   - Save this ID for the next step

4. **⚠️ IMPORTANT: Start with Blank Sheets**

   **Do NOT pre-fill team data before the draft!** The bot will populate data as coaches:
   - Register with `!league register`
   - Complete the draft with `!draft pick`
   - Upload logos with `!league uploadlogo`

   **Workflow:**
   1. Create blank sheet tabs with headers only
   2. Run `!league init` to initialize
   3. Coaches register and draft
   4. Bot automatically populates Google Sheets
   5. Run `!league start` when draft is complete

5. **Create Sheet Tabs** (in this exact order):
   - `Config`
   - `Pokemon` (pre-fill this with all available Pokémon and their costs)
   - `Teams` (blank - populated during draft)
   - `Tera_Captains` (blank - populated when coaches set Tera Captains)
   - `Draft_History` (blank - populated during draft)
   - `Matches` (blank - populated when matches are recorded)
   - `Standings` (blank - populated automatically)
   - `Stats` (blank - populated automatically)
   - `Trades` (blank - populated when trades occur)
   - `Archived_Teams` (blank - populated when coaches are removed)
   - `Error_Diagnostics` (blank - populated by `!league diagnose`)

6. **Set up Config tab** (add these rows):
   ```
   Key                 | Value
   -------------------|------
   league_name        | My Pokemon League
   total_points       | 120
   min_pokemon        | 10
   max_pokemon        | 12
   max_tera_captains  | 3
   max_tera_points    | 25
   ```

7. **Set up Pokemon tab headers** (then add all available Pokémon):
   ```
   Name | Tier | Type1 | Type2 | Point_Cost | HP | Attack | Defense | SpAttack | SpDefense | Speed
   ```

   **Example row:**
   ```
   Pikachu | A | Electric | | 8 | 35 | 55 | 40 | 50 | 50 | 90
   ```

8. **Set up Teams tab headers** (leave data rows BLANK):
   ```
   Player | Team_Name | Team_Logo | Pokemon_List | Total_Points_Used
   ```

9. **Set up remaining tab headers** (leave data rows BLANK):
   - **Tera_Captains**: `Player | Pokemon | Tera_Type | Point_Cost`
   - **Draft_History**: `Pick_Number | Player | Pokemon | Point_Cost | Timestamp`
   - **Matches**: `Week | Player1 | Player2 | Score | Winner | Kills | Deaths | Differential | Replay_Link`
   - **Standings**: `Player | Wins | Losses | Points | Status`
   - **Stats**: `Pokemon | Times_Drafted | Win_Rate | Times_Used`
   - **Trades**: `Week | Player1 | Pokemon1 | Player2 | Pokemon2 | Status | Timestamp`
   - **Archived_Teams**: `Archived_Date | Player | Team_Name | Team_Logo | Pokemon_List | Total_Points_Used`
   - **Error_Diagnostics**: `Timestamp | Error_Type | Severity | Description | Affected_Data | Status | Auto_Fix_Attempted`

### Step 5: Set Up Discord Bot

1. **Go to Discord Developer Portal**: https://discord.com/developers/applications
2. **Click "New Application"**
   - Name it "Pokemon Draft Bot"
   - Click "Create"
3. **Go to "Bot" section**
   - Click "Add Bot" → "Yes, do it!"
   - **Copy the bot token** (keep this secret!)
4. **Enable Intents** (scroll down):
   - ✅ Message Content Intent
   - ✅ Server Members Intent
5. **Go to "OAuth2" → "URL Generator"**
   - Scopes: `bot`
   - Bot Permissions:
     - Send Messages
     - Read Messages/View Channels
     - Embed Links
     - Attach Files
     - Read Message History
   - Copy the generated URL
   - Open it in browser and invite bot to your server

### Step 6: Configure Credentials

Create a `.credentials.json` file in the project root with this structure:

```json
{
    "discord_bot_token": "YOUR_DISCORD_BOT_TOKEN_HERE",
    "spreadsheet_id": "YOUR_GOOGLE_SHEET_ID_HERE"
}
```

**Important:** Never commit this file to Git! (It's already in `.gitignore`)

### Step 7: Run the Bot

```bash
python bot.py
```

You should see:
```
Bot logged in as Pokemon Draft Bot#1234
Ready to manage draft leagues!
```

### Step 8: Test in Discord

In your Discord server, try:
```
!ping
```

If the bot responds, you're all set! 🎉

## Available Commands

### League Commands

- `!league init <name>` - Initialize new league (admin)
- `!league register "Team Name" <logo_url>` - Register as coach
- `!league uploadlogo` - Upload team logo (attach image file)
- `!league start` - Start season & create channels (admin)
- `!league addcoach @user` - Add coach to league (admin)
- `!league removecoach @user` - Remove coach (admin)
- `!league diagnose` - Run error diagnostics (admin)
- `!league reset` - Reset entire league (admin)

### Draft Commands

- `!draft start` - Start a new draft
- `!draft pick <pokemon>` - Make a draft pick
- `!draft budget [player]` - Check remaining points
- `!draft status` - Show current draft status
- `!draft undo` - Undo last pick (admin)
- `!draft end` - End the draft (admin)

### Tera Captain Commands

- `!tera` or `!tera show [player]` - Display your or another player's Tera Captains
- `!tera set <pokemon> <type>` - Designate a Pokémon as a Tera Captain with specific type
- `!tera change <pokemon> <new_type>` - Change a Tera Captain's type
- `!tera remove <pokemon>` - Remove Tera Captain designation from a Pokémon
- `!tera list` - Show all league Tera Captains grouped by player
- `!tera types` - Display all 19 valid Tera types with emojis
- `!tera help` - Show detailed Tera Captain command help

### Team Commands

- `!team <player>` - View a player's team
- `!roster` - View your own team
- `!analyze [player]` - Comprehensive team analysis (public)
- `!dmanalysis [player]` - Send analysis via Direct Message (private)
- `!teams` - List all teams
- `!trade propose <player> <your_pokemon> for <their_pokemon>` - Propose trade
- `!trade accept` - Accept pending trade
- `!trade reject` - Reject pending trade
- `!trade history [player]` - View trade history

### Battle Commands

- `!record <opponent> <score>` - Record match result
- `!schedule` - View your scheduled matches
- `!standings` - Display current standings
- `!matchups <week>` - View matchups for a week

### Stats Commands

- `!stats <pokemon>` - Show Pokémon usage stats
- `!usage` - Show most/least used Pokémon
- `!tiers` - Display tier breakdown
- `!playerstats <player>` - Show player statistics

## League Rules

### Draft Rules
- 120 points total per player
- Draft 10-12 Pokémon
- 5-minute pick timer
- Once picked, Pokémon is unavailable

### Tera Captain Rules
- **Exactly 3 Tera Captains** per team (no more, no less)
- **Point Cost Limit**: Only Pokémon with ≤13 points can be Tera Captains
- **Total Points Limit**: Combined Tera Captain points must be ≤25
- **Type Selection**: Can Terastallize to any of 19 types:
  - 18 Standard Types: Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy
  - **Stellar Type**: The 19th unique Tera type
- **Set Anytime**: Designate Tera Captains before Week 1 or change them between weeks
- **Validation**: Bot automatically validates all restrictions when setting captains

### Trade Rules
- **Week 1:** Unlimited trades
- **Weeks 2-5:** Maximum 5 total trades
- **Sunday-Tuesday:** Trades take effect immediately
- **Wednesday-Saturday:** Trades take effect next week

### Battle Rules
- Double Battles, Best-of-Three
- Bring 6, choose 4
- Nintendo Switch only
- Submit builds to judges before battle
- Record KOs and post replays

## Troubleshooting

### Bot doesn't respond
- Check bot is online (green dot in Discord)
- Verify bot has "Send Messages" permission
- Make sure Message Content Intent is enabled

### "Permission denied" on Google Sheets
- Verify service account email is shared with the sheet
- Check service account has "Editor" permissions
- Confirm `.credentials.json` contains valid credentials

### "Module not found" error
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Bot crashes on startup
- Check `.credentials.json` format is valid JSON
- Verify Discord token is correct
- Check spreadsheet ID is correct

## Project Structure

```
pokemon-draft-bot/
├── bot.py                  # Main entry point
├── config.py               # Configuration loader
├── requirements.txt        # Python dependencies
├── .credentials.json       # Secrets (not in Git)
├── .gitignore             # Ignored files
├── README.md              # This file
├── cogs/                  # Command modules
│   ├── draft.py
│   ├── team.py
│   ├── tera.py
│   ├── battle.py
│   └── stats.py
├── services/              # Business logic
│   ├── sheets_service.py
│   ├── draft_service.py
│   ├── team_service.py
│   ├── tera_service.py
│   └── battle_service.py
├── models/                # Data models
│   ├── pokemon.py
│   ├── team.py
│   └── match.py
└── utils/                 # Helpers
    ├── constants.py
    └── validators.py
```

## Support & Resources

- **Discord.py Documentation**: https://discordpy.readthedocs.io/
- **Google Sheets API**: https://developers.google.com/sheets/api
- **PokéAPI**: https://pokeapi.co/
- **Implementation Plan**: See `C:\Users\power\.claude\plans\expressive-juggling-cascade.md`

## Contributing

This bot is designed for personal/league use. Feel free to fork and customize for your own league rules!

## License

MIT License - feel free to use and modify!

---

Built with ❤️ for Pokémon Draft Leagues
