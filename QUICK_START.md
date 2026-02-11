# 🚀 Quick Start Guide - Pokémon Draft League Bot

Get your bot up and running in 10 minutes!

---

## ✅ Prerequisites Checklist

Before starting, make sure you have:
- [ ] Python 3.8+ installed
- [ ] Google account (for Google Sheets)
- [ ] Discord account (for bot creation)
- [ ] A Discord server where you have admin permissions

---

## 📦 Step 1: Install Dependencies (2 minutes)

Open terminal/command prompt in the bot directory and run:

```bash
cd "F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot"
pip install -r requirements.txt
```

**Expected output:** All packages install successfully ✅

**Verify installation:**
```bash
python test_imports.py
```

You should see `[OK] All imports successful!`

---

## 🔑 Step 2: Set Up Google Sheets API (5 minutes)

### 2.1 Enable Google Sheets API

1. Go to: https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Click "Enable APIs and Services"
4. Search for "Google Sheets API" → Enable it
5. Search for "Google Drive API" → Enable it

### 2.2 Create Service Account

1. Go to "Credentials" in left sidebar
2. Click "Create Credentials" → "Service Account"
3. Name it: `pokemon-draft-bot`
4. Click "Create and Continue"
5. Skip roles (optional) → Click "Done"

### 2.3 Download Credentials

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose JSON format → Click "Create"
5. **Save the downloaded JSON file as `.credentials.json` in your bot directory**

### 2.4 Create Google Sheet

1. Go to: https://sheets.google.com
2. Create a new blank spreadsheet
3. Name it: "Pokemon Draft League"
4. Copy the spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
   ```

### 2.5 Share Sheet with Bot

1. Open your Google Sheet
2. Click "Share" button (top right)
3. Open `.credentials.json` and find the `client_email` field
4. Paste that email into the Share dialog
5. Give "Editor" permissions
6. Click "Send"

---

## 🤖 Step 3: Set Up Discord Bot (3 minutes)

### 3.1 Create Discord Application

1. Go to: https://discord.com/developers/applications
2. Click "New Application"
3. Name it: "Pokemon Draft Bot"
4. Click "Create"

### 3.2 Create Bot User

1. Click "Bot" in left sidebar
2. Click "Add Bot" → "Yes, do it!"
3. **Copy the bot token** (Click "Reset Token" if needed)
4. ⚠️ **Keep this token secret!**

### 3.3 Enable Intents

Scroll down to "Privileged Gateway Intents" and enable:
- ✅ **Message Content Intent**
- ✅ **Server Members Intent**

Click "Save Changes"

### 3.4 Generate Invite Link

1. Click "OAuth2" → "URL Generator" in left sidebar
2. Select scopes:
   - ✅ `bot`
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Read Messages/View Channels
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Manage Channels
   - ✅ Manage Roles
4. Copy the generated URL
5. Open it in browser → Select your server → Authorize

---

## 📝 Step 4: Configure Credentials File

Open `.credentials.json` in a text editor. It should look like this:

```json
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "pokemon-draft-bot@....iam.gserviceaccount.com",
  ...
}
```

**Add these two fields at the top of the JSON:**

```json
{
  "discord_bot_token": "YOUR_DISCORD_BOT_TOKEN_HERE",
  "spreadsheet_id": "YOUR_GOOGLE_SHEET_ID_HERE",
  "type": "service_account",
  ...rest of the file...
}
```

**Example:**
```json
{
  "discord_bot_token": "MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.AbCdEf.GhIjKlMnOpQrStUvWxYz",
  "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
  "type": "service_account",
  "project_id": "pokemon-draft-123456",
  ...
}
```

**Save the file!**

---

## 📊 Step 5: Set Up Google Sheet Structure

### 5.1 Create Required Tabs

In your Google Sheet, create these tabs (in this order):

1. `Config`
2. `Pokemon`
3. `Teams`
4. `Tera_Captains`
5. `Draft_History`
6. `Matches`
7. `Standings`
8. `Stats`
9. `Trades`
10. `Archived_Teams`
11. `Error_Diagnostics`

**Tip:** Right-click on a tab → "Rename" to change the name

### 5.2 Set Up Config Tab

In the `Config` tab, add these headers and values:

| Key | Value |
|-----|-------|
| league_name | My Pokemon League |
| total_points | 120 |
| min_pokemon | 10 |
| max_pokemon | 12 |
| max_tera_captains | 3 |
| max_tera_points | 25 |

### 5.3 Set Up Pokemon Tab Headers

In the `Pokemon` tab, add this header row:

| Name | Tier | Type1 | Type2 | Point_Cost | HP | Attack | Defense | SpAttack | SpDefense | Speed |
|------|------|-------|-------|------------|----|----|-------|----------|-----------|-------|

**Example rows (add your own Pokémon):**

| Name | Tier | Type1 | Type2 | Point_Cost | HP | Attack | Defense | SpAttack | SpDefense | Speed |
|------|------|-------|-------|------------|----|----|-------|----------|-----------|-------|
| Pikachu | A | Electric | | 8 | 35 | 55 | 40 | 50 | 50 | 90 |
| Charizard | S | Fire | Flying | 15 | 78 | 84 | 78 | 109 | 85 | 100 |
| Garchomp | S | Dragon | Ground | 14 | 108 | 130 | 95 | 80 | 85 | 102 |

### 5.4 Set Up Other Tab Headers (Leave Data Blank!)

**Teams:**
| Player | Team_Name | Team_Logo | Pokemon_List | Total_Points_Used |
|--------|-----------|-----------|--------------|-------------------|

**Tera_Captains:**
| Player | Pokemon | Tera_Type | Point_Cost |
|--------|---------|-----------|------------|

**Draft_History:**
| Pick_Number | Player | Pokemon | Point_Cost | Timestamp |
|-------------|--------|---------|------------|-----------|

**Matches:**
| Week | Player1 | Player2 | Score | Winner | Kills | Deaths | Differential | Replay_Link |
|------|---------|---------|-------|--------|-------|--------|--------------|-------------|

**Standings:**
| Player | Wins | Losses | Points | Status |
|--------|------|--------|--------|--------|

**Stats:**
| Pokemon | Times_Drafted | Win_Rate | Times_Used |
|---------|---------------|----------|------------|

**Trades:**
| Week | Player1 | Pokemon1 | Player2 | Pokemon2 | Status | Timestamp |
|------|---------|----------|---------|----------|--------|-----------|

**Archived_Teams:**
| Archived_Date | Player | Team_Name | Team_Logo | Pokemon_List | Total_Points_Used |
|---------------|--------|-----------|-----------|--------------|-------------------|

**Error_Diagnostics:**
| Timestamp | Error_Type | Severity | Description | Affected_Data | Status | Auto_Fix_Attempted |
|-----------|------------|----------|-------------|---------------|--------|--------------------|

---

## 🎮 Step 6: Test the Bot!

### 6.1 Start the Bot

In terminal/command prompt:

```bash
python bot.py
```

**Expected output:**
```
🚀 Starting Pokemon Draft League Bot...
   Python version: 3.x.x
   Discord.py version: 2.x.x

✅ Connected to Google Sheets: Pokemon Draft League
✅ Loaded cog: cogs.league

================================================
🤖 Bot logged in as: Pokemon Draft Bot (ID: XXXXX)
📊 Connected to 1 server(s)
👥 Total members: X
⚡ Command prefix: !
================================================
✅ Pokemon Draft League Bot is ready!
   Use !help to see available commands
```

**If you see errors:**
- Check `.credentials.json` has correct token and spreadsheet ID
- Verify bot token is correct (no extra spaces)
- Ensure Google Sheet is shared with service account email

### 6.2 Test Basic Commands

In your Discord server, try these commands:

**1. Test Help:**
```
!help
```
Should show available commands ✅

**2. Test League Commands:**
```
!league
```
Should show league command categories ✅

**3. Initialize League (Admin Only):**
```
!init "Test League 2026"
```
Should create "Coach" role and show success message ✅

**4. Register as Coach:**
```
!register "Fire Fighters" https://i.imgur.com/example.png
```
Should assign you the Coach role ✅

**5. Test Logo Upload:**
```
!uploadlogo
(attach an image file)
```
Should show logo preview ✅

**6. Test Tera Captain Commands:**
```
!tera types
```
Should show all 19 valid Tera types with emojis ✅

```
!tera help
```
Should show Tera Captain command help ✅

---

## ✅ Success Checklist

After completing all steps, verify:

- [ ] Bot is online in Discord (green status)
- [ ] Bot responds to `!help`
- [ ] Bot responds to `!league`
- [ ] Google Sheet tabs are created and formatted
- [ ] Pokemon tab has sample data
- [ ] Bot can create "Coach" role with `!init`
- [ ] You can register with `!register`

**🎉 If all checks pass, your bot is ready!**

---

## 🐛 Troubleshooting

### Bot won't start
- **Error: "Invalid token"**
  - Double-check Discord bot token in `.credentials.json`
  - Make sure there are no extra spaces or quotes

- **Error: "Credentials file not found"**
  - Ensure `.credentials.json` is in the bot directory
  - Check the filename exactly (with the dot at the beginning)

### Bot can't access Google Sheets
- **Error: "Permission denied"**
  - Share the Google Sheet with the service account email
  - Give "Editor" permissions
  - Check spreadsheet_id is correct

### Commands don't work
- **Bot doesn't respond**
  - Check bot has "Read Messages" and "Send Messages" permissions
  - Verify Message Content Intent is enabled in Discord Developer Portal
  - Ensure bot is in the correct channel

- **"Missing permissions" error**
  - Bot needs "Manage Channels" and "Manage Roles" for full functionality
  - Re-invite bot with correct permissions using OAuth2 URL

### Can't upload logo
- **File type error**
  - Use PNG, JPG, JPEG, GIF, or WEBP format
  - File must be under 8MB

---

## 📚 Next Steps

Now that your bot is running:

1. **Add More Pokémon** - Fill out the Pokemon tab with all available Pokémon and their costs
2. **Invite Coaches** - Have other players register with `!register`
3. **Start a Draft** - Use `!draft start` to begin the draft process
4. **Set Tera Captains** - After drafting, use `!tera set <pokemon> <type>` to designate your 3 Tera Captains
5. **Read LEAGUE_RULES.md** - Full rules and command reference including detailed Tera Captain strategies

---

## 💡 Pro Tips

1. **Test on a Private Server First** - Don't test on your main league server
2. **Backup Your Sheet** - Make a copy of your Google Sheet regularly
3. **Keep Credentials Safe** - Never share `.credentials.json` or commit it to git
4. **Use Test Data** - Test with fake Pokémon and coaches before going live
5. **Check Bot Logs** - Watch the console output for errors and warnings

---

## 🆘 Need Help?

If you run into issues:
1. Check the console output for error messages
2. Verify all setup steps were completed
3. Review TESTING.md for detailed test cases
4. Check README.md for full documentation

---

**Ready to draft? Let's build that draft system next!** 🎮
