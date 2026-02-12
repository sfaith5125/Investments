"""Database management for articles"""

import logging
import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from .models import Base, Article
from ..config import Settings

logger = logging.getLogger(__name__)


class Database:
    """Database manager for articles"""

    def __init__(self, database_url: str = None):
        """Initialize database connection"""
        self.database_url = database_url or Settings.DATABASE_URL
        self.engine = create_engine(
            self.database_url,
            echo=Settings.DEBUG,
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._init_db()

    @staticmethod
    def _serialize_tags(tags) -> str:
        if not tags:
            return ""
        if isinstance(tags, str):
            return tags
        if isinstance(tags, (list, tuple, set)):
            return ",".join(str(tag).strip() for tag in tags if str(tag).strip())
        return str(tags)

    def _init_db(self) -> None:
        """Initialize database tables"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise

    def add_article(self, article_data: dict) -> Optional[Article]:
        """Add or update an article"""
        session = self.SessionLocal()
        try:
            # Check if article already exists
            existing = session.query(Article).filter(
                Article.url == article_data["url"]
            ).first()

            if existing:
                # Update existing article
                existing.updated_date = datetime.now(timezone.utc)
                existing.summary = article_data.get("summary", existing.summary)
                existing.content = article_data.get("content", existing.content)
                existing.tags = self._serialize_tags(article_data.get("tags")) or existing.tags
                logger.debug(f"Updated article: {article_data['title'][:50]}...")
            else:
                # Create new article
                article = Article(
                    title=article_data["title"],
                    url=article_data["url"],
                    summary=article_data.get("summary", ""),
                    content=article_data.get("content", ""),
                    source=article_data.get("source", "Unknown"),
                    published_date=article_data.get("published_date", datetime.now(timezone.utc)),
                    tags=self._serialize_tags(article_data.get("tags")),
                )
                session.add(article)
                logger.debug(f"Added article: {article_data['title'][:50]}...")

            session.commit()
            return existing or article

        except Exception as e:
            session.rollback()
            logger.error(f"Error adding article: {str(e)}")
            return None
        finally:
            session.close()

    def add_articles_batch(self, articles: List[dict]) -> int:
        """Add multiple articles at once"""
        session = self.SessionLocal()
        added_count = 0

        try:
            for article_data in articles:
                existing = session.query(Article).filter(
                    Article.url == article_data["url"]
                ).first()

                if not existing:
                    article = Article(
                        title=article_data["title"],
                        url=article_data["url"],
                        summary=article_data.get("summary", ""),
                        content=article_data.get("content", ""),
                        source=article_data.get("source", "Unknown"),
                        published_date=article_data.get("published_date", datetime.now(timezone.utc)),
                        tags=self._serialize_tags(article_data.get("tags")),
                    )
                    session.add(article)
                    added_count += 1
                else:
                    existing.summary = article_data.get("summary", existing.summary)
                    existing.content = article_data.get("content", existing.content)
                    serialized_tags = self._serialize_tags(article_data.get("tags"))
                    if serialized_tags:
                        existing.tags = serialized_tags

            session.commit()
            logger.info(f"Added {added_count} new articles to database")
            return added_count

        except Exception as e:
            session.rollback()
            logger.error(f"Error adding articles batch: {str(e)}")
            return 0
        finally:
            session.close()

    def get_articles(
        self,
        limit: int = 100,
        offset: int = 0,
        source: Optional[str] = None,
        days_back: Optional[int] = None,
    ) -> List[Article]:
        """Get articles with optional filters"""
        session = self.SessionLocal()

        try:
            query = session.query(Article).order_by(Article.published_date.desc())

            if source:
                query = query.filter(Article.source == source)

            if days_back:
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
                query = query.filter(Article.published_date >= cutoff_date)

            articles = query.limit(limit).offset(offset).all()
            return articles

        except Exception as e:
            logger.error(f"Error retrieving articles: {str(e)}")
            return []
        finally:
            session.close()

    def search_articles(
        self,
        keyword: str,
        limit: int = 50,
    ) -> List[Article]:
        """Search articles by keyword"""
        session = self.SessionLocal()

        try:
            articles = (
                session.query(Article)
                .filter(
                    (Article.title.ilike(f"%{keyword}%")) |
                    (Article.summary.ilike(f"%{keyword}%")) |
                    (Article.content.ilike(f"%{keyword}%"))
                )
                .order_by(Article.published_date.desc())
                .limit(limit)
                .all()
            )
            return articles

        except Exception as e:
            logger.error(f"Error searching articles: {str(e)}")
            return []
        finally:
            session.close()

    def get_article_count(self) -> int:
        """Get total article count"""
        session = self.SessionLocal()

        try:
            count = session.query(func.count(Article.id)).scalar()
            return count or 0
        except Exception as e:
            logger.error(f"Error getting article count: {str(e)}")
            return 0
        finally:
            session.close()

    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        """Fetch a single article by ID"""
        session = self.SessionLocal()

        try:
            return session.query(Article).filter(Article.id == article_id).first()
        except Exception as e:
            logger.error(f"Error retrieving article {article_id}: {str(e)}")
            return None
        finally:
            session.close()

    def get_sources(self) -> List[str]:
        """Get list of unique sources"""
        session = self.SessionLocal()

        try:
            sources = session.query(Article.source).distinct().all()
            return [s[0] for s in sources]
        except Exception as e:
            logger.error(f"Error getting sources: {str(e)}")
            return []
        finally:
            session.close()
