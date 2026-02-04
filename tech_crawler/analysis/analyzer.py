"""Article analyzer for relevance and tag extraction"""

import logging
import re
from typing import List, Tuple
from datetime import datetime

from ..config import Settings

logger = logging.getLogger(__name__)


class ArticleAnalyzer:
    """Analyzer for articles related to tech investments"""

    def __init__(self):
        """Initialize analyzer with company names and trends"""
        self.companies = {c["name"].lower(): c["ticker"] for c in Settings.TECH_COMPANIES}
        self.trends = [t.lower() for t in Settings.TECH_TRENDS]

    def analyze_article(self, title: str, summary: str, content: str = "") -> dict:
        """
        Analyze article for relevance and extract tags.
        
        Args:
            title: Article title
            summary: Article summary
            content: Full article content
            
        Returns:
            dict: Analysis results with relevance score and tags
        """
        full_text = f"{title} {summary} {content}".lower()
        
        # Check relevance
        is_relevant = self._check_relevance(full_text)
        relevance_score = self._calculate_relevance_score(full_text)
        
        # Extract companies mentioned
        companies_mentioned = self._extract_companies(full_text)
        
        # Extract trends
        trends_mentioned = self._extract_trends(full_text)
        
        # Generate tags
        tags = companies_mentioned + trends_mentioned
        
        return {
            "is_relevant": is_relevant,
            "relevance_score": relevance_score,
            "companies": companies_mentioned,
            "trends": trends_mentioned,
            "tags": tags,
        }

    def _check_relevance(self, text: str) -> bool:
        """Check if article is relevant to tech investing"""
        # Must contain at least one company or trend
        has_company = any(company in text for company in self.companies.keys())
        has_trend = any(trend in text for trend in self.trends)
        
        # Exclude irrelevant keywords
        irrelevant_keywords = [
            "gaming",
            "entertainment",
            "sports",
            "celebrity",
        ]
        has_irrelevant = any(keyword in text for keyword in irrelevant_keywords)
        
        return (has_company or has_trend) and not has_irrelevant

    def _calculate_relevance_score(self, text: str) -> float:
        """Calculate relevance score between 0 and 1"""
        score = 0.0
        max_score = 0.0
        
        # Company mentions (high weight)
        for company in self.companies.keys():
            count = text.count(company)
            score += min(count * 0.3, 0.3)
            max_score += 0.3
        
        # Trend mentions (medium weight)
        for trend in self.trends:
            if trend in text:
                score += 0.2
                max_score += 0.2
        
        # Keywords like "invest", "stock", "market"
        investment_keywords = ["invest", "stock", "market", "ipo", "acquisition"]
        for keyword in investment_keywords:
            if keyword in text:
                score += 0.1
                max_score += 0.1
        
        if max_score == 0:
            return 0.0
        
        return min(score / max_score, 1.0)

    def _extract_companies(self, text: str) -> List[str]:
        """Extract company names and tickers mentioned in text"""
        companies = []
        
        for company_name, ticker in self.companies.items():
            if company_name in text:
                companies.append(f"{ticker} ({company_name.title()})")
        
        return list(set(companies))

    def _extract_trends(self, text: str) -> List[str]:
        """Extract tech trends mentioned in text"""
        trends = []
        
        for trend in self.trends:
            if trend in text:
                trends.append(trend.replace(" ", "_").upper())
        
        return list(set(trends))

    def batch_analyze(self, articles: List[dict]) -> List[dict]:
        """Analyze multiple articles"""
        results = []
        
        for article in articles:
            analysis = self.analyze_article(
                article.get("title", ""),
                article.get("summary", ""),
                article.get("content", ""),
            )
            article.update(analysis)
            results.append(article)
        
        return results
