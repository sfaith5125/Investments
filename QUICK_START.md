# Quick Start Guide - Web Interface

Get the web interface running in 30 seconds!

## Step 1: Run the Crawler (if not done)
```bash
python main.py
```
This populates the database with articles.

## Step 2: Start the Web Server
```bash
python web_server.py
```

Output will show:
```
Starting Tech Investment Crawler Web Server
Web server running at http://localhost:5000
 * Running on http://0.0.0.0:5000
```

## Step 3: Open Your Browser
Visit: **http://localhost:5000**

You should see:
- 📊 **Dashboard** with statistics
- 📰 Recent relevant articles
- Navigation menu (Articles, Search)

## What Can You Do?

### 📊 Dashboard
- View total articles crawled
- See number of news sources
- Browse recent articles
- Quick link to all articles

### 📰 Articles Page
- Browse all articles
- Filter by source (TechCrunch, The Verge, ArXiv, etc.)
- Filter by date range (7, 30, 90, 365 days)
- Click to read full articles

### 🔍 Search
- Search for companies: "Apple", "Microsoft", "Nvidia"
- Search for trends: "AI", "quantum", "blockchain"
- Search for keywords: any word or phrase
- Get results instantly

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+K` or `/` | Jump to search |
| `Ctrl+Shift+B` | Run crawler (VS Code) |
| `F5` | Refresh page |

## Common Tasks

### I want to see Apple news
1. Go to Search page
2. Type "Apple"
3. Press Enter
4. See all articles mentioning Apple

### I want recent TechCrunch articles
1. Go to Articles page
2. Filter by source: "TechCrunch"
3. Filter by date: "7 days"
4. Scroll to browse

### I want to check the database
Visit: `http://localhost:5000/api/stats`

Shows:
- Total articles
- All sources
- Last crawl time

### I want to integrate with my app
Use the API endpoints:
```bash
# Get articles
curl http://localhost:5000/api/articles?limit=10

# Search
curl http://localhost:5000/api/search?q=AI

# Stats
curl http://localhost:5000/api/stats
```

## Next Steps

- 📖 Read: `WEB_INTERFACE.md` for full documentation
- 🔧 Configure: Edit `tech_crawler/config/settings.py` to add sources
- 📊 Crawl: Run `python main.py` to update data
- 🎨 Customize: Modify `tech_crawler/web/static/style.css` for styling

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Port already in use" | Change port in `web_server.py` |
| "No articles showing" | Run `python main.py` first |
| "Page looks broken" | Clear browser cache (Ctrl+Shift+Delete) |
| "Flask not found" | Run `pip install -r requirements.txt` |

## Running Crawler on Schedule

### Windows Task Scheduler
```batch
# Run crawler every hour
schtasks /create /tn "CrawlerTask" /tr "python C:\Users\sfaith\Dev\Investments\main.py" /sc hourly
```

### Python Scheduler (APScheduler)
```bash
pip install APScheduler
# Then modify main.py to use scheduler
```

---

**Happy crawling!** 🚀

Questions? Check `WEB_INTERFACE.md` for more details.
