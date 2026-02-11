@echo off
REM Push Pokemon Draft League Bot to GitHub
REM Username: NoChillModeOnline

echo ============================================================
echo  PUSH TO GITHUB - NoChillModeOnline
echo ============================================================
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.
echo Repository: pokemon-draft-league-bot
echo Username: NoChillModeOnline
echo URL: https://github.com/NoChillModeOnline/pokemon-draft-league-bot
echo.

pause

echo.
echo [STEP 1] Adding GitHub remote...
git remote add origin https://github.com/NoChillModeOnline/pokemon-draft-league-bot.git

if errorlevel 1 (
    echo.
    echo Remote might already exist. Removing and re-adding...
    git remote remove origin
    git remote add origin https://github.com/NoChillModeOnline/pokemon-draft-league-bot.git
)

echo.
echo [STEP 2] Verifying remote...
git remote -v

echo.
echo [STEP 3] Pushing to GitHub...
echo This will push 13 commits and 54 files...
echo.
pause

git push -u origin master

if errorlevel 1 (
    echo.
    echo ============================================================
    echo  ERROR: Push failed!
    echo ============================================================
    echo.
    echo Common fixes:
    echo  1. Make sure you created the repository on GitHub first
    echo  2. Make sure you're authenticated (gh auth login)
    echo  3. Repository should be EMPTY on GitHub
    echo.
    pause
    exit /b 1
)

echo.
echo [STEP 4] Creating version tag...
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"
git push origin v1.0.0

echo.
echo ============================================================
echo  SUCCESS! Repository pushed to GitHub
echo ============================================================
echo.
echo Your repository is now live at:
echo https://github.com/NoChillModeOnline/pokemon-draft-league-bot
echo.
echo Next steps:
echo  1. Visit your repository on GitHub
echo  2. Add topics: discord-bot, pokemon, draft-league
echo  3. Create a release for v1.0.0
echo  4. Share with the community!
echo.
pause
