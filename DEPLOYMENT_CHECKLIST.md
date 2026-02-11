# 🚀 Deployment Checklist

**Status:** Ready for Production
**Last Updated:** 2026-02-10

---

## ✅ Pre-Deployment Verification

- [x] All code written and committed (33 files)
- [x] Tests passing (8/8 tests)
- [x] Documentation complete (11 files, 9,000+ lines)
- [x] Git repository initialized
- [x] .gitignore configured to protect credentials

---

## 📋 Deployment Steps

### Step 1: Set Up Google Sheets

1. **Create Google Cloud Project**
   - Go to: https://console.cloud.google.com/
   - Create new project: "Pokemon Draft Bot"

2. **Enable Google Sheets API**
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

3. **Create Service Account**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Name: "pokemon-draft-bot"
   - Grant role: "Editor"
   - Click "Done"

4. **Generate Service Account Key**
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" → "Create New Key"
   - Choose "JSON" format
   - Download the JSON file

5. **Create Google Sheet**
   - Go to: https://sheets.google.com/
   - Create new spreadsheet: "Pokemon Draft League"
   - Share with service account email (found in JSON):
     - Click "Share" button
     - Paste service account email (looks like: `pokemon-draft-bot@project-id.iam.gserviceaccount.com`)
     - Grant "Editor" access
   - Copy the spreadsheet ID from URL:
     - URL format: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`
     - Copy the `{SPREADSHEET_ID}` part

6. **Create Required Sheets**
   The bot will create these automatically, but you can pre-create them:
   - Config
   - Pokemon
   - Teams
   - Tera_Captains
   - Draft_History
   - Matches
   - Standings
   - Stats
   - Trades
   - Archived_Teams
   - Error_Diagnostics

---

### Step 2: Set Up Discord Bot

1. **Create Discord Application**
   - Go to: https://discord.com/developers/applications
   - Click "New Application"
   - Name: "Pokemon Draft Bot"

2. **Create Bot**
   - Go to "Bot" tab
   - Click "Add Bot"
   - Enable these intents:
     - ✅ Presence Intent
     - ✅ Server Members Intent
     - ✅ Message Content Intent

3. **Get Bot Token**
   - Under "Bot" tab, click "Reset Token"
   - Copy the token (you'll need this for credentials)
   - ⚠️ **IMPORTANT:** Never share this token publicly!

4. **Set Bot Permissions**
   - Go to "OAuth2" → "URL Generator"
   - Select scopes:
     - ✅ bot
     - ✅ applications.commands
   - Select bot permissions:
     - ✅ Read Messages/View Channels
     - ✅ Send Messages
     - ✅ Send Messages in Threads
     - ✅ Embed Links
     - ✅ Attach Files
     - ✅ Read Message History
     - ✅ Add Reactions
     - ✅ Manage Channels
     - ✅ Manage Roles
     - ✅ Use External Emojis

5. **Invite Bot to Server**
   - Copy the generated URL from step 4
   - Paste in browser and authorize to your Discord server

---

### Step 3: Configure Credentials

1. **Create `.credentials.json`**
   ```bash
   cd "F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot"
   notepad .credentials.json
   ```

2. **Add Your Credentials**
   Paste this template and fill in your values:
   ```json
   {
     "discord_bot_token": "YOUR_DISCORD_BOT_TOKEN_HERE",
     "spreadsheet_id": "YOUR_GOOGLE_SHEET_ID_HERE",
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "key-id-from-json",
     "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
     "client_email": "pokemon-draft-bot@project-id.iam.gserviceaccount.com",
     "client_id": "123456789",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
   }
   ```

3. **Verify File is Protected**
   ```bash
   git status
   ```
   Should show: `.credentials.json` is NOT listed (protected by .gitignore)

---

### Step 4: Install Dependencies

```bash
cd "F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot"
pip install -r requirements.txt
```

Expected output:
```
Successfully installed discord.py-2.6.4 gspread-5.12.0 google-auth-2.23.0 ...
```

---

### Step 5: Start the Bot

```bash
python bot.py
```

Expected output:
```
🤖 Pokemon Draft League Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Version: 1.0.0
Python: 3.x.x
Discord.py: 2.6.4

📋 Configuration loaded from .credentials.json

🔌 Loading cogs...
  ✅ Loaded cogs.league
  ✅ Loaded cogs.draft
  ✅ Loaded cogs.tera
  ✅ Loaded cogs.team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Bot is ready!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Logged in as: YourBotName#1234
  Connected to X servers
  Prefix: !

Type Ctrl+C to stop the bot.
```

---

## 🧪 Testing the Bot

### Test 1: Basic Commands

In your Discord server:
```
!help
```
Expected: Bot responds with command list

### Test 2: League Initialization

```
!league init "Test League"
```
Expected:
- Creates "Coach" role
- Announces league creation

### Test 3: Register as Coach

```
!league register "Test Team" https://i.imgur.com/example.png
```
Expected:
- Assigns Coach role to you
- Stores team in Google Sheets
- Confirms registration

### Test 4: Upload Team Logo

```
!league uploadlogo
```
Then attach an image file.
Expected:
- Uploads image to Google Sheet
- Updates team logo URL
- Confirms upload

### Test 5: Start Draft (Interactive)

```
!draft start
```
Expected:
- Asks 3 questions:
  1. Draft format (snake/auction)
  2. Number of rounds
  3. Pick time limit
- Creates draft order
- Announces draft start

### Test 6: Make Draft Pick

```
!draft pick Pikachu
```
Expected:
- Validates it's your turn
- Checks Pokémon availability
- Records pick with point cost
- Updates roster
- Announces pick

### Test 7: View Team

```
!team @YourName
```
Expected:
- Shows your roster
- Lists Pokémon with types
- Shows points used

### Test 8: Set Tera Captain

```
!tera set Pikachu Dragon
```
Expected:
- Validates Pokémon on roster
- Checks point cost ≤13
- Records Tera Captain
- Shows confirmation

### Test 9: Team Analysis (Public)

```
!analyze
```
Expected:
- Sends 7 embeds in channel
- Type coverage
- Weaknesses
- Tera suggestions
- Speed tiers

### Test 10: Team Analysis (Private DM)

```
!dmanalysis
```
Expected:
- Sends 7 embeds via DM
- Includes competitive resource links
- Confirms in channel

### Test 11: Complete Draft and Start League

```
!league start
```
Expected:
- Creates category: ⌜🎮⌟ ᴅʀᴀꜰᴛ ʟᴇᴀɢᴜᴇ ᴄᴏᴀᴄʜᴇꜱ ⌜🎮⌟
- Creates private channels for each coach
- Posts welcome embeds with rosters

---

## 🔧 Troubleshooting

### Bot Won't Start

**Error:** `Credentials file not found`
- **Fix:** Create `.credentials.json` in bot directory
- **Verify:** File exists at `F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot\.credentials.json`

**Error:** `Invalid token`
- **Fix:** Reset token in Discord Developer Portal
- **Update:** Copy new token to `.credentials.json`

**Error:** `Missing intents`
- **Fix:** Enable all required intents in Discord Developer Portal
- **Required:** Message Content, Server Members, Presence

### Google Sheets Errors

**Error:** `Spreadsheet not found`
- **Fix:** Share Google Sheet with service account email
- **Verify:** Service account has "Editor" access

**Error:** `API rate limit exceeded`
- **Fix:** Wait 60 seconds, then retry
- **Note:** Limit is 60 requests/minute

### Discord Errors

**Error:** `Missing permissions`
- **Fix:** Ensure bot has these permissions:
  - Manage Channels (for !league start)
  - Manage Roles (for Coach role)
  - Send Messages, Embed Links, etc.

**Error:** `Cannot send DM`
- **Fix:** User needs to enable DMs from server members
- **Setting:** Privacy & Safety → Allow direct messages from server members

---

## 📊 Monitoring

### What to Watch

1. **Console Output**
   - All commands logged
   - Errors displayed with tracebacks
   - Draft picks announced

2. **Google Sheets**
   - Teams sheet updates after picks
   - Draft_History logs all picks
   - Tera_Captains tracks designations

3. **Discord Server**
   - Commands respond within 1-2 seconds
   - Embeds display correctly
   - Coach channels created properly

---

## 🚀 Easy Launch Options

### Option 1: Desktop Shortcut (EASIEST)
1. Double-click `create_desktop_shortcut.bat`
2. A shortcut appears on your desktop
3. Double-click the desktop shortcut to start the bot!

### Option 2: Batch File
1. Double-click `run_bot.bat` in the bot folder
2. Bot starts automatically

### Option 3: Build Standalone EXE
1. Follow instructions in `BUILD_EXECUTABLE.md`
2. Creates `PokemonDraftBot.exe` that runs without Python

### Option 4: Command Line (Traditional)
```bash
cd "F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot"
python bot.py
```

---

## 🎯 Next Steps After Deployment

1. **Add Pokémon Data**
   - Populate "Pokemon" sheet with available Pokémon
   - Include: name, type1, type2, point_cost, stats
   - Minimum 50-100 Pokémon recommended

2. **Configure League Rules**
   - Update "Config" sheet:
     - max_tera_captains: 3
     - total_points: 120
     - min_pokemon: 10
     - max_pokemon: 12

3. **Test Full Draft Flow**
   - Start draft with 4+ people
   - Complete all picks
   - Run !league start
   - Verify channels created

4. **Enable Advanced Features**
   - Uncomment battle cog in bot.py
   - Uncomment stats cog in bot.py
   - Test match recording
   - Test standings updates

---

## 🆘 Support

### Documentation
- **Setup:** README.md
- **Quick Start:** QUICK_START.md (10-minute guide)
- **Commands:** All commands documented in cogs
- **Rules:** LEAGUE_RULES.md

### Resources
- Discord.py docs: https://discordpy.readthedocs.io/
- Google Sheets API: https://developers.google.com/sheets/api
- Smogon: https://www.smogon.com/
- Pikalytics: https://pikalytics.com/

---

## ✅ Deployment Complete!

Once you see the bot online in Discord and responding to commands, you're live! 🎉

**Remember:**
- Keep `.credentials.json` secure (never commit to git)
- Monitor console for errors
- Check Google Sheets for data updates
- Test thoroughly before league launch

**Have fun running your Pokémon Draft League!** 🎮
