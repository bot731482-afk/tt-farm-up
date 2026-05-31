"""
Database Models
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Device(Base):
    """Device model"""
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    adb_id = Column(String(100), unique=True, nullable=False)
    is_connected = Column(Boolean, default=False)
    model = Column(String(100))
    android_version = Column(String(50))
    last_seen = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)


class Theme(Base):
    """Theme model"""
    __tablename__ = "themes"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    keywords = Column(Text)  # JSON string
    hashtags = Column(Text)  # JSON string
    blacklist_keywords = Column(Text)  # JSON string
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)


class BotSession(Base):
    """Bot Session model"""
    __tablename__ = "bot_sessions"
    
    id = Column(String(100), primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    theme_id = Column(Integer, ForeignKey("themes.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)  # seconds
    status = Column(String(50))  # running, stopped, paused
    total_videos = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    follows = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    behavior_profile = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)


class VideoInteraction(Base):
    """Video Interaction model"""
    __tablename__ = "video_interactions"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), ForeignKey("bot_sessions.id"))
    video_url = Column(String(255))
    action = Column(String(50))  # like, comment, follow, share
    success = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.now)
