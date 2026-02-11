@echo off
REM Setup Discord Bot Application
REM Opens Discord Developer Portal and guides through setup

title Pokemon Draft Bot - Discord Setup

echo ============================================================
echo  DISCORD BOT SETUP WIZARD
echo ============================================================
echo.
echo This wizard will help you:
echo  1. Login to Discord Developer Portal
echo  2. Select or Create an Application
echo  3. Configure the bot
echo  4. Get your bot token
echo  5. Generate invite link
echo.
pause

REM Step 1: Login to Discord
echo.
echo ============================================================
echo  STEP 1: Login to Discord Developer Portal
echo ============================================================
echo.
echo Opening Discord Developer Portal...
echo Please login with your Discord account.
echo.
pause

start https://discord.com/developers/applications

echo.
echo Logging in...
echo Press any key once you're logged in...
pause

REM Step 2: Select or Create Application
echo.
echo ============================================================
echo  STEP 2: Select or Create Application
echo ============================================================
echo.
echo You should now see your applications.
echo.
echo Choose one option:
echo.
echo   Option A: Create NEW Application
echo   ------------------------------------
echo   1. Click "New Application" (top right)
echo   2. Name: Pokemon Draft Bot
echo   3. Click "Create"
echo.
echo   Option B: Use EXISTING Application
echo   ------------------------------------
echo   1. Click on an existing application
echo   2. You can rename it in General Information
echo.
set /p app_choice="Create NEW or use EXISTING? (new/existing): "

if /i "%app_choice%"=="new" (
    echo.
    echo [INFO] Creating new application...
    echo Click "New Application" button and name it "Pokemon Draft Bot"
) else (
    echo.
    echo [INFO] Using existing application...
    echo Click on the application you want to use.
)

echo.
pause

REM Step 3: Navigate to Bot Section
echo.
echo ============================================================
echo  STEP 3: Configure Bot Settings
echo ============================================================
echo.
echo In your application, navigate to the "Bot" tab (left sidebar)
echo.
echo If you see "Add Bot" button:
echo   1. Click "Add Bot"
echo   2. Click "Yes, do it!"
echo.
echo If bot already exists:
echo   1. You're good to go!
echo.
pause

echo.
echo ============================================================
echo  STEP 4: Enable Required Intents
echo ============================================================
echo.
echo Scroll down to "Privileged Gateway Intents"
echo.
echo Enable these THREE intents:
echo   [x] PRESENCE INTENT
echo   [x] SERVER MEMBERS INTENT
echo   [x] MESSAGE CONTENT INTENT
echo.
echo Click "Save Changes" at the bottom!
echo.
pause

REM Step 4: Get Bot Token
echo.
echo ============================================================
echo  STEP 5: Get Your Bot Token
echo ============================================================
echo.
echo In the Bot tab, find the "TOKEN" section.
echo.
echo Click "Reset Token" (or "Copy" if you haven't reset it)
echo   - Click "Yes, do it!" to confirm
echo   - Click "Copy" to copy the token
echo.
echo IMPORTANT: Save this token somewhere safe!
echo You'll need it for the setup wizard.
echo.
echo WARNING: Never share your bot token publicly!
echo.
pause

REM Step 5: Generate Invite Link
echo.
echo ============================================================
echo  STEP 6: Generate Bot Invite Link
echo ============================================================
echo.
echo Navigate to "OAuth2" tab (left sidebar)
echo Then click "URL Generator" (sub-tab)
echo.
echo Step 1: Select SCOPES
echo   [x] bot
echo   [x] applications.commands
echo.
echo Step 2: Select BOT PERMISSIONS
echo   [x] Read Messages/View Channels
echo   [x] Send Messages
echo   [x] Send Messages in Threads
echo   [x] Embed Links
echo   [x] Attach Files
echo   [x] Read Message History
echo   [x] Add Reactions
echo   [x] Manage Channels
echo   [x] Manage Roles
echo   [x] Use External Emojis
echo.
echo Step 3: Copy the generated URL at the bottom
echo.
pause

echo.
echo ============================================================
echo  STEP 7: Invite Bot to Your Server
echo ============================================================
echo.
echo 1. Copy the generated URL from the previous step
echo 2. Paste it in your browser
echo 3. Select the Discord server you want to add the bot to
echo 4. Click "Authorize"
echo 5. Complete the CAPTCHA
echo.
echo Your bot should now appear in your server (offline until you run it)
echo.
pause

REM Step 6: Save Configuration
echo.
echo ============================================================
echo  STEP 8: Save Your Configuration
echo ============================================================
echo.
echo You've obtained:
echo   [x] Bot Token
echo   [x] Bot is invited to your server
echo   [x] Required intents are enabled
echo.
echo Now you need to:
echo   1. Copy your Bot Token
echo   2. Run the setup wizard: python setup_bot.py
echo      OR
echo      Run: setup_and_run.bat (choose option 1)
echo.
echo In the setup wizard, you'll need:
echo   - Discord Bot Token (you just copied it!)
echo   - Google Spreadsheet ID (we'll set this up next)
echo.

set /p open_setup="Open setup wizard now? (y/n): "

if /i "%open_setup%"=="y" (
    echo.
    echo Opening setup wizard...
    echo.
    echo Choose option 1 for "First-Time Setup"
    echo Then paste your Bot Token when prompted.
    echo.
    pause
    start "" "%~dp0setup_and_run.bat"
) else (
    echo.
    echo No problem! Run setup later with:
    echo   python setup_bot.py
    echo   OR
    echo   setup_and_run.bat
    echo.
)

echo.
echo ============================================================
echo  DISCORD BOT SETUP COMPLETE!
echo ============================================================
echo.
echo Summary of what you did:
echo   [x] Logged into Discord Developer Portal
echo   [x] Created/Selected application
echo   [x] Enabled required intents
echo   [x] Got bot token
echo   [x] Invited bot to server
echo.
echo Next steps:
echo   1. Set up Google Sheets (run SETUP_GOOGLE_SHEETS.bat)
echo   2. Run setup wizard (python setup_bot.py)
echo   3. Start the bot (python bot.py)
echo.
echo Need help? Check DEPLOYMENT_CHECKLIST.md
echo.
pause
