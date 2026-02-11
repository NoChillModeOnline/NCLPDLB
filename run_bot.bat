@echo off
REM Pokemon Draft League Bot Launcher
REM This batch file starts the Discord bot

title Pokemon Draft League Bot

echo.
echo ======================================
echo  Pokemon Draft League Bot
echo ======================================
echo.
echo Starting bot...
echo.

cd /d "%~dp0"

python bot.py

if errorlevel 1 (
    echo.
    echo ======================================
    echo  ERROR: Bot crashed or failed to start
    echo ======================================
    echo.
    echo Check the error messages above.
    echo.
    pause
)
