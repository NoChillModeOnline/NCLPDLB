@echo off
REM Push Pokemon Draft League Bot to GitHub
REM Username: NoChillModeOnline

title Pokemon Draft Bot - Push to GitHub

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

REM Check if setup was run
echo Pre-flight checks...
echo.

REM Check if repository exists on GitHub
set /p repo_created="Did you create the repository on GitHub? (y/n): "
if /i not "%repo_created%"=="y" (
    echo.
    echo [!] Repository not created yet!
    echo.
    echo Run SETUP_GITHUB_LOGIN.bat first to:
    echo   1. Login to GitHub
    echo   2. Create the repository
    echo   3. Set up authentication
    echo.
    set /p run_setup="Run setup now? (y/n): "
    if /i "%run_setup%"=="y" (
        start "" "%~dp0SETUP_GITHUB_LOGIN.bat"
        exit /b 0
    )
    echo.
    echo Please run SETUP_GITHUB_LOGIN.bat first!
    pause
    exit /b 1
)

REM Check authentication
echo.
echo Checking GitHub authentication...
gh auth status >nul 2>&1

if errorlevel 1 (
    echo.
    echo [!] Not authenticated with GitHub!
    echo.
    echo You need to authenticate. Choose a method:
    echo.
    echo   1. GitHub CLI (recommended)
    echo   2. I'll handle it manually
    echo.
    set /p auth_method="Choose (1 or 2): "

    if "%auth_method%"=="1" (
        echo.
        echo Checking if GitHub CLI is installed...
        gh --version >nul 2>&1

        if errorlevel 1 (
            echo.
            echo [!] GitHub CLI not installed!
            echo.
            echo Opening installation page...
            start https://cli.github.com/
            echo.
            echo After installing, run: gh auth login
            echo Then run this script again.
            pause
            exit /b 1
        )

        echo.
        echo Starting GitHub CLI authentication...
        echo.
        gh auth login

        if errorlevel 1 (
            echo.
            echo [X] Authentication failed!
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo [INFO] Manual authentication
        echo.
        echo You'll need a Personal Access Token.
        echo Opening GitHub token creation page...
        echo.
        echo When prompted for password, use your Personal Access Token.
        echo.
        start https://github.com/settings/tokens/new
        pause
    )
)

echo.
echo [OK] Ready to push!
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
echo This will push all commits and files...
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
    echo  1. Make sure repository exists on GitHub
    echo  2. Make sure you're authenticated
    echo  3. Repository should be EMPTY on GitHub
    echo.
    echo Try these commands:
    echo   gh auth login
    echo   git push -u origin master
    echo.
    pause
    exit /b 1
)

echo.
echo [STEP 4] Creating version tag...
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"
git push origin v1.0.0

if errorlevel 1 (
    echo.
    echo [!] Tag already exists or push failed
    echo This is okay if you already created the tag.
)

echo.
echo ============================================================
echo  SUCCESS! Repository pushed to GitHub
echo ============================================================
echo.
echo Your repository is now live at:
echo https://github.com/NoChillModeOnline/pokemon-draft-league-bot
echo.
echo Opening your repository in browser...
start https://github.com/NoChillModeOnline/pokemon-draft-league-bot

echo.
echo Next steps:
echo  1. Add topics: discord-bot, pokemon, draft-league
echo  2. Create a release for v1.0.0
echo  3. Share with the community!
echo.
pause
