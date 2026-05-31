"""
Bot Scheduler - Manages bot sessions and scheduling
"""
from typing import Optional, Dict, List
import threading
import time
from datetime import datetime, timedelta
from enum import Enum
from app.bot.tiktok_bot import TikTokBot, BotMode
from loguru import logger


class SessionStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


class BotScheduler:
    """Manages bot sessions and scheduling"""
    
    def __init__(self):
        """Initialize scheduler"""
        self.sessions: Dict[str, Dict] = {}
        self.current_session_id: Optional[str] = None
        self.scheduler_thread: Optional[threading.Thread] = None
        self.is_running = False
        logger.info("Bot Scheduler initialized")
    
    def create_session(
        self,
        session_id: str,
        device_id: Optional[str],
        theme_id: int,
        behavior_profile: str = "casual",
        duration: int = 3600,
        mode: BotMode = BotMode.MOCK
    ) -> Dict:
        """Create new bot session"""
        logger.info(f"Creating session {session_id}")
        
        bot = TikTokBot(
            device_id=device_id,
            behavior_profile=behavior_profile,
            mode=mode
        )
        
        session = {
            "id": session_id,
            "device_id": device_id,
            "theme_id": theme_id,
            "bot": bot,
            "status": SessionStatus.IDLE,
            "start_time": None,
            "end_time": None,
            "duration": duration,
            "thread": None,
            "stats": {}
        }
        
        self.sessions[session_id] = session
        return session
    
    def start_session(self, session_id: str):
        """Start a session"""
        if session_id not in self.sessions:
            logger.error(f"Session {session_id} not found")
            return
        
        session = self.sessions[session_id]
        logger.info(f"Starting session {session_id}")
        
        session["status"] = SessionStatus.RUNNING
        session["start_time"] = datetime.now()
        
        # Run bot in separate thread
        thread = threading.Thread(
            target=session["bot"].start_session,
            args=(session["theme_id"], session["duration"])
        )
        thread.daemon = True
        thread.start()
        session["thread"] = thread
        
        self.current_session_id = session_id
    
    def stop_session(self, session_id: str):
        """Stop a session"""
        if session_id not in self.sessions:
            logger.error(f"Session {session_id} not found")
            return
        
        session = self.sessions[session_id]
        logger.info(f"Stopping session {session_id}")
        
        session["bot"].stop_session()
        session["status"] = SessionStatus.STOPPED
        session["end_time"] = datetime.now()
        session["stats"] = session["bot"].get_stats()
        
        if self.current_session_id == session_id:
            self.current_session_id = None
    
    def pause_session(self, session_id: str):
        """Pause a session"""
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        session["bot"].is_running = False
        session["status"] = SessionStatus.PAUSED
        logger.info(f"Session {session_id} paused")
    
    def resume_session(self, session_id: str):
        """Resume a paused session"""
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        session["bot"].is_running = True
        session["status"] = SessionStatus.RUNNING
        logger.info(f"Session {session_id} resumed")
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session info"""
        return self.sessions.get(session_id)
    
    def list_sessions(self) -> List[Dict]:
        """List all sessions"""
        return list(self.sessions.values())
    
    def get_session_stats(self, session_id: str) -> Dict:
        """Get session statistics"""
        if session_id not in self.sessions:
            return {}
        
        session = self.sessions[session_id]
        return {
            "id": session_id,
            "status": session["status"].value,
            "start_time": session["start_time"].isoformat() if session["start_time"] else None,
            "end_time": session["end_time"].isoformat() if session["end_time"] else None,
            "stats": session["bot"].get_stats()
        }
    
    def schedule_recurring(
        self,
        session_id_prefix: str,
        device_id: Optional[str],
        theme_id: int,
        start_hour: int,
        end_hour: int,
        duration: int = 3600,
        mode: BotMode = BotMode.MOCK
    ):
        """Schedule recurring bot sessions"""
        logger.info(
            f"Scheduling recurring sessions from {start_hour}:00 to {end_hour}:00"
        )
        
        if not self.is_running:
            self.is_running = True
            self.scheduler_thread = threading.Thread(
                target=self._scheduler_loop,
                kwargs={
                    "session_id_prefix": session_id_prefix,
                    "device_id": device_id,
                    "theme_id": theme_id,
                    "start_hour": start_hour,
                    "end_hour": end_hour,
                    "duration": duration,
                    "mode": mode
                }
            )
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
    
    def _scheduler_loop(
        self,
        session_id_prefix: str,
        device_id: Optional[str],
        theme_id: int,
        start_hour: int,
        end_hour: int,
        duration: int,
        mode: BotMode
    ):
        """Main scheduler loop"""
        while self.is_running:
            now = datetime.now()
            current_hour = now.hour
            
            # Check if within scheduling window
            if start_hour <= current_hour < end_hour:
                if self.current_session_id is None:
                    session_id = f"{session_id_prefix}_{now.timestamp()}"
                    self.create_session(
                        session_id,
                        device_id,
                        theme_id,
                        duration=duration,
                        mode=mode
                    )
                    self.start_session(session_id)
            else:
                # Stop current session if outside window
                if self.current_session_id:
                    self.stop_session(self.current_session_id)
            
            time.sleep(60)  # Check every minute
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        logger.info("Stopping scheduler")
        self.is_running = False
        
        # Stop all running sessions
        for session in self.sessions.values():
            if session["status"] == SessionStatus.RUNNING:
                session["bot"].stop_session()
