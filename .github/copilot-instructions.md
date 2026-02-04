# Tech Investment Crawler - Development Guide

## Project Overview

Tech Investment News Crawler is a Python application that aggregates and analyzes technology-related investment news from multiple sources. It tracks US-based tech companies and industry trends to inform investment decisions.

## Project Structure

- **tech_crawler/**: Main package
  - **crawlers/**: RSS and HTML crawling implementations
  - **storage/**: Database models and management
  - **analysis/**: Article relevance analysis and tagging
  - **blog/**: Blog publishing framework (future enhancement)
  - **config/**: Configuration management
- **tests/**: Unit tests
- **main.py**: Application entry point

## Key Technologies

- **Python 3.8+**
- **SQLAlchemy**: Database ORM
- **BeautifulSoup4**: HTML parsing
- **FeedParser**: RSS feed parsing
- **Requests**: HTTP client

## Development Workflow

### Setup

1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure

### Running

- Execute crawler: `python main.py`
- Run tests: `pytest tests/`

### Key Components

- **TechInvestmentCrawler**: Main orchestrator in main.py
- **BaseCrawler**: Abstract base for all crawlers
- **RSSCrawler**: RSS feed parser
- **HTMLCrawler**: HTML page parser
- **ArticleAnalyzer**: Relevance analysis and tagging
- **Database**: Article persistence layer
- **BlogPublisher**: Blog API integration (future)

## Configuration

Edit `tech_crawler/config/settings.py` to:
- Add/remove news sources
- Track additional companies
- Monitor new tech trends
- Configure crawling behavior

## Future Enhancement: Blog Integration

The blog module provides a framework for publishing articles to external platforms:

1. Configure in `.env`:
   ```
   BLOG_ENABLED=True
   BLOG_API_URL=https://your-blog-api.com
   BLOG_API_KEY=your-key
   ```

2. Extend `BlogPublisher` in `tech_crawler/blog/publisher.py` to support:
   - WordPress REST API
   - Medium API
   - Ghost API
   - Custom platforms

3. Integrate into main workflow for automatic publishing

## Common Tasks

- **Add news source**: Edit `Settings.NEWS_SOURCES` in config/settings.py
- **Track new company**: Add to `Settings.TECH_COMPANIES`
- **Add trend keyword**: Add to `Settings.TECH_TRENDS`
- **Customize analysis**: Modify `ArticleAnalyzer` in analysis/analyzer.py
- **Change crawler behavior**: Edit rate limits and timeouts in config/settings.py

## Testing

Create tests in `tests/` directory:
- `test_crawlers.py`: Crawler functionality
- `test_analyzer.py`: Analysis logic
- `test_database.py`: Storage operations

Run: `pytest tests/ -v`
