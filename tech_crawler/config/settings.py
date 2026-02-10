"""Application configuration settings"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""

    # Application
    APP_NAME = "Tech Investment Crawler"
    APP_VERSION = "0.1.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Data storage
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tech_crawler.db")
    DATA_DIR = os.getenv("DATA_DIR", "data")
    ARTICLES_DIR = os.path.join(DATA_DIR, "articles")

    # Crawling settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    )
    RATE_LIMIT_DELAY = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))

    # News sources (can be extended)
    NEWS_SOURCES = [
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed/",
            "type": "rss",
        },
        {
            "name": "The Verge",
            "url": "https://www.theverge.com/rss/index.xml",
            "type": "rss",
        },
        {
            "name": "Hacker News",
            "url": "https://news.ycombinator.com/",
            "type": "html",
        },
        {
            "name": "ArXiv CS",
            "url": "https://arxiv.org/rss/cs.AI",
            "type": "rss",
        },
        {
            "name": "Wired",
            "url": "https://www.wired.com/feed/category/tech/latest/rss",
            "type": "rss",
        },
        {
            "name": "Ars Technica",
            "url": "https://arstechnica.com/feed/",
            "type": "rss",
        },
        {
            "name": "Dev.to",
            "url": "https://dev.to/feed",
            "type": "rss",
        },

    ]

    # Tech companies to track (S&P 500 tech companies)
    TECH_COMPANIES = [
        {"name": "Apple", "ticker": "AAPL"},
        {"name": "Microsoft", "ticker": "MSFT"},
        {"name": "Nvidia", "ticker": "NVDA"},
        {"name": "Alphabet", "ticker": "GOOGL"},
        {"name": "Meta", "ticker": "META"},
        {"name": "Tesla", "ticker": "TSLA"},
        {"name": "Broadcom", "ticker": "AVGO"},
        {"name": "Qualcomm", "ticker": "QCOM"},
        {"name": "AMD", "ticker": "AMD"},
        {"name": "Cisco", "ticker": "CSCO"},
        {"name": "Intel", "ticker": "INTC"},
        {"name": "Snowflake", "ticker": "SNOW"},
        {"name": "Salesforce", "ticker": "CRM"},
        {"name": "Stripe", "ticker": "PRIVATE"},
        {"name": "Figma", "ticker": "PRIVATE"},
    ]

    # Tech trends keywords
    TECH_TRENDS = [
        "artificial intelligence",
        "machine learning",
        "quantum computing",
        "cloud computing",
        "cybersecurity",
        "blockchain",
        "5G",
        "edge computing",
        "autonomous vehicles",
        "augmented reality",
        "virtual reality",
        "metaverse",
        "web3",
        "api economy",
        "no-code",
        "devops",
        "microservices",
        "containers",
    ]

    # Blog configuration (for future enhancement)
    BLOG_ENABLED = os.getenv("BLOG_ENABLED", "False").lower() == "true"
    BLOG_API_URL = os.getenv("BLOG_API_URL", "")
    BLOG_API_KEY = os.getenv("BLOG_API_KEY", "")

    @classmethod
    def get_config_dict(cls) -> dict:
        """Return configuration as dictionary"""
        return {
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "debug": cls.DEBUG,
            "database_url": cls.DATABASE_URL,
            "data_dir": cls.DATA_DIR,
            "request_timeout": cls.REQUEST_TIMEOUT,
            "rate_limit_delay": cls.RATE_LIMIT_DELAY,
        }
