# 🧪 Testing Guide - Pokémon Draft League Bot

This document provides a comprehensive testing plan for the bot before deployment.

---

## 📋 Pre-Testing Checklist

### ✅ Required Setup

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] Service account created with credentials downloaded
- [ ] Discord bot created in Developer Portal
- [ ] Bot invited to test Discord server
- [ ] `.credentials.json` file created with valid credentials
- [ ] Google Sheet created with all required tabs
- [ ] Service account has Editor permissions on the sheet

---

## 🔍 Phase 1: Basic Connectivity Tests

### Test 1.1: Bot Starts Successfully

**Command:**
```bash
python bot.py
```

**Expected Output:**
```
🚀 Starting Pokemon Draft League Bot...
   Python version: 3.x.x
   Discord.py version: 2.x.x

✅ Connected to Google Sheets: [Your Sheet Name]
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

**Success Criteria:**
- ✅ No errors during startup
- ✅ Bot shows as online in Discord
- ✅ Google Sheets connection successful
- ✅ League cog loads without errors

---

### Test 1.2: Help Command

**Command in Discord:**
```
!help
```

**Expected Output:**
- Bot responds with command list
- No errors or timeout

**Success Criteria:**
- ✅ Bot responds within 3 seconds
- ✅ Shows available commands

---

### Test 1.3: League Help Command

**Command in Discord:**
```
!league
```

**Expected Output:**
- Embed with league commands organized by category:
  - 📋 Setup Commands
  - 👥 Coach Management
  - 🔧 Maintenance

**Success Criteria:**
- ✅ Embed displays correctly
- ✅ All commands listed
- ✅ Formatting is clean and readable

---

## 🎮 Phase 2: League Initialization Tests

### Test 2.1: League Init (Admin Only)

**Prerequisites:**
- User has Administrator permission in Discord

**Command:**
```
!init "Test League 2026"
```

**Expected Output:**
```
✅ League Initialized!
**Test League 2026** has been created!

📝 Next Steps
1. Coaches: Use `!league register <team_name> <logo_url>` to join
2. Complete the draft with `!draft start`
3. Admin: Start season with `!league start`
```

**Success Criteria:**
- ✅ Embed displays correctly
- ✅ "Coach" role created in Discord
- ✅ No errors

**Verify:**
- Check Discord roles - "Coach" role should exist

---

### Test 2.2: League Init (Non-Admin)

**Prerequisites:**
- User does NOT have Administrator permission

**Command:**
```
!init "Test League"
```

**Expected Output:**
```
❌ You don't have permission to use this command!
Required: administrator
```

**Success Criteria:**
- ✅ Permission denied message
- ✅ Command doesn't execute

---

### Test 2.3: Coach Registration

**Prerequisites:**
- League initialized
- User does NOT have Coach role yet

**Command:**
```
!register "Fire Fighters" https://i.imgur.com/example.png
```

**Expected Output:**
```
✅ Coach Registered!
@Username joined as **Fire Fighters**

📝 Next Steps
Wait for the draft to begin!
```

**Success Criteria:**
- ✅ Embed displays with team logo thumbnail
- ✅ User receives "Coach" role
- ✅ No errors

**Verify:**
- Check user has "Coach" role in Discord

---

### Test 2.4: Logo Upload Command

**Prerequisites:**
- User has "Coach" role

**Command:**
```
!uploadlogo
(attach a PNG/JPG image)
```

**Expected Output:**
```
✅ Team Logo Uploaded!
Logo updated for @Username

[Image preview displayed]

Logo URL
[View Full Size](URL)
```

**Success Criteria:**
- ✅ Image attachment validated
- ✅ Logo preview displays in embed
- ✅ URL is accessible
- ✅ Warning shows for Sheet update (not yet implemented)

---

### Test 2.5: Logo Upload Without Coach Role

**Prerequisites:**
- User does NOT have "Coach" role

**Command:**
```
!uploadlogo
```

**Expected Output:**
```
❌ You must be registered as a coach first! Use `!league register`
```

**Success Criteria:**
- ✅ Error message displays
- ✅ Command doesn't execute

---

### Test 2.6: Logo Upload Without Attachment

**Prerequisites:**
- User has "Coach" role

**Command:**
```
!uploadlogo
(NO attachment)
```

**Expected Output:**
```
❌ Please attach an image file when using this command!
Example: Use `!league uploadlogo` and attach your team logo image.
```

**Success Criteria:**
- ✅ Error message displays
- ✅ Instructions provided

---

### Test 2.7: Logo Upload Invalid File Type

**Prerequisites:**
- User has "Coach" role

**Command:**
```
!uploadlogo
(attach a .txt or .pdf file)
```

**Expected Output:**
```
❌ Invalid file type! Please upload an image file.
Supported formats: PNG, JPG, JPEG, GIF, WEBP
```

**Success Criteria:**
- ✅ File validation works
- ✅ Supported formats listed

---

## 🚀 Phase 3: Season Start Tests

### Test 3.1: Start League Before Draft

**Prerequisites:**
- League initialized
- Coaches registered
- NO draft completed (Teams sheet is empty or incomplete)

**Command:**
```
!start
```

**Expected Output:**
```
❌ Cannot Start Season
Some teams don't have complete rosters!

Incomplete Teams
- Username1
- Username2

Required
Minimum 10 Pokémon per team
```

**Success Criteria:**
- ✅ Validation prevents starting
- ✅ Lists incomplete teams
- ✅ Clear error message

---

### Test 3.2: Start League After Draft (Simulated)

**Prerequisites:**
- League initialized
- Coaches registered
- Teams sheet manually filled with 10+ Pokémon per team (for testing)

**Steps:**
1. Manually add test data to Teams sheet:
   - Player: Username1
   - Team_Name: Fire Fighters
   - Pokemon_List: Pikachu, Charizard, Garchomp, Rotom, Talonflame, Marowak, Blastoise, Venusaur, Snorlax, Gengar
   - Total_Points_Used: 100

2. Run command:
```
!start
```

**Expected Output:**
```
🚀 Starting league season... Validating rosters...
✅ All rosters validated! Creating coach channels...

🎮 League Season Started! 🎮
Created 1 coach channels!

Next Steps
• Check your private channel
• Review your roster
• Prepare for Week 1 battles!
```

**Success Criteria:**
- ✅ Validation passes
- ✅ Category created: `⌜🎮⌟ ᴅʀᴀꜰᴛ ʟᴇᴀɢᴜᴇ ᴄᴏᴀᴄʜᴇꜱ ⌜🎮⌟`
- ✅ Private channel created: `🏆┃ꜰɪʀᴇ-ꜰɪɢʜᴛᴇʀꜱ`
- ✅ Channel has correct permissions (only coach + admins can see)
- ✅ Welcome embed posted in channel with roster

---

### Test 3.3: Verify Coach Channel Content

**Prerequisites:**
- Season started (Test 3.2 passed)

**Action:**
- Navigate to the coach's private channel

**Expected Content:**
```
🏆 Fire Fighters 🏆
Welcome, Coach @Username1!

📋 Roster (10 Pokémon - 100/120 pts)
1. **Pikachu** (Electric) - 8 pts
2. **Charizard** (Fire/Flying) - 15 pts
[... rest of roster ...]

⚡ Tera Captains
(if any are set)

Good luck this season! 🎮
```

**Success Criteria:**
- ✅ Team logo displays as thumbnail
- ✅ All Pokémon listed with types and costs
- ✅ Total points calculated correctly
- ✅ Tera Captains section shows (if any)
- ✅ Formatting is clean and professional

---

## 👥 Phase 4: Coach Management Tests

### Test 4.1: Add Coach

**Prerequisites:**
- League started
- User is NOT a coach yet
- Teams sheet has data for this user

**Steps:**
1. Manually add test data to Teams sheet for @NewCoach
2. Run command:
```
!addcoach @NewCoach
```

**Expected Output:**
```
🔍 Looking for NewCoach's data in Google Sheets...
✅ Assigned Coach role to @NewCoach
📝 Creating private channel for Their Team Name...

🎉 New Coach Joined!
Welcome @NewCoach to the league!

Team: Their Team Name
Pokémon: 10

✅ @NewCoach Your private channel is ready: #🏆┃their-team-name
```

**Success Criteria:**
- ✅ User receives Coach role
- ✅ Private channel created
- ✅ Welcome embed posted
- ✅ Announcement in main channel

---

### Test 4.2: Add Coach Without Sheet Data

**Prerequisites:**
- User is NOT a coach
- Teams sheet does NOT have data for this user

**Command:**
```
!addcoach @UserWithoutData
```

**Expected Output:**
```
❌ Team Data Not Found
Could not find team data for UserWithoutData

Please Add Their Data First
**Required sheets:**
• Teams: Player, Team_Name, Team_Logo, Pokemon_List
• Draft_History: Their draft picks
• Tera_Captains: Their Tera Captain choices
```

**Success Criteria:**
- ✅ Error message displays
- ✅ Instructions provided
- ✅ No changes made to Discord

---

### Test 4.3: Remove Coach (Full Flow)

**Prerequisites:**
- Coach exists with channel and data

**Command:**
```
!removecoach @Coach
```

**Expected Output (Step 1 - Confirmation):**
```
⚠️ Remove Coach Confirmation
Are you sure you want to remove @Coach (Fire Fighters)?

✅ What will be preserved:
• Match history (kills, deaths, +/-)
• Draft history
• Standings record (marked inactive)

❌ What will be removed:
• Private channel
• Coach role
• Active team data (archived first)

Reply with 'confirm' to proceed or 'cancel' to abort
```

**Action:**
- Type: `confirm`

**Expected Output (Step 2 - Execution):**
```
🗑️ Removing coach @Coach...
✅ Team data archived
✅ Marked as inactive in standings
✅ Cleared Tera Captain data
✅ Deleted private channel
✅ Removed Coach role

👋 Coach Removed
@Coach (Fire Fighters) has been removed from the league.

Historical Data
All match history and stats have been preserved.
```

**Success Criteria:**
- ✅ Confirmation required
- ✅ Data archived to Archived_Teams sheet
- ✅ Standings marked inactive (not deleted)
- ✅ Tera Captains cleared
- ✅ Channel deleted
- ✅ Role removed
- ✅ Clear confirmation at each step

**Verify:**
- Check Archived_Teams sheet - should have entry
- Check Standings sheet - player marked "(Inactive)"
- Check Discord - channel deleted, role removed

---

### Test 4.4: Remove Coach Timeout

**Prerequisites:**
- Coach exists

**Command:**
```
!removecoach @Coach
```

**Action:**
- Wait 30+ seconds without responding

**Expected Output:**
```
❌ Timed out. Coach removal cancelled.
```

**Success Criteria:**
- ✅ Timeout after 30 seconds
- ✅ No changes made
- ✅ Clear cancellation message

---

### Test 4.5: Remove Coach Cancel

**Prerequisites:**
- Coach exists

**Command:**
```
!removecoach @Coach
```

**Action:**
- Type: `cancel` (or anything except "confirm")

**Expected Output:**
```
❌ Coach removal cancelled.
```

**Success Criteria:**
- ✅ Cancellation works
- ✅ No changes made

---

## 🔍 Phase 5: Error Diagnostics Tests

### Test 5.1: Diagnose Clean Data

**Prerequisites:**
- Google Sheet has valid, clean data

**Command:**
```
!diagnose
```

**Expected Output:**
```
🔍 Running error diagnostics... This may take a moment.

📊 Diagnostic Results

Total Errors Found
**0**

✅ All Clear!
No errors detected in your league data.
```

**Success Criteria:**
- ✅ Diagnostic completes without errors
- ✅ Clean data confirmed
- ✅ Embed displays correctly

---

### Test 5.2: Diagnose With Errors (Simulated)

**Prerequisites:**
- Manually add invalid data to test errors:
  - Teams sheet: Add team with 5 Pokémon (too few)
  - Tera_Captains sheet: Add Tera Captain with 15 point cost (too expensive)

**Command:**
```
!diagnose
```

**Expected Output:**
```
🔍 Running error diagnostics... This may take a moment.

📊 Diagnostic Results

Total Errors Found
**2**

Severity Breakdown
🚨 Critical: 1
⚠️ High: 1

Auto-Fixable
**0**

📝 Details
Check the `Error_Diagnostics` sheet in Google Sheets for full details.
```

**Success Criteria:**
- ✅ Errors detected correctly
- ✅ Severity breakdown shows
- ✅ Error_Diagnostics sheet populated with details
- ✅ Embed color changes to warning (orange)

**Verify:**
- Check Error_Diagnostics sheet for logged errors

---

## 🗑️ Phase 6: League Reset Tests

### Test 6.1: League Reset (Full Flow)

**Prerequisites:**
- League is active with channels and coaches

**Command:**
```
!reset
```

**Expected Output (Step 1 - Confirmation):**
```
🚨 LEAGUE RESET WARNING 🚨
This will **DELETE ALL LEAGUE DATA**!

What will be deleted:
• All draft picks
• All team rosters
• All Tera Captains
• All coach channels
• All Coach roles
• Match history (if implemented)
• Standings (if implemented)

⚠️ THIS CANNOT BE UNDONE!
Reply with `DELETE EVERYTHING` to proceed or `cancel` to abort
```

**Action:**
- Type: `DELETE EVERYTHING` (exactly)

**Expected Output (Step 2 - Execution):**
```
🗑️ Resetting league... This will take a moment.
✅ Deleted all coach channels
✅ Removed all Coach roles
⚠️ Sheet data deletion not yet implemented

✅ League Reset Complete
The league has been reset. Use `!league init` to start a new season.
```

**Success Criteria:**
- ✅ Requires exact phrase "DELETE EVERYTHING"
- ✅ Category and all channels deleted
- ✅ All Coach roles removed
- ✅ Clear warnings throughout

**Verify:**
- Check Discord - category and channels deleted
- Check roles - Coach role deleted

---

### Test 6.2: League Reset Cancel

**Prerequisites:**
- League is active

**Command:**
```
!reset
```

**Action:**
- Type: `cancel` (or anything except "DELETE EVERYTHING")

**Expected Output:**
```
❌ League reset cancelled.
```

**Success Criteria:**
- ✅ Cancellation works
- ✅ No changes made

---

## 🔧 Phase 7: Error Handling Tests

### Test 7.1: Invalid Command

**Command:**
```
!invalidcommand
```

**Expected Output:**
- No response (CommandNotFound is silenced)

**Success Criteria:**
- ✅ Bot doesn't spam error messages
- ✅ Graceful failure

---

### Test 7.2: Missing Required Argument

**Command:**
```
!init
(no league name provided)
```

**Expected Output:**
```
❌ Missing required argument: `league_name`
Use `!help init` for usage info.
```

**Success Criteria:**
- ✅ Clear error message
- ✅ Helpful hint provided

---

### Test 7.3: Google Sheets Connection Failure

**Prerequisites:**
- Temporarily break Google Sheets connection (wrong spreadsheet ID in .credentials.json)

**Action:**
- Restart bot

**Expected Output:**
```
❌ Error connecting to Google Sheets: [error details]
```

**Success Criteria:**
- ✅ Clear error message during startup
- ✅ Bot stops gracefully (doesn't crash)

**Cleanup:**
- Restore correct spreadsheet ID

---

### Test 7.4: Discord Permission Missing

**Prerequisites:**
- Remove "Manage Channels" permission from bot

**Command:**
```
!start
```

**Expected Output:**
```
❌ I don't have the required permissions!
I need: manage_channels
```

**Success Criteria:**
- ✅ Permission check works
- ✅ Clear error message

**Cleanup:**
- Restore bot permissions

---

## 📊 Testing Results Template

### Test Session: [Date]

**Environment:**
- Python Version: ___________
- Discord.py Version: ___________
- OS: ___________

**Test Results:**

| Phase | Test | Status | Notes |
|-------|------|--------|-------|
| 1.1 | Bot Starts | ⬜ Pass / ❌ Fail | |
| 1.2 | Help Command | ⬜ Pass / ❌ Fail | |
| 1.3 | League Help | ⬜ Pass / ❌ Fail | |
| 2.1 | League Init | ⬜ Pass / ❌ Fail | |
| 2.2 | Init Non-Admin | ⬜ Pass / ❌ Fail | |
| 2.3 | Coach Registration | ⬜ Pass / ❌ Fail | |
| 2.4 | Logo Upload | ⬜ Pass / ❌ Fail | |
| 2.5 | Logo No Role | ⬜ Pass / ❌ Fail | |
| 2.6 | Logo No Attachment | ⬜ Pass / ❌ Fail | |
| 2.7 | Logo Invalid File | ⬜ Pass / ❌ Fail | |
| 3.1 | Start Before Draft | ⬜ Pass / ❌ Fail | |
| 3.2 | Start After Draft | ⬜ Pass / ❌ Fail | |
| 3.3 | Channel Content | ⬜ Pass / ❌ Fail | |
| 4.1 | Add Coach | ⬜ Pass / ❌ Fail | |
| 4.2 | Add Coach No Data | ⬜ Pass / ❌ Fail | |
| 4.3 | Remove Coach | ⬜ Pass / ❌ Fail | |
| 4.4 | Remove Timeout | ⬜ Pass / ❌ Fail | |
| 4.5 | Remove Cancel | ⬜ Pass / ❌ Fail | |
| 5.1 | Diagnose Clean | ⬜ Pass / ❌ Fail | |
| 5.2 | Diagnose Errors | ⬜ Pass / ❌ Fail | |
| 6.1 | League Reset | ⬜ Pass / ❌ Fail | |
| 6.2 | Reset Cancel | ⬜ Pass / ❌ Fail | |
| 7.1 | Invalid Command | ⬜ Pass / ❌ Fail | |
| 7.2 | Missing Argument | ⬜ Pass / ❌ Fail | |
| 7.3 | Sheets Failure | ⬜ Pass / ❌ Fail | |
| 7.4 | Permission Missing | ⬜ Pass / ❌ Fail | |

**Overall Status:** ⬜ All Pass / ⚠️ Some Failures / ❌ Major Issues

**Issues Found:**
1. ___________________________________________
2. ___________________________________________
3. ___________________________________________

**Notes:**
___________________________________________
___________________________________________
___________________________________________

---

## ✅ Pre-Draft Implementation Checklist

Before implementing the draft cog, ensure:

- [ ] All Phase 1 tests pass (Basic Connectivity)
- [ ] All Phase 2 tests pass (League Initialization)
- [ ] All Phase 3 tests pass (Season Start)
- [ ] All Phase 4 tests pass (Coach Management)
- [ ] All Phase 5 tests pass (Error Diagnostics)
- [ ] All Phase 6 tests pass (League Reset)
- [ ] All Phase 7 tests pass (Error Handling)
- [ ] No critical bugs found
- [ ] Google Sheets integration working correctly
- [ ] Discord automation working correctly
- [ ] All edge cases handled gracefully

**Status:** ⬜ Ready for Draft Implementation / ❌ Issues Need Resolution

---

*Last Updated: [Date]*
