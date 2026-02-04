"""Main entry point for Tech Investment Crawler"""

import logging
import sys
import time
from typing import List

from tech_crawler.config import Settings
from tech_crawler.crawlers import RSSCrawler, HTMLCrawler
from tech_crawler.storage import Database
from tech_crawler.analysis import ArticleAnalyzer
from tech_crawler.blog import BlogPublisher

# Configure logging
logging.basicConfig(
    level=logging.INFO if not Settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class TechInvestmentCrawler:
    """Main crawler orchestrator"""

    def __init__(self):
        """Initialize crawler with all components"""
        self.db = Database()
        self.analyzer = ArticleAnalyzer()
        self.publisher = BlogPublisher()
        self.crawlers = []
        self._init_crawlers()

    def _init_crawlers(self) -> None:
        """Initialize crawlers for all configured sources"""
        for source in Settings.NEWS_SOURCES:
            try:
                if source["type"] == "rss":
                    crawler = RSSCrawler(source["name"], source["url"])
                elif source["type"] == "html":
                    crawler = HTMLCrawler(source["name"], source["url"])
                else:
                    logger.warning(f"Unknown source type: {source['type']}")
                    continue

                self.crawlers.append(crawler)
                logger.info(f"Initialized crawler for {source['name']}")

            except Exception as e:
                logger.error(f"Error initializing crawler for {source['name']}: {str(e)}")

    def run_crawl(self, save_to_db: bool = True, analyze: bool = True) -> dict:
        """
        Run the crawler for all sources.
        
        Args:
            save_to_db: Whether to save articles to database
            analyze: Whether to analyze articles for relevance
            
        Returns:
            dict: Crawl statistics
        """
        stats = {
            "total_articles": 0,
            "relevant_articles": 0,
            "sources_crawled": 0,
            "errors": 0,
        }

        for crawler in self.crawlers:
            try:
                logger.info(f"Crawling {crawler.source_name}...")

                # Fetch and parse
                if not crawler.fetch():
                    logger.warning(f"Failed to fetch from {crawler.source_name}")
                    stats["errors"] += 1
                    continue

                articles = crawler.parse()
                stats["total_articles"] += len(articles)

                # Analyze if requested
                if analyze:
                    articles = self.analyzer.batch_analyze(articles)
                    relevant = [a for a in articles if a.get("is_relevant", False)]
                    stats["relevant_articles"] += len(relevant)
                else:
                    relevant = articles

                # Save to database if requested
                if save_to_db:
                    self.db.add_articles_batch(relevant)

                stats["sources_crawled"] += 1

                # Rate limiting
                time.sleep(Settings.RATE_LIMIT_DELAY)

            except Exception as e:
                logger.error(
                    f"Error crawling {crawler.source_name}: {str(e)}"
                )
                stats["errors"] += 1

        # Log summary
        logger.info(
            f"Crawl complete - Total: {stats['total_articles']}, "
            f"Relevant: {stats['relevant_articles']}, "
            f"Sources: {stats['sources_crawled']}, "
            f"Errors: {stats['errors']}"
        )

        return stats

    def search_articles(self, keyword: str, limit: int = 20) -> List[dict]:
        """Search articles by keyword"""
        articles = self.db.search_articles(keyword, limit)
        return [a.to_dict() for a in articles]

    def get_recent_articles(
        self,
        limit: int = 50,
        days_back: int = 7,
    ) -> List[dict]:
        """Get recent articles"""
        articles = self.db.get_articles(limit=limit, days_back=days_back)
        return [a.to_dict() for a in articles]

    def get_statistics(self) -> dict:
        """Get crawler statistics"""
        return {
            "total_articles": self.db.get_article_count(),
            "sources": self.db.get_sources(),
        }


def main():
    """Main execution function"""
    logger.info(f"Starting {Settings.APP_NAME} v{Settings.APP_VERSION}")

    try:
        crawler = TechInvestmentCrawler()

        # Run crawl
        stats = crawler.run_crawl(save_to_db=True, analyze=True)

        # Get recent articles
        recent = crawler.get_recent_articles(limit=10)
        logger.info(f"Recent articles: {len(recent)}")
        for article in recent[:3]:
            logger.info(
                f"  - {article['title'][:60]}... ({article['source']})"
            )

        # Get statistics
        stats = crawler.get_statistics()
        logger.info(f"Database statistics: {stats}")

        logger.info("Crawler execution completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
