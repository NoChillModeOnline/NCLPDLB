@echo off
REM Complete Setup - Master Wizard
REM Guides through entire setup process

title Pokemon Draft Bot - Complete Setup Wizard

:MENU
cls
echo ============================================================
echo  POKEMON DRAFT LEAGUE BOT - COMPLETE SETUP
echo ============================================================
echo.
echo This wizard will guide you through:
echo   1. GitHub repository setup
echo   2. Discord bot configuration
echo   3. Bot credentials setup
echo   4. Pushing code to GitHub
echo.
echo Username: NoChillModeOnline
echo Repository: pokemon-draft-league-bot
echo.
echo ============================================================
echo  SETUP STEPS
echo ============================================================
echo.
echo  1. Setup GitHub (login, create repo, authenticate)
echo  2. Setup Discord Bot (create app, get token)
echo  3. Configure Bot Credentials (run setup wizard)
echo  4. Push Code to GitHub
echo  5. Start Bot
echo.
echo  0. Exit
echo.
echo ============================================================
set /p choice="Choose a step (1-5, 0 to exit): "

if "%choice%"=="1" goto GITHUB_SETUP
if "%choice%"=="2" goto DISCORD_SETUP
if "%choice%"=="3" goto BOT_SETUP
if "%choice%"=="4" goto PUSH_GITHUB
if "%choice%"=="5" goto START_BOT
if "%choice%"=="0" goto EXIT

echo Invalid choice!
pause
goto MENU

:GITHUB_SETUP
cls
echo ============================================================
echo  STEP 1: GitHub Setup
echo ============================================================
echo.
echo This will open the GitHub setup wizard.
echo.
echo The wizard will help you:
echo   - Login to GitHub
echo   - Create your repository
echo   - Set up authentication (GitHub CLI or Personal Access Token)
echo   - Configure git identity
echo.
pause

start "" "%~dp0SETUP_GITHUB_LOGIN.bat"

echo.
echo GitHub setup wizard opened!
echo Complete that wizard, then come back here.
echo.
pause
goto MENU

:DISCORD_SETUP
cls
echo ============================================================
echo  STEP 2: Discord Bot Setup
echo ============================================================
echo.
echo This will open the Discord setup wizard.
echo.
echo The wizard will help you:
echo   - Login to Discord Developer Portal
echo   - Create or select an application
echo   - Enable required intents
echo   - Get your bot token
echo   - Generate invite link and add bot to server
echo.
pause

start "" "%~dp0SETUP_DISCORD_BOT.bat"

echo.
echo Discord setup wizard opened!
echo Complete that wizard and save your bot token.
echo.
pause
goto MENU

:BOT_SETUP
cls
echo ============================================================
echo  STEP 3: Configure Bot Credentials
echo ============================================================
echo.
echo This will run the bot configuration wizard.
echo.
echo You will need:
echo   - Discord Bot Token (from Step 2)
echo   - Google Spreadsheet ID
echo   - Google Service Account JSON (optional)
echo.
echo Choose setup method:
echo   1. Interactive setup wizard (Python)
echo   2. All-in-one menu (Batch file)
echo.
set /p setup_method="Choose (1 or 2): "

if "%setup_method%"=="1" (
    echo.
    echo Starting Python setup wizard...
    python setup_bot.py
) else (
    echo.
    echo Starting all-in-one menu...
    start "" "%~dp0setup_and_run.bat"
    echo.
    echo Choose option 1 in the menu for "First-Time Setup"
)

echo.
pause
goto MENU

:PUSH_GITHUB
cls
echo ============================================================
echo  STEP 4: Push Code to GitHub
echo ============================================================
echo.
echo Before pushing, make sure you completed:
echo   [x] Step 1: GitHub Setup (repository created)
echo   [x] GitHub authentication (gh auth login)
echo.
set /p ready="Ready to push? (y/n): "

if /i not "%ready%"=="y" (
    echo.
    echo Please complete Step 1 first!
    pause
    goto MENU
)

echo.
echo Starting push process...
echo.

start "" "%~dp0PUSH_TO_GITHUB.bat"

echo.
echo Push script opened!
echo Follow the prompts to push your code.
echo.
pause
goto MENU

:START_BOT
cls
echo ============================================================
echo  STEP 5: Start Bot
echo ============================================================
echo.
echo Before starting, make sure you completed:
echo   [x] Step 2: Discord Bot Setup
echo   [x] Step 3: Bot Credentials Configuration
echo.
echo What would you like to start?
echo.
echo   1. Discord Bot only
echo   2. Web Dashboard only
echo   3. Both (Discord Bot + Web Dashboard)
echo.
set /p start_choice="Choose (1-3): "

if "%start_choice%"=="1" (
    echo.
    echo Starting Discord Bot...
    start "Discord Bot" cmd /k python bot.py
) else if "%start_choice%"=="2" (
    echo.
    echo Starting Web Dashboard...
    start "Web Dashboard" cmd /k python web_server.py
    echo.
    echo Dashboard will be at: http://localhost:5000
) else if "%start_choice%"=="3" (
    echo.
    echo Starting both services...
    start "Discord Bot" cmd /k python bot.py
    start "Web Dashboard" cmd /k python web_server.py
    echo.
    echo Dashboard will be at: http://localhost:5000
) else (
    echo Invalid choice!
    pause
    goto START_BOT
)

echo.
echo Services started!
echo.
pause
goto MENU

:EXIT
cls
echo.
echo ============================================================
echo  SETUP WIZARD CLOSED
echo ============================================================
echo.
echo Thank you for setting up Pokemon Draft League Bot!
echo.
echo Quick reference:
echo   Start bot: python bot.py
echo   Start web: python web_server.py
echo   GitHub: https://github.com/NoChillModeOnline/pokemon-draft-league-bot
echo.
echo Documentation:
echo   Quick Start: QUICK_START.md
echo   Full Deployment: DEPLOYMENT_CHECKLIST.md
echo   Web Dashboard: WEB_DASHBOARD_GUIDE.md
echo.
pause
exit /b 0
