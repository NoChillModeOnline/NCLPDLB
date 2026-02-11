# 🔨 Building Executable Guide

This guide shows you how to create a standalone `.exe` file for your Pokemon Draft League Bot.

---

## 📋 **Two Options**

### **Option 1: Simple Batch File (Quick & Easy)** ✅ RECOMMENDED FOR BEGINNERS

This creates a `.bat` file you can double-click to start the bot.

**Pros:**
- Already created! (`run_bot.bat`)
- No additional setup needed
- Works immediately
- Easy to modify

**Cons:**
- Requires Python installed on the computer
- Shows command prompt window

**How to Use:**
1. Double-click `run_bot.bat`
2. Bot starts automatically!

---

### **Option 2: Standalone EXE (Advanced)**

This creates a true `.exe` file that doesn't require Python installed.

**Pros:**
- No Python installation needed
- Can distribute to others
- Professional appearance

**Cons:**
- Requires PyInstaller
- Larger file size (~50MB)
- Takes longer to build

---

## 🚀 **Option 1: Using the Batch File** (EASIEST)

### Step 1: Locate the File
Navigate to:
```
F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot\run_bot.bat
```

### Step 2: Run It
1. Double-click `run_bot.bat`
2. A command window opens
3. Bot starts automatically
4. Leave the window open while bot is running

### Step 3: Stop the Bot
- Press `Ctrl+C` in the command window
- Or just close the window

**That's it!** ✅

---

## 🔧 **Option 2: Building a Standalone EXE**

### Prerequisites
1. Python installed
2. All dependencies installed (`pip install -r requirements.txt`)
3. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

---

### Step 1: Run the Build Script

Open Command Prompt and navigate to the bot folder:
```bash
cd "F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot"
```

Run the build script:
```bash
python build_exe.py
```

**This will take 2-5 minutes.**

---

### Step 2: Locate the Executable

After building, you'll find:
```
F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot\dist\PokemonDraftBot.exe
```

---

### Step 3: Prepare for Deployment

Create a deployment folder with these files:
```
PokemonDraftBot/
├── PokemonDraftBot.exe       ← The executable
├── .credentials.json          ← Your credentials (REQUIRED!)
└── README.txt                 ← Optional: Usage instructions
```

**⚠️ IMPORTANT:** The `.credentials.json` file **MUST** be in the same folder as the `.exe`!

---

### Step 4: Run the Executable

1. Double-click `PokemonDraftBot.exe`
2. Console window opens showing bot status
3. Bot connects to Discord
4. Leave window open while running

---

## 📦 **Distributing to Others**

If you want to share the bot with friends/teammates:

### What to Share:
1. `PokemonDraftBot.exe` (from `dist` folder)
2. Instructions on how to get their own `.credentials.json`
3. Link to this documentation

### What NOT to Share:
- ❌ Your `.credentials.json` file (contains secrets!)
- ❌ Your Discord bot token
- ❌ Your Google service account credentials

### Instructions for Recipients:
1. They need to create their own Discord bot (follow `DEPLOYMENT_CHECKLIST.md`)
2. They need their own Google Sheets setup
3. They create their own `.credentials.json`
4. Place it next to `PokemonDraftBot.exe`
5. Run the executable

---

## 🐛 **Troubleshooting**

### Build Errors

**Error: `ModuleNotFoundError: No module named 'PyInstaller'`**
- **Fix:** Install PyInstaller: `pip install pyinstaller`

**Error: `RecursionError: maximum recursion depth exceeded`**
- **Fix:** Increase recursion limit in `build_exe.py`:
  ```python
  import sys
  sys.setrecursionlimit(5000)
  ```

**Error: Missing modules in built .exe**
- **Fix:** Add hidden imports to `build_exe.py`:
  ```python
  '--hidden-import=MODULE_NAME',
  ```

---

### Runtime Errors

**Error: `.credentials.json not found`**
- **Fix:** Make sure `.credentials.json` is in the same folder as the `.exe`

**Error: `DLL load failed` or `ImportError`**
- **Fix:** Rebuild with `--collect-all` flag for problematic packages

**Bot window closes immediately**
- **Fix:** Run from Command Prompt to see error messages:
  ```bash
  cd path\to\folder
  PokemonDraftBot.exe
  ```

---

## 📊 **File Size Comparison**

| Method | File Size | Notes |
|--------|-----------|-------|
| **Batch file** | < 1 KB | Requires Python installed |
| **EXE (onefile)** | ~50 MB | Standalone, no Python needed |
| **EXE (onedir)** | ~100 MB | Faster startup, multiple files |

---

## 🎯 **Recommendations**

### For Personal Use:
**Use the batch file (`run_bot.bat`)** ✅
- Simplest solution
- No build process needed
- Easy to update

### For Distribution:
**Build the EXE** ⚙️
- Share with non-technical users
- No Python installation required
- Professional appearance

### For Development:
**Run with Python** 🔧
- Fastest iteration
- Easy debugging
- Best for testing changes

---

## 🔄 **Updating the Bot**

### If Using Batch File:
1. Make changes to Python files
2. Save changes
3. Run `run_bot.bat` again
4. Changes take effect immediately

### If Using EXE:
1. Make changes to Python files
2. Run `python build_exe.py` again
3. Replace old `.exe` with new one from `dist` folder
4. Restart the bot

---

## ✅ **Quick Start**

**Want to start using the bot RIGHT NOW?**

Just double-click: `run_bot.bat` 🚀

That's it! No building, no compiling, no waiting.

---

## 📞 **Need Help?**

- Check `DEPLOYMENT_CHECKLIST.md` for setup issues
- Check `README.md` for command documentation
- Check console output for error messages
- Verify `.credentials.json` is properly formatted

---

**Happy Drafting!** 🎮⚡🔥💧
