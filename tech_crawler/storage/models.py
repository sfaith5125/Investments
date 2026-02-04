"""Database models for articles"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Article(Base):
    """Article database model"""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False, index=True)
    url = Column(String(1000), unique=True, nullable=False, index=True)
    summary = Column(Text)
    content = Column(Text)
    source = Column(String(100), nullable=False, index=True)
    published_date = Column(DateTime, nullable=False, index=True)
    crawled_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    relevant = Column(Boolean, default=True)
    processed = Column(Boolean, default=False)
    tags = Column(String(500))  # Comma-separated tags

    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:50]}...')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "summary": self.summary,
            "content": self.content,
            "source": self.source,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "crawled_date": self.crawled_date.isoformat() if self.crawled_date else None,
            "relevant": self.relevant,
            "processed": self.processed,
            "tags": self.tags.split(",") if self.tags else [],
        }
