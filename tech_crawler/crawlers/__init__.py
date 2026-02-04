"""Crawler modules for news aggregation"""

from .base_crawler import BaseCrawler
from .rss_crawler import RSSCrawler
from .html_crawler import HTMLCrawler

__all__ = ["BaseCrawler", "RSSCrawler", "HTMLCrawler"]
