@echo off
REM Creates a desktop shortcut for the Pokemon Draft Bot

setlocal

REM Get the current directory
set "BOT_DIR=%~dp0"
set "TARGET=%BOT_DIR%run_bot.bat"
set "SHORTCUT=%USERPROFILE%\Desktop\Pokemon Draft Bot.lnk"

echo.
echo ========================================
echo  Creating Desktop Shortcut
echo ========================================
echo.
echo Creating shortcut to:
echo %TARGET%
echo.

REM Create shortcut using PowerShell
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%SHORTCUT%'); $SC.TargetPath = '%TARGET%'; $SC.WorkingDirectory = '%BOT_DIR%'; $SC.Description = 'Pokemon Draft League Discord Bot'; $SC.Save()"

if exist "%SHORTCUT%" (
    echo.
    echo ========================================
    echo  SUCCESS!
    echo ========================================
    echo.
    echo Desktop shortcut created:
    echo %SHORTCUT%
    echo.
    echo You can now double-click the shortcut
    echo on your desktop to start the bot!
    echo.
) else (
    echo.
    echo ========================================
    echo  ERROR!
    echo ========================================
    echo.
    echo Failed to create desktop shortcut.
    echo Please create it manually.
    echo.
)

pause
