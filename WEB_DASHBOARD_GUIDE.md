# 🌐 Web Dashboard Guide

## Overview

The Pokemon Draft League Bot now includes a beautiful **web-based dashboard** that provides real-time visualization of your league data!

---

## 🚀 Quick Start

### **Method 1: Interactive Menu** (EASIEST!)

1. **Double-click:** `setup_and_run.bat`
2. **Choose option 3:** Run Web Dashboard
3. **Access at:** http://localhost:5000

### **Method 2: Command Line**

```bash
python web_server.py
```

Then open your browser to: **http://localhost:5000**

### **Method 3: Run Bot + Dashboard Together**

```bash
# Using the menu
Double-click: setup_and_run.bat
Choose option 4: Run Both

# OR manually
python bot.py  # Terminal 1
python web_server.py  # Terminal 2
```

---

## 📊 Dashboard Features

### **Main Dashboard** (`/`)
- **League Statistics:**
  - Total teams registered
  - Total Pokemon available
  - Matches played
  - Average team size

- **League Information:**
  - League name
  - Point budget (120 default)
  - Team size requirements (10-12 Pokemon)
  - Tera Captain limit (3 per team)

- **Draft Status:**
  - Live/Inactive indicator
  - Picks made counter
  - Quick link to draft page

- **Current Standings:**
  - Top 5 teams
  - Win/Loss records
  - Win percentage
  - Link to full standings

### **Teams Page** (`/teams`)
- Grid view of all teams
- Team logos (if uploaded)
- Pokemon count and points used
- Win/Loss records
- Click team to view details

### **Draft Page** (`/draft`)
- Live draft progress
- Recent picks
- Current turn indicator
- Draft order display

### **Standings Page** (`/standings`)
- Complete league rankings
- Sortable by wins/losses
- Win percentage calculations
- Team statistics

### **Team Detail Page** (`/team/<player>`)
- Full roster with Pokemon details
- Type coverage analysis
- Team weaknesses and strengths
- Tera Captain selections
- Suggested Tera types
- Speed tier breakdown
- Efficiency score (0-100)

---

## 🔌 API Endpoints

All API endpoints return JSON data for integration with other tools.

### **Status & Info**

| Endpoint | Description | Example Response |
|----------|-------------|------------------|
| `/api/status` | Server status | `{"status": "online", "version": "1.0.0"}` |
| `/api/league/info` | League config | `{"league_name": "...", "total_points": 120}` |
| `/api/stats/summary` | Statistics | `{"total_teams": 8, "total_matches": 24}` |

### **Teams & Rosters**

| Endpoint | Description |
|----------|-------------|
| `/api/teams/all` | All teams with basic info |
| `/api/team/<player>` | Detailed team data + analysis |

### **Draft & Standings**

| Endpoint | Description |
|----------|-------------|
| `/api/draft/status` | Current draft status |
| `/api/standings` | League standings |
| `/api/pokemon/available` | Available Pokemon list |

### **Example API Usage**

```javascript
// Fetch league standings
fetch('http://localhost:5000/api/standings')
  .then(response => response.json())
  .then(data => console.log(data.standings));

// Get team analysis
fetch('http://localhost:5000/api/team/PlayerName')
  .then(response => response.json())
  .then(data => console.log(data.analysis));
```

---

## 🎨 Visual Features

### **Type Badges**
Pokemon types displayed with official colors:
- Fire: 🔥 Red
- Water: 💧 Blue
- Electric: ⚡ Yellow
- Grass: 🌿 Green
- And all 19 types including Stellar!

### **Real-Time Updates**
- Auto-refresh every 30 seconds
- Manual refresh with `Ctrl+R`
- Status indicator in footer
- Live draft updates

### **Responsive Design**
- Mobile-friendly layout
- Tablet optimization
- Desktop experience
- Works on all screen sizes

### **Smooth Animations**
- Fade-in effects
- Hover transitions
- Loading spinners
- Toast notifications

---

## ⚙️ Configuration

### **Port Configuration**

Change the default port (5000) in `web_server.py`:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
# Change port=5000 to your desired port
```

### **Auto-Refresh Interval**

Change refresh rate in dashboard templates:

```javascript
// Default: 30 seconds
setInterval(loadData, 30000);

// Change to 60 seconds
setInterval(loadData, 60000);
```

### **Theme Colors**

Customize colors in `tailwind.config`:

```javascript
colors: {
    'pokemon-red': '#DC0A2D',    // Primary red
    'pokemon-blue': '#3B4CCA',   // Primary blue
    'pokemon-yellow': '#FFCB05', // Primary yellow
}
```

---

## 🔒 Security

### **Local Network Only**

By default, the server binds to `0.0.0.0`, making it accessible on your local network.

**To restrict to localhost only:**

```python
app.run(host='127.0.0.1', port=5000, debug=True)
```

### **Production Deployment**

For production, disable debug mode and use a production WSGI server:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app
```

### **Authentication** (Future Enhancement)

Currently, no authentication is required. For public deployment, consider adding:
- Login system
- Discord OAuth
- API key authentication
- Rate limiting

---

## 🐛 Troubleshooting

### **Dashboard Won't Start**

**Error: `Port 5000 already in use`**
- **Solution:** Another application is using port 5000
- **Fix:** Change port in `web_server.py` or stop the conflicting application

**Error: `ModuleNotFoundError: No module named 'flask'`**
- **Solution:** Flask not installed
- **Fix:** Run `pip install -r requirements.txt`

### **Data Not Loading**

**Empty dashboard or error messages**
- **Check:** Bot connected to Google Sheets?
- **Fix:** Ensure `.credentials.json` is configured
- **Test:** Run `python test_imports.py`

**API returns errors**
- **Check:** Browser console (F12) for error messages
- **Check:** Terminal for server logs
- **Verify:** Google Sheet has required tabs (Config, Teams, Pokemon, etc.)

### **Slow Performance**

**Dashboard loads slowly**
- **Issue:** Large dataset
- **Fix:** Caching is enabled automatically (5-minute TTL)
- **Alternative:** Reduce auto-refresh frequency

**API calls timing out**
- **Issue:** Google Sheets API rate limit
- **Fix:** Caching reduces API calls by 70-85%
- **Note:** Limit is 60 requests/minute

---

## 📱 Mobile Access

### **Access from Phone/Tablet**

1. **Find your computer's IP address:**
   ```bash
   # Windows
   ipconfig

   # Mac/Linux
   ifconfig
   ```

2. **On mobile browser, navigate to:**
   ```
   http://YOUR_COMPUTER_IP:5000
   ```

3. **Example:**
   ```
   http://192.168.1.100:5000
   ```

### **QR Code** (Optional)

Generate a QR code for easy mobile access:

```bash
pip install qrcode
python -c "import qrcode; qrcode.make('http://192.168.1.100:5000').save('dashboard_qr.png')"
```

---

## 🎯 Use Cases

### **For League Organizers**
- Monitor draft progress live
- Check team compositions
- Update standings easily
- Share dashboard URL with players

### **For Players**
- View your team anytime
- Check type coverage
- See Tera suggestions
- Compare with opponents

### **For Spectators**
- Follow draft live
- View league standings
- Browse all teams
- Track match results

---

## 🔄 Integration

### **Embed in Discord**

Share dashboard link in Discord channel:

```
📊 **League Dashboard**
View live stats: http://localhost:5000
```

### **OBS/Streaming**

Add dashboard as browser source in OBS:

1. Add Source → Browser
2. URL: `http://localhost:5000`
3. Width: 1920, Height: 1080
4. Use for streaming overlay!

### **Export Data**

Use API endpoints to export data:

```bash
# Export standings to JSON
curl http://localhost:5000/api/standings > standings.json

# Export all teams
curl http://localhost:5000/api/teams/all > teams.json
```

---

## 📊 Screenshots

### Dashboard
![Dashboard Preview](https://via.placeholder.com/800x600?text=Dashboard+Preview)

### Teams Page
![Teams Preview](https://via.placeholder.com/800x600?text=Teams+Preview)

### Team Detail
![Team Detail Preview](https://via.placeholder.com/800x600?text=Team+Detail+Preview)

---

## 🚀 Future Enhancements

Planned features for future versions:

- [ ] **Real-time updates** with WebSockets
- [ ] **Dark mode** toggle
- [ ] **Custom themes** per league
- [ ] **Advanced statistics** and charts
- [ ] **Player profiles** with history
- [ ] **Match scheduling** system
- [ ] **Live battle viewer**
- [ ] **Mobile app** (React Native)
- [ ] **Admin panel** for league management
- [ ] **Discord OAuth** integration

---

## 📚 Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Tailwind CSS:** https://tailwindcss.com/
- **REST API Design:** https://restfulapi.net/
- **Web Development:** https://developer.mozilla.org/

---

## ✅ Quick Checklist

Before using the dashboard:

- [x] Install Flask: `pip install flask flask-cors`
- [x] Configure `.credentials.json`
- [x] Start web server: `python web_server.py`
- [x] Access dashboard: http://localhost:5000
- [x] Check server status in footer
- [x] Test API endpoints
- [x] Enjoy real-time league data!

---

**Built with ❤️ for Pokemon Draft Leagues**

🎮 **Happy Drafting!** 🔥💧⚡
