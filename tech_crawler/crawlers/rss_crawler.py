"""RSS feed crawler implementation"""

import logging
import feedparser
from typing import List, Dict, Any
from datetime import datetime
from dateutil import parser as date_parser

from .base_crawler import BaseCrawler
from ..config import Settings

logger = logging.getLogger(__name__)


class RSSCrawler(BaseCrawler):
    """Crawler for RSS feeds"""

    def __init__(self, source_name: str, feed_url: str):
        """Initialize RSS crawler"""
        super().__init__(source_name, feed_url)
        self.feed_data = None

    def fetch(self) -> bool:
        """Fetch RSS feed"""
        try:
            logger.info(f"Fetching RSS feed from {self.source_url}")
            self.feed_data = feedparser.parse(self.source_url)
            
            if self.feed_data.bozo:
                logger.warning(
                    f"Feed parsing issue for {self.source_name}: "
                    f"{self.feed_data.bozo_exception}"
                )
            
            return len(self.feed_data.entries) > 0
        except Exception as e:
            logger.error(f"Error fetching RSS feed {self.source_url}: {str(e)}")
            return False

    def parse(self) -> List[Dict[str, Any]]:
        """Parse RSS feed entries"""
        if not self.feed_data:
            logger.warning(f"No feed data for {self.source_name}")
            return []

        try:
            for entry in self.feed_data.entries:
                title = entry.get("title", "No Title")
                url = entry.get("link", "")
                summary = entry.get("summary", "")
                
                # Parse publication date
                published_date = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    published_date = datetime(*entry.updated_parsed[:6])
                else:
                    published_date = datetime.now()

                if title and url:
                    full_content = self.fetch_full_content(url)
                    self.add_article(
                        title=title,
                        url=url,
                        summary=summary,
                        published_date=published_date,
                        content=full_content or summary,
                    )

            logger.info(
                f"Parsed {len(self.articles)} articles from {self.source_name}"
            )
            return self.articles

        except Exception as e:
            logger.error(f"Error parsing RSS feed {self.source_name}: {str(e)}")
            return []
