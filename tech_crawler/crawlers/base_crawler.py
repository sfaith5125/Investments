"""Base crawler class for all crawlers"""

import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from ..config import Settings


logger = logging.getLogger(__name__)


class BaseCrawler(ABC):
    """Abstract base class for all crawlers"""

    def __init__(self, source_name: str, source_url: str):
        """Initialize crawler with source information"""
        self.source_name = source_name
        self.source_url = source_url
        self.articles: List[Dict[str, Any]] = []

    @abstractmethod
    def fetch(self) -> bool:
        """
        Fetch content from the source.
        Should be implemented by subclasses.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def parse(self) -> List[Dict[str, Any]]:
        """
        Parse fetched content into articles.
        Should be implemented by subclasses.
        
        Returns:
            List[Dict]: List of parsed articles
        """
        pass

    def add_article(
        self,
        title: str,
        url: str,
        summary: str,
        published_date: datetime,
        content: str = "",
    ) -> None:
        """Add an article to the collection"""
        article = {
            "title": title,
            "url": url,
            "summary": summary,
            "published_date": published_date,
            "content": content,
            "source": self.source_name,
            "crawled_date": datetime.now(),
        }
        self.articles.append(article)
        logger.info(f"Added article: {title[:50]}... from {self.source_name}")

    def fetch_full_content(self, url: str) -> Optional[str]:
        """Fetch full article content from the URL"""
        try:
            headers = {"User-Agent": Settings.USER_AGENT}
            response = requests.get(
                url,
                headers=headers,
                timeout=Settings.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            article_element = soup.find("article")
            if article_element:
                paragraphs = article_element.find_all("p")
            else:
                paragraphs = soup.find_all("p")

            chunks = []
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text:
                    chunks.append(text)

            content = "\n\n".join(chunks)
            return content or None
        except Exception as e:
            logger.debug(f"Unable to fetch full content for {url}: {str(e)}")
            return None

    def get_articles(self) -> List[Dict[str, Any]]:
        """Return all collected articles"""
        return self.articles

    def clear_articles(self) -> None:
        """Clear the articles collection"""
        self.articles = []
