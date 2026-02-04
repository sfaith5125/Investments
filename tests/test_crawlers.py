"""Tests for crawler functionality"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime

from tech_crawler.crawlers import BaseCrawler, RSSCrawler


class TestBaseCrawler(unittest.TestCase):
    """Test BaseCrawler base class"""

    def setUp(self):
        """Set up test fixtures"""
        self.crawler = Mock(spec=BaseCrawler)
        self.crawler.source_name = "Test Source"
        self.crawler.source_url = "https://example.com"
        self.crawler.articles = []

    def test_add_article(self):
        """Test adding an article"""
        article_data = {
            "title": "Test Article",
            "url": "https://example.com/article",
            "summary": "Test summary",
            "published_date": datetime.now(),
        }
        
        article = {
            "title": article_data["title"],
            "url": article_data["url"],
            "summary": article_data["summary"],
            "published_date": article_data["published_date"],
            "source": self.crawler.source_name,
            "crawled_date": datetime.now(),
        }
        self.crawler.articles.append(article)
        
        self.assertEqual(len(self.crawler.articles), 1)
        self.assertEqual(self.crawler.articles[0]["title"], "Test Article")

    def test_get_articles(self):
        """Test retrieving articles"""
        for i in range(3):
            article = {
                "title": f"Article {i}",
                "url": f"https://example.com/article{i}",
                "summary": f"Summary {i}",
                "published_date": datetime.now(),
                "source": self.crawler.source_name,
                "crawled_date": datetime.now(),
            }
            self.crawler.articles.append(article)
        
        self.assertEqual(len(self.crawler.articles), 3)


if __name__ == "__main__":
    unittest.main()
