"""HTML crawler implementation"""

import logging
import requests
from typing import List, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup

from .base_crawler import BaseCrawler
from ..config import Settings

logger = logging.getLogger(__name__)


class HTMLCrawler(BaseCrawler):
    """Crawler for HTML-based content"""

    def __init__(self, source_name: str, source_url: str):
        """Initialize HTML crawler"""
        super().__init__(source_name, source_url)
        self.html_content = None

    def fetch(self) -> bool:
        """Fetch HTML content from URL"""
        try:
            logger.info(f"Fetching HTML content from {self.source_url}")
            headers = {"User-Agent": Settings.USER_AGENT}
            response = requests.get(
                self.source_url,
                headers=headers,
                timeout=Settings.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            self.html_content = response.text
            return True

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error fetching HTML from {self.source_url}: {str(e)}"
            )
            return False

    def parse(self) -> List[Dict[str, Any]]:
        """Parse HTML content (basic implementation for demo)"""
        if not self.html_content:
            logger.warning(f"No HTML content for {self.source_name}")
            return []

        try:
            soup = BeautifulSoup(self.html_content, "html.parser")
            
            # Example: Parse articles from a news site
            # This is a basic implementation that should be customized per source
            articles = soup.find_all("article")
            
            if not articles:
                # Fallback: look for common article containers
                articles = soup.find_all("div", class_=lambda x: x and "article" in x.lower())

            for article in articles[:20]:  # Limit to 20 articles
                try:
                    title_elem = article.find(["h1", "h2", "h3", "a"])
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    
                    link_elem = article.find("a", href=True)
                    url = link_elem["href"] if link_elem else ""
                    
                    if not url.startswith(("http://", "https://")):
                        # Make absolute URL
                        from urllib.parse import urljoin
                        url = urljoin(self.source_url, url)

                    summary_elem = article.find("p")
                    summary = (
                        summary_elem.get_text(strip=True) 
                        if summary_elem else ""
                    )

                    full_content = self.fetch_full_content(url)

                    if title and url:
                        self.add_article(
                            title=title,
                            url=url,
                            summary=summary,
                            published_date=datetime.now(),
                            content=full_content or summary,
                        )

                except Exception as e:
                    logger.debug(f"Error parsing article element: {str(e)}")
                    continue

            logger.info(
                f"Parsed {len(self.articles)} articles from {self.source_name}"
            )
            return self.articles

        except Exception as e:
            logger.error(f"Error parsing HTML for {self.source_name}: {str(e)}")
            return []
