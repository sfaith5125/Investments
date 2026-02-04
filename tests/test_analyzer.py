"""Tests for analyzer functionality"""

import unittest

from tech_crawler.analysis import ArticleAnalyzer


class TestArticleAnalyzer(unittest.TestCase):
    """Test ArticleAnalyzer"""

    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = ArticleAnalyzer()

    def test_analyze_relevant_article(self):
        """Test analyzing a relevant article"""
        title = "Apple Announces New AI Features"
        summary = "Apple has announced new artificial intelligence features in its products"
        
        result = self.analyzer.analyze_article(title, summary)
        
        self.assertTrue(result["is_relevant"])
        self.assertGreater(result["relevance_score"], 0)
        self.assertIn("AAPL", str(result["companies"]))

    def test_analyze_irrelevant_article(self):
        """Test analyzing an irrelevant article"""
        title = "Sports Team Announces New Coach"
        summary = "A sports team has hired a new head coach"
        
        result = self.analyzer.analyze_article(title, summary)
        
        # May not be marked as completely irrelevant, but should have low score
        self.assertLess(result["relevance_score"], 0.5)

    def test_extract_companies(self):
        """Test company extraction"""
        text = "microsoft and apple are leading in AI technology"
        
        companies = self.analyzer._extract_companies(text)
        
        self.assertTrue(len(companies) >= 1)
        company_str = str(companies)
        self.assertTrue("MSFT" in company_str or "AAPL" in company_str)

    def test_extract_trends(self):
        """Test trend extraction"""
        text = "machine learning and artificial intelligence are transforming cloud computing"
        
        trends = self.analyzer._extract_trends(text)
        
        self.assertGreater(len(trends), 0)
        trends_str = str(trends)
        self.assertTrue("AI" in trends_str or "MACHINE_LEARNING" in trends_str)


if __name__ == "__main__":
    unittest.main()
