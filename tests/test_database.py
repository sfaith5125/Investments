"""Tests for database functionality"""

import unittest
from datetime import datetime

from tech_crawler.storage import Database, Article


class TestDatabase(unittest.TestCase):
    """Test Database"""

    def setUp(self):
        """Set up test fixtures"""
        # Use in-memory SQLite database for tests
        self.db_url = "sqlite:///:memory:"
        self.db = Database(self.db_url)

    def tearDown(self):
        """Clean up"""
        pass

    def test_add_article(self):
        """Test adding an article"""
        article_data = {
            "title": "Test Article",
            "url": "https://example.com/test",
            "summary": "Test summary",
            "source": "Test Source",
            "published_date": datetime.now(),
        }
        
        result = self.db.add_article(article_data)
        
        self.assertIsNotNone(result)
        # Verify article was added by checking count
        count = self.db.get_article_count()
        self.assertEqual(count, 1)

    def test_add_duplicate_article(self):
        """Test adding duplicate article (should update)"""
        article_data = {
            "title": "Test Article",
            "url": "https://example.com/test",
            "summary": "Test summary",
            "source": "Test Source",
            "published_date": datetime.now(),
        }
        
        # Add article twice
        self.db.add_article(article_data)
        self.db.add_article(article_data)
        
        # Should still have only one article
        count = self.db.get_article_count()
        self.assertEqual(count, 1)

    def test_get_articles(self):
        """Test retrieving articles"""
        # Add multiple articles
        for i in range(5):
            article_data = {
                "title": f"Article {i}",
                "url": f"https://example.com/article{i}",
                "summary": f"Summary {i}",
                "source": "Test Source",
                "published_date": datetime.now(),
            }
            self.db.add_article(article_data)
        
        articles = self.db.get_articles(limit=10)
        self.assertEqual(len(articles), 5)

    def test_search_articles(self):
        """Test searching articles"""
        # Add test articles
        for title in ["Python Web Development", "JavaScript Frameworks", "Python AI"]:
            article_data = {
                "title": title,
                "url": f"https://example.com/{title.replace(' ', '-')}",
                "summary": f"Summary for {title}",
                "source": "Test Source",
                "published_date": datetime.now(),
            }
            self.db.add_article(article_data)
        
        # Search for Python articles
        results = self.db.search_articles("Python", limit=10)
        self.assertEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
