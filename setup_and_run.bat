@echo off
REM Pokemon Draft League Bot - Setup and Run Script

title Pokemon Draft League Bot - Setup

:MENU
cls
echo ========================================
echo  Pokemon Draft League Bot
echo ========================================
echo.
echo What would you like to do?
echo.
echo 1. First-Time Setup (Configure credentials)
echo 2. Run Discord Bot
echo 3. Run Web Dashboard
echo 4. Run Both (Bot + Dashboard)
echo 5. Install Dependencies
echo 6. Test Connection
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto SETUP
if "%choice%"=="2" goto RUN_BOT
if "%choice%"=="3" goto RUN_WEB
if "%choice%"=="4" goto RUN_BOTH
if "%choice%"=="5" goto INSTALL
if "%choice%"=="6" goto TEST
if "%choice%"=="7" goto EXIT

echo Invalid choice. Please try again.
pause
goto MENU

:SETUP
cls
echo ========================================
echo  First-Time Setup
echo ========================================
echo.
echo This will guide you through setting up:
echo  - Discord bot token
echo  - Google Sheets credentials
echo  - Configuration file
echo.
pause

python setup_bot.py

echo.
echo ========================================
pause
goto MENU

:RUN_BOT
cls
echo ========================================
echo  Starting Discord Bot
echo ========================================
echo.

REM Check if credentials exist
if not exist .credentials.json (
    echo ERROR: .credentials.json not found!
    echo.
    echo Please run First-Time Setup first.
    echo.
    pause
    goto MENU
)

echo Starting Pokemon Draft League Bot...
echo.
echo Press Ctrl+C to stop the bot.
echo.

python bot.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo  ERROR: Bot crashed or failed to start
    echo ========================================
    echo.
    pause
)
goto MENU

:RUN_WEB
cls
echo ========================================
echo  Starting Web Dashboard
echo ========================================
echo.

REM Check if credentials exist
if not exist .credentials.json (
    echo ERROR: .credentials.json not found!
    echo.
    echo Please run First-Time Setup first.
    echo.
    pause
    goto MENU
)

echo Starting Web Dashboard (Frontend)...
echo.
echo Features:
echo  - Real-time league statistics
echo  - Team rosters and analysis
echo  - Draft progress monitoring
echo  - REST API for integrations
echo.
echo Dashboard will be available at:
echo   http://localhost:5000
echo.
echo See FRONTEND_SETUP.md for more options!
echo.
echo Press Ctrl+C to stop the server.
echo.

python web_server.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo  ERROR: Web server crashed
    echo ========================================
    echo.
    pause
)
goto MENU

:RUN_BOTH
cls
echo ========================================
echo  Starting Bot + Dashboard
echo ========================================
echo.

REM Check if credentials exist
if not exist .credentials.json (
    echo ERROR: .credentials.json not found!
    echo.
    echo Please run First-Time Setup first.
    echo.
    pause
    goto MENU
)

echo Starting both services...
echo.
echo This will open two windows:
echo  1. Discord Bot (backend)
echo  2. Web Dashboard (frontend at http://localhost:5000)
echo.
echo Frontend Features:
echo  - Real-time dashboard
echo  - Team management interface
echo  - Draft progress viewer
echo  - REST API endpoints
echo.
echo See FRONTEND_SETUP.md for customization!
echo.
pause

start "Discord Bot" cmd /k python bot.py
start "Web Dashboard" cmd /k python web_server.py

echo.
echo Both services started in separate windows!
echo.
pause
goto MENU

:INSTALL
cls
echo ========================================
echo  Installing Dependencies
echo ========================================
echo.
echo Installing required Python packages...
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    pause
    goto MENU
)

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
pause
goto MENU

:TEST
cls
echo ========================================
echo  Testing Connection
echo ========================================
echo.

if not exist .credentials.json (
    echo ERROR: .credentials.json not found!
    echo.
    echo Please run First-Time Setup first.
    echo.
    pause
    goto MENU
)

echo Running test suite...
echo.

python run_all_tests.py

echo.
pause
goto MENU

:EXIT
cls
echo.
echo Thanks for using Pokemon Draft League Bot!
echo.
echo To run the bot later:
echo  - Use this script again, OR
echo  - Double-click run_bot.bat, OR
echo  - Run: python bot.py
echo.
pause
exit
