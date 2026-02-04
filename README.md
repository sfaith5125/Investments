# Tech Investment News Crawler

A comprehensive web crawler application for aggregating and analyzing technology-related investment news and trends. Designed to inform investment decisions in US-based tech companies.

## Features

- **Multi-Source News Aggregation**: Crawls RSS feeds and HTML-based news sources
- **Relevance Analysis**: Automatically analyzes articles for relevance to tech investments
- **Company & Trend Tracking**: Identifies mentions of tracked tech companies and industry trends
- **Database Storage**: Persistent storage of articles with search capabilities
- **Modular Architecture**: Clean separation of concerns for easy extension
- **Blog Integration Ready**: Framework for future blog publishing capabilities

## Project Structure

```
tech_crawler/
├── crawlers/           # Web crawling implementations (RSS, HTML)
├── storage/            # Database models and management
├── analysis/           # Article analysis and tagging
├── blog/               # Blog publishing (future enhancement)
└── config/             # Configuration settings

tests/                  # Unit tests
main.py                # Main entry point
requirements.txt       # Python dependencies
```

## Installation

1. Clone or navigate to the project directory:
```bash
cd c:\Users\sfaith\Dev\Investments
```

2. Create a Python virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` with your settings:
```
DEBUG=False
DATABASE_URL=sqlite:///tech_crawler.db
REQUEST_TIMEOUT=10
RATE_LIMIT_DELAY=1.0
```

## Usage

### Running the Web Interface

Start the web server to browse and search articles:

```bash
python web_server.py
```

Then open your browser to `http://localhost:5000`

**Features:**
- 📊 Dashboard with statistics
- 📰 Browse all articles
- 🔍 Full-text search across articles
- 🏷️ Filter by source and date range
- 📱 Responsive design (works on mobile)

**Pages:**
- **Dashboard** (`/`): Overview with recent articles and stats
- **Articles** (`/articles`): Browse all articles with filters
- **Search** (`/search`): Search articles by keyword, company, or trend
- **API Endpoints**:
  - `GET /api/articles` - Fetch articles (paginated)
  - `GET /api/search?q=keyword` - Search articles
  - `GET /api/stats` - Get database statistics

### Basic Crawling

Run the crawler to fetch and analyze articles:

```bash
python main.py
```

This will:
1. Fetch articles from all configured news sources
2. Parse and analyze articles for relevance
3. Save relevant articles to the database
4. Log statistics

### Tracked Companies

The crawler tracks these major US tech companies:
- Apple (AAPL)
- Microsoft (MSFT)
- Nvidia (NVDA)
- Alphabet (GOOGL)
- Meta (META)
- Tesla (TSLA)
- And more...

### Tracked Trends

The crawler monitors these tech trends:
- Artificial Intelligence
- Machine Learning
- Quantum Computing
- Cloud Computing
- Cybersecurity
- Blockchain
- 5G & Edge Computing
- And more...

## Future Enhancements

### Blog Publishing
The application is designed with future blog integration in mind:
- `blog/` module provides placeholder for API integration
- Configure `BLOG_API_URL` and `BLOG_API_KEY` in `.env`
- Support for WordPress, Medium, Ghost, and custom APIs can be added
- Automatic article publishing and summary generation

### Potential Additions
- Advanced NLP sentiment analysis
- Machine learning classification
- Real-time notifications for breaking news
- Email digests
- Integration with financial APIs (Alpha Vantage, IEX)
- Web dashboard for browsing articles
- RSS feed generation for readers

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New News Sources

Edit `tech_crawler/config/settings.py`:

```python
NEWS_SOURCES = [
    {
        "name": "Your Source",
        "url": "https://example.com/feed",
        "type": "rss",  # or "html"
    },
    # ...
]
```

### Adding New Companies to Track

Edit `TECH_COMPANIES` in `tech_crawler/config/settings.py`:

```python
TECH_COMPANIES = [
    {"name": "Company Name", "ticker": "TICK"},
    # ...
]
```

## Database

Articles are stored in SQLite with the following fields:
- `title`: Article title
- `url`: Original article URL
- `summary`: Article summary
- `content`: Full content (if available)
- `source`: News source
- `published_date`: Publication date
- `crawled_date`: When the article was crawled
- `relevant`: Relevance to tech investing
- `processed`: Whether article has been processed
- `tags`: Associated company/trend tags

### Querying the Database

```python
from tech_crawler.storage import Database

db = Database()
articles = db.get_articles(limit=50, days_back=7)
results = db.search_articles("artificial intelligence")
```

## Logging

The application logs to console with the following levels:
- `DEBUG`: Detailed information (when `DEBUG=True`)
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## License

[Add your license here]

## Author

Investment Research Team

## Support

For issues or questions, please create an issue in the project repository.
