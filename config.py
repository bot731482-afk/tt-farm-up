"""
Configuration settings for tt-farm
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_PATH = os.getenv('DATABASE_PATH', 'tt_farm.db')

# API
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 8000))

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Automation Intervals
CHECK_POSTS_INTERVAL = int(os.getenv('CHECK_POSTS_INTERVAL', 60))
CHECK_WARM_INTERVAL = int(os.getenv('CHECK_WARM_INTERVAL', 300))

# ADB and Device Control
ADB_PATH = os.getenv('ADB_PATH', 'adb')
SCRCPY_PATH = os.getenv('SCRCPY_PATH', 'scrcpy')

# AI Analysis
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
USE_AI_ANALYSIS = os.getenv('USE_AI_ANALYSIS', 'true').lower() == 'true'

# Bot Behavior
DEFAULT_BEHAVIOR_PROFILE = os.getenv('DEFAULT_BEHAVIOR_PROFILE', 'casual')  # casual, active, passive, aggressive
MAX_DAILY_ACTIONS = int(os.getenv('MAX_DAILY_ACTIONS', 500))
SESSION_MAX_DURATION = int(os.getenv('SESSION_MAX_DURATION', 3600))  # seconds

# Content Filtering
ENABLE_CONTENT_FILTERING = os.getenv('ENABLE_CONTENT_FILTERING', 'true').lower() == 'true'
MIN_ENGAGEMENT_RATE = float(os.getenv('MIN_ENGAGEMENT_RATE', 0.0))
