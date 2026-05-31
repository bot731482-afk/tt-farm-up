"""
Database Connection and Session Management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.models import Base
import config
from loguru import logger

# Create engine
engine = create_engine(f"sqlite:///{config.DATABASE_PATH}", echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
    logger.info(f"Database initialized at {config.DATABASE_PATH}")


def get_db() -> Session:
    """Get database session"""
    return SessionLocal()
