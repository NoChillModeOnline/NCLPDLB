# 🚀 GitHub Setup - Quick Start Guide

**Easy setup for hosting your Pokemon Draft League Bot on GitHub (Private Repository)**

---

## ⚡ Quick Setup (5 Minutes)

### Option 1: Use the Interactive Setup Wizard (Recommended)

The easiest way - just double-click a file!

1. **Open:** `COMPLETE_SETUP.bat` (or `SETUP_GITHUB_LOGIN.bat`)
2. **Follow the wizard** - it opens everything you need
3. **Done!** Your code is on GitHub

### Option 2: Manual Setup (Follow Steps Below)

Use this if you prefer more control or are on Mac/Linux.

---

## 📋 Step-by-Step Manual Setup

### Step 1: Create Your GitHub Account (If Needed)

1. Go to https://github.com/join
2. Sign up for free
3. Verify your email

---

### Step 2: Create a Private Repository

**Via GitHub Website:**

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `pokemon-draft-league-bot` (or any name you prefer)
   - **Description:** "My Pokemon Draft League Discord Bot"
   - **Visibility:** ✅ **Private** (keeps your code and credentials hidden)
   - **DO NOT** check "Initialize with README" (we already have one)
3. Click **"Create repository"**

**Why Private?**
- ✅ Keeps your bot configuration private
- ✅ Protects your setup from public access
- ✅ Free for unlimited private repositories
- ✅ You can always make it public later if desired

---

### Step 3: Connect Your Local Code to GitHub

**Windows Users:**

Open PowerShell or Command Prompt in your bot folder:

```bash
cd "F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot"

# Add GitHub as your remote repository
git remote add origin https://github.com/YOUR_USERNAME/pokemon-draft-league-bot.git

# Push your code to GitHub
git push -u origin master
```

**Mac/Linux Users:**

```bash
cd /path/to/pokemon-draft-bot

# Add GitHub as your remote repository
git remote add origin https://github.com/YOUR_USERNAME/pokemon-draft-league-bot.git

# Push your code to GitHub
git push -u origin master
```

**⚠️ Important:** Replace `YOUR_USERNAME` with your actual GitHub username!

---

### Step 4: Authenticate (First Time Only)

When you push for the first time, GitHub will ask you to log in.

**Option A: GitHub CLI (Recommended)**

```bash
# Install GitHub CLI: https://cli.github.com/
gh auth login
```

**Option B: Personal Access Token**

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a name: "Pokemon Bot"
4. Select scopes: ✅ `repo` (full control)
5. Click **"Generate token"**
6. Copy the token (you'll only see it once!)
7. Use it as your password when git prompts you

---

### Step 5: Verify Your Upload

1. Go to https://github.com/YOUR_USERNAME/pokemon-draft-league-bot
2. You should see:
   - ✅ Your README displayed
   - ✅ All your code files
   - ✅ Documentation folder
   - ✅ 🔒 **Private** label (repository is hidden from others)

---

## 🔒 Privacy & Security

### What's Private?

When your repository is **Private**:
- ✅ Only you can see the code
- ✅ Only people you invite can access it
- ✅ Your bot tokens stay hidden
- ✅ Your Google Sheets ID stays hidden

### What About .credentials.json?

Don't worry! Your `.credentials.json` file is **automatically excluded** by `.gitignore`:

```gitignore
# Sensitive files (NEVER pushed to GitHub)
.credentials.json
.env
*.env
service-account.json
```

**These files will NEVER be uploaded to GitHub!** ✅

---

## 👥 Sharing Your Bot (Optional)

### Invite Collaborators

To let others help develop your bot:

1. Go to your repository on GitHub
2. Click **Settings** → **Collaborators**
3. Click **"Add people"**
4. Enter their GitHub username
5. They'll get an email invitation

### Make Repository Public (If Desired)

Want to share with everyone?

1. Go to **Settings** → **Danger Zone**
2. Click **"Change visibility"**
3. Choose **"Make public"**
4. Type the repository name to confirm

**⚠️ Before making public:**
- ✅ Double-check `.credentials.json` is in `.gitignore`
- ✅ Remove any API keys from code
- ✅ Remove any sensitive information

---

## 🔄 Keeping Your Repository Updated

### After Making Changes

```bash
# Stage all changes
git add -A

# Commit with a descriptive message
git commit -m "Add new feature"

# Push to GitHub
git push origin master
```

### Pull Latest Changes (From Another Computer)

```bash
# Download latest version
git pull origin master
```

---

## 📱 Using GitHub on Multiple Computers

### Computer 1 (Initial Setup)
Already done! Your code is on GitHub.

### Computer 2 (Clone Repository)

```bash
# Clone your private repository
git clone https://github.com/YOUR_USERNAME/pokemon-draft-league-bot.git
cd pokemon-draft-league-bot

# Install dependencies
pip install -r requirements.txt

# Add your credentials
python setup_bot.py
```

**Note:** You'll need to authenticate with GitHub CLI or Personal Access Token.

---

## 🔧 Advanced: Using SSH Instead of HTTPS

More secure and no password prompts!

### Setup SSH Keys

1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Add to GitHub:
   - Copy your public key: `cat ~/.ssh/id_ed25519.pub`
   - Go to https://github.com/settings/keys
   - Click **"New SSH key"**
   - Paste and save

3. Change remote URL:
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/pokemon-draft-league-bot.git
   ```

Now you can push/pull without entering credentials!

---

## 🆘 Troubleshooting

### "Remote already exists"

```bash
# Remove old remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/YOUR_USERNAME/pokemon-draft-league-bot.git
```

### "Authentication failed"

- Use GitHub CLI: `gh auth login`
- Or create a Personal Access Token (Step 4, Option B)
- Make sure 2FA is set up if your account requires it

### "Repository not found"

- Check repository name matches exactly
- Make sure you replaced `YOUR_USERNAME` with your actual username
- If private, make sure you're logged in

### "Push rejected"

```bash
# Pull first, then push
git pull origin master --allow-unrelated-histories
git push origin master
```

---

## 📚 Quick Reference

### View Repository Status
```bash
git status
```

### View Commit History
```bash
git log --oneline -10
```

### Check Remote URL
```bash
git remote -v
```

### Create a Backup Branch
```bash
git checkout -b backup-branch
git push origin backup-branch
```

---

## ✅ Setup Checklist

Complete setup steps:

- [ ] Create GitHub account (if needed)
- [ ] Create **private** repository on GitHub
- [ ] Connect local code to GitHub (`git remote add origin`)
- [ ] Authenticate (GitHub CLI or Personal Access Token)
- [ ] Push code to GitHub (`git push -u origin master`)
- [ ] Verify code uploaded successfully
- [ ] Confirm `.credentials.json` is NOT in repository
- [ ] (Optional) Invite collaborators
- [ ] (Optional) Clone on additional computers

---

## 🎉 You're Done!

Your bot is now safely stored on GitHub!

**Your Private Repository:**
```
https://github.com/YOUR_USERNAME/pokemon-draft-league-bot
```

**Benefits:**
- ✅ Code backed up safely
- ✅ Access from any computer
- ✅ Version history saved
- ✅ Easy collaboration
- ✅ Free forever (private repositories are free!)

---

## 💡 Next Steps

1. **Set up the bot:** Run `setup_bot.py` to configure credentials
2. **Test locally:** Run `run_bot.bat` to test the bot
3. **Deploy (optional):** Follow `DEPLOYMENT_GUIDE.md` for hosting online

---

## 🔗 Helpful Links

- [GitHub Docs](https://docs.github.com/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub CLI](https://cli.github.com/)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

---

**Questions?** Check the troubleshooting section above or open an issue in your repository!

**Need help with bot setup?** See `QUICK_START.md` and `README.md`
