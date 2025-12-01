"""Database models for the logger application."""
from datetime import datetime
from typing import Optional
import json

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Log(Base):
    """Log entry model."""
    
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False, index=True)
    original_text = Column(Text, nullable=True)
    image_path = Column(String(500), nullable=True)
    ai_summary = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    tags = Column(JSON, nullable=True)
    duration_estimate = Column(Integer, nullable=True)  # in minutes
    
    def __repr__(self):
        return f"<Log(id={self.id}, category={self.category}, created_at={self.created_at})>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "original_text": self.original_text,
            "image_path": self.image_path,
            "ai_summary": self.ai_summary,
            "category": self.category,
            "tags": self.tags,
            "duration_estimate": self.duration_estimate,
        }


def init_database(database_url: str):
    """Initialize database and create all tables."""
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    """Get a new database session."""
    Session = sessionmaker(bind=engine)
    return Session()

