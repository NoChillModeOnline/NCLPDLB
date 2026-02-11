# 🎨 Frontend Setup Guide

**Complete guide to setting up and using the Web Dashboard**

---

## 📋 Overview

The Pokemon Draft League Bot includes a **beautiful web dashboard** built with:
- ✅ **Flask** - Python web framework
- ✅ **HTML/CSS/JavaScript** - Responsive design
- ✅ **Real-time updates** - Auto-refreshing data
- ✅ **REST API** - 8 endpoints for integration

---

## ⚡ Quick Start (2 Minutes)

### Option 1: Use the Setup Wizard (Easiest)

1. **Run:** `setup_and_run.bat`
2. **Choose:** Option 3 (Run Web Dashboard) or Option 4 (Run Both)
3. **Open browser:** http://localhost:5000
4. **Done!** Dashboard is live

### Option 2: Manual Start

```bash
# Make sure you're in the bot directory
cd "F:\Claude Code\Claude\Claude Chats\pokemon-draft-bot"

# Start the web server
python web_server.py
```

Then open http://localhost:5000 in your browser!

---

## 🖥️ What You Get

### Main Dashboard
**URL:** http://localhost:5000

Shows:
- ✅ League information and statistics
- ✅ Current draft status
- ✅ Active players and teams
- ✅ Recent activity
- ✅ System status

Features:
- 📊 Real-time stats
- 🔄 Auto-refresh every 30 seconds
- 📱 Mobile responsive
- 🎨 Clean, modern UI

### Teams Page
**URL:** http://localhost:5000/teams

Shows:
- ✅ All registered teams
- ✅ Team rosters with Pokemon
- ✅ Tera Captain information
- ✅ Team records (wins/losses)
- ✅ Coach information

### Individual Team View
**URL:** http://localhost:5000/team/PlayerName

Shows:
- ✅ Complete team roster
- ✅ Point allocation
- ✅ Type coverage analysis
- ✅ Tera Captain details
- ✅ Weaknesses and resistances

---

## 🔧 Prerequisites

### Already Included
- ✅ Flask (installed via requirements.txt)
- ✅ HTML templates (in templates/ folder)
- ✅ CSS styling (in static/css/)
- ✅ JavaScript (in static/js/)

### You Need
- ✅ `.credentials.json` configured (bot credentials)
- ✅ Google Sheets with data
- ✅ Python 3.8+

---

## 📁 File Structure

```
pokemon-draft-bot/
├── web_server.py          # Main Flask application
├── templates/             # HTML templates
│   ├── base.html         # Base template (header/footer)
│   ├── dashboard.html    # Main dashboard page
│   └── teams.html        # Teams listing page
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Styling
    └── js/
        └── main.js       # Client-side JavaScript
```

---

## 🚀 Running the Dashboard

### Method 1: Interactive Menu (Recommended)

```bash
# Run the setup menu
setup_and_run.bat

# Choose option:
# 3 - Run Web Dashboard only
# 4 - Run Both (Bot + Dashboard)
```

### Method 2: Direct Python Command

```bash
# Windows
python web_server.py

# Mac/Linux
python3 web_server.py
```

### Method 3: Run Both Services

Start bot and dashboard simultaneously:

```bash
# Windows - Opens two separate windows
start "Discord Bot" cmd /k python bot.py
start "Web Dashboard" cmd /k python web_server.py
```

---

## 🌐 Accessing the Dashboard

### Local Access (Default)

**Dashboard:** http://localhost:5000
**Teams Page:** http://localhost:5000/teams
**API Status:** http://localhost:5000/api/status

### Network Access (Other Devices)

To access from other devices on your network:

1. **Find your IP address:**
   ```bash
   # Windows
   ipconfig
   # Look for "IPv4 Address"

   # Mac/Linux
   ifconfig
   # Look for "inet"
   ```

2. **Update web_server.py (Line 305):**
   ```python
   # Change from:
   app.run(debug=True, host='127.0.0.1', port=5000)

   # To:
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```

3. **Access from other devices:**
   ```
   http://YOUR_IP_ADDRESS:5000
   Example: http://192.168.1.100:5000
   ```

4. **Firewall:** Make sure port 5000 is allowed in Windows Firewall

---

## 🎨 Customization

### Change Port

Edit `web_server.py` (last line):
```python
# Default port 5000
app.run(debug=True, port=5000)

# Change to 8080
app.run(debug=True, port=8080)
```

### Change Theme Colors

Edit `static/css/style.css`:
```css
/* Primary color */
:root {
    --primary-color: #3b82f6;  /* Change this */
    --secondary-color: #10b981; /* And this */
}
```

### Add Custom Pages

1. Create HTML template in `templates/`
2. Add route in `web_server.py`:
   ```python
   @app.route('/mypage')
   def my_page():
       return render_template('mypage.html')
   ```

---

## 🔌 REST API Endpoints

The dashboard includes a REST API for integration:

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Bot and server status |
| `/api/league/info` | GET | League information |
| `/api/teams/all` | GET | All teams and rosters |
| `/api/team/<player>` | GET | Individual team details |
| `/api/draft/status` | GET | Draft progress |
| `/api/standings` | GET | League standings |
| `/api/pokemon/available` | GET | Available Pokemon for draft |
| `/api/stats/summary` | GET | League statistics |

### Example API Usage

**JavaScript:**
```javascript
// Get league info
fetch('http://localhost:5000/api/league/info')
    .then(response => response.json())
    .then(data => console.log(data));

// Get team data
fetch('http://localhost:5000/api/team/PlayerName')
    .then(response => response.json())
    .then(data => console.log(data));
```

**Python:**
```python
import requests

# Get all teams
response = requests.get('http://localhost:5000/api/teams/all')
teams = response.json()
print(teams)
```

**curl:**
```bash
# Get API status
curl http://localhost:5000/api/status

# Get draft status
curl http://localhost:5000/api/draft/status
```

---

## 🔒 Security Notes

### For Local Use (Default)
- ✅ Dashboard runs on localhost (127.0.0.1)
- ✅ Only accessible from your computer
- ✅ No internet exposure
- ✅ Credentials stay private

### For Public Access
⚠️ **Not recommended without additional security!**

If you want public access:
1. Use a proper hosting service (Railway, Heroku, etc.)
2. Add authentication (login system)
3. Use HTTPS (SSL certificate)
4. Hide sensitive data

**See:** `DEPLOYMENT_GUIDE.md` for secure public hosting

---

## 🐛 Troubleshooting

### "Port already in use"

Another service is using port 5000:

**Solution 1:** Change port in `web_server.py`
```python
app.run(debug=True, port=8080)  # Use different port
```

**Solution 2:** Kill existing process
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### "Module not found: flask"

Flask not installed:

```bash
pip install flask
# Or reinstall all dependencies:
pip install -r requirements.txt
```

### "Template not found"

Templates folder missing or wrong location:

```bash
# Make sure you're in the bot directory
cd pokemon-draft-bot

# Verify templates exist
ls templates/
# Should show: base.html, dashboard.html, teams.html
```

### "No data showing"

Bot needs to be running and configured:

1. Check `.credentials.json` exists
2. Verify Google Sheets has data
3. Run bot first: `python bot.py`
4. Then run dashboard: `python web_server.py`

### "Cannot connect from other device"

1. Check firewall allows port 5000
2. Make sure `host='0.0.0.0'` in web_server.py
3. Use correct IP address (not localhost)
4. Both devices on same network

---

## 📊 Performance

### Auto-Refresh

Dashboard auto-refreshes every 30 seconds:

**To change refresh rate:**

Edit `static/js/main.js`:
```javascript
// Refresh every 30 seconds (default)
setInterval(loadDashboardData, 30000);

// Change to 60 seconds
setInterval(loadDashboardData, 60000);

// Disable auto-refresh
// Comment out the setInterval line
```

### Caching

API responses are cached to reduce Google Sheets API calls:
- Pokemon data: 5-minute cache
- Config data: 10-minute cache

**See:** `OPTIMIZATION_SUMMARY.md` for performance details

---

## 🎯 Features Explained

### Real-Time Updates
- Dashboard fetches new data every 30 seconds
- No need to manually refresh page
- Shows live draft progress
- Updates team rosters automatically

### Responsive Design
- Works on desktop, tablet, and mobile
- Adapts layout to screen size
- Touch-friendly interface

### Type Badges
- Color-coded by Pokemon type
- Official Pokemon type colors
- Hover for type effectiveness

### Error Handling
- Graceful fallbacks if data unavailable
- Clear error messages
- Automatic retry on failure

---

## 🚀 Next Steps

### Basic Setup
1. ✅ Run `python web_server.py`
2. ✅ Open http://localhost:5000
3. ✅ Explore dashboard features

### Advanced Setup
1. 📱 Enable network access (change host)
2. 🎨 Customize colors/theme
3. 🔌 Use REST API for integrations
4. 🌐 Deploy publicly (see DEPLOYMENT_GUIDE.md)

### Integration
1. Use API endpoints in your apps
2. Create custom dashboards
3. Build mobile apps
4. Add Discord bot commands

---

## 📚 Related Documentation

- **WEB_DASHBOARD_GUIDE.md** - Detailed dashboard features
- **DEPLOYMENT_GUIDE.md** - Public hosting options
- **OPTIMIZATION_SUMMARY.md** - Performance details
- **README.md** - Complete bot documentation

---

## ✅ Setup Checklist

- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Configure `.credentials.json`
- [ ] Verify Google Sheets has data
- [ ] Run web server (`python web_server.py`)
- [ ] Open browser to http://localhost:5000
- [ ] Test dashboard features
- [ ] (Optional) Enable network access
- [ ] (Optional) Customize theme
- [ ] (Optional) Set up API integration

---

## 🎉 You're Done!

Your Pokemon Draft League Web Dashboard is ready!

**Access:** http://localhost:5000

**Features:**
- ✅ Real-time league statistics
- ✅ Team rosters and analysis
- ✅ Draft progress monitoring
- ✅ REST API for integrations
- ✅ Mobile-responsive design

**Questions?** See troubleshooting section above or check related documentation!

---

**Pro Tip:** Run both bot and dashboard together using `setup_and_run.bat` → Option 4!
