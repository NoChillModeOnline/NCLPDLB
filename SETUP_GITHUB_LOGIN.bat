@echo off
REM Setup GitHub Authentication and Repository
REM Opens GitHub pages for user to login and create repository

title Pokemon Draft Bot - GitHub Setup

echo ============================================================
echo  GITHUB SETUP WIZARD
echo ============================================================
echo.
echo This wizard will help you:
echo  1. Login to GitHub
echo  2. Create the repository
echo  3. Link your local repository
echo.
echo Username: NoChillModeOnline
echo Repository: pokemon-draft-league-bot
echo.
pause

REM Step 1: GitHub Login
echo.
echo ============================================================
echo  STEP 1: Login to GitHub
echo ============================================================
echo.
echo Opening GitHub login page...
echo Please login to your GitHub account (NoChillModeOnline)
echo.
pause

start https://github.com/login

echo.
echo Waiting for you to login...
echo Press any key once you're logged in...
pause

REM Step 2: Create Repository
echo.
echo ============================================================
echo  STEP 2: Create Repository
echo ============================================================
echo.
echo Opening repository creation page...
echo.
echo Please configure:
echo   Repository name: pokemon-draft-league-bot
echo   Description: Complete Pokemon Draft League Discord Bot with web dashboard
echo   Visibility: Public (recommended)
echo
echo   IMPORTANT: Do NOT check "Initialize with README"
echo   IMPORTANT: License: Choose "MIT License" from dropdown
echo.
echo Then click "Create repository"
echo.
pause

start https://github.com/new

echo.
echo Creating repository...
echo Press any key once you've created the repository...
pause

REM Step 3: Authenticate Git
echo.
echo ============================================================
echo  STEP 3: Authenticate Git
echo ============================================================
echo.
echo Opening GitHub authentication page...
echo This will help you authenticate git commands.
echo.
echo Choose one of these methods:
echo   1. GitHub CLI (recommended) - type: gh auth login
echo   2. Personal Access Token
echo   3. SSH Key
echo.
pause

start https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

echo.
echo Would you like to use GitHub CLI for authentication?
echo If yes, we'll open the installation page.
echo.
set /p use_gh_cli="Use GitHub CLI? (y/n): "

if /i "%use_gh_cli%"=="y" (
    echo.
    echo Opening GitHub CLI installation page...
    start https://cli.github.com/
    echo.
    echo After installing GitHub CLI, run: gh auth login
    echo Then come back and run PUSH_TO_GITHUB.bat
    echo.
    pause
    exit /b 0
)

REM Step 4: Configure Git
echo.
echo ============================================================
echo  STEP 4: Configure Git Identity
echo ============================================================
echo.
echo Setting up git with your GitHub identity...
echo.

set /p git_name="Enter your name for Git commits (e.g., Your Name): "
set /p git_email="Enter your GitHub email: "

git config --global user.name "%git_name%"
git config --global user.email "%git_email%"

echo.
echo [OK] Git configured!
echo   Name: %git_name%
echo   Email: %git_email%
echo.

REM Step 5: Ready to Push
echo.
echo ============================================================
echo  STEP 5: Ready to Push
echo ============================================================
echo.
echo Your repository is created and you're authenticated!
echo.
echo Next step: Run PUSH_TO_GITHUB.bat to push your code.
echo.
echo Before you do, make sure:
echo   [x] You're logged into GitHub
echo   [x] Repository "pokemon-draft-league-bot" is created
echo   [x] Repository is EMPTY (no README initialized)
echo   [x] Git is authenticated (gh auth login OR personal access token)
echo.
echo Ready to push?
pause

echo.
echo Opening PUSH_TO_GITHUB.bat location...
explorer /select,"%~dp0PUSH_TO_GITHUB.bat"

echo.
echo ============================================================
echo  NEXT STEP
echo ============================================================
echo.
echo Double-click PUSH_TO_GITHUB.bat to push your code!
echo.
pause
