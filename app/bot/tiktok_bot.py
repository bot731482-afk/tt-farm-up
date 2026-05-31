"""
TikTok Bot - Main automation logic
"""
import time
import random
from typing import Optional, Dict
from enum import Enum
from app.bot.adb_manager import ADBManager
from app.automation.behavior_simulator import BehaviorSimulator
from app.automation.content_analyzer import HybridAnalyzer
import config
from loguru import logger


class BotMode(Enum):
    REAL = "real"  # Real device via ADB
    MOCK = "mock"  # Mock mode (no device needed)


class TikTokBot:
    """Main TikTok automation bot"""
    
    def __init__(
        self,
        device_id: Optional[str] = None,
        behavior_profile: str = "casual",
        mode: BotMode = BotMode.MOCK
    ):
        """
        Initialize TikTok Bot
        
        Args:
            device_id: Android device ID
            behavior_profile: Behavior profile (casual, active, passive, aggressive)
            mode: Bot mode (REAL or MOCK)
        """
        self.device_id = device_id
        self.behavior_profile = behavior_profile
        self.mode = mode
        self.is_running = False
        self.session_stats = {
            "total_videos": 0,
            "likes": 0,
            "comments": 0,
            "follows": 0,
            "shares": 0,
        }
        
        # Initialize components
        self.behavior_simulator = BehaviorSimulator(profile=behavior_profile)
        self.analyzer = HybridAnalyzer(
            api_key=config.DEEPSEEK_API_KEY,
            use_ai=config.USE_AI_ANALYSIS
        )
        
        # Initialize ADB (only if REAL mode)
        if mode == BotMode.REAL:
            try:
                self.adb = ADBManager(device_id)
                if not self.adb.is_connected():
                    raise RuntimeError("Device not connected")
                logger.info(f"Connected to device: {device_id}")
            except Exception as e:
                logger.warning(f"Could not connect to device: {e}. Using MOCK mode.")
                self.mode = BotMode.MOCK
                self.adb = None
        else:
            self.adb = None
        
        logger.info(f"Bot initialized in {self.mode.value} mode with {behavior_profile} profile")
    
    def start_session(self, theme_id: int, duration: int = 3600):
        """Start a new session"""
        logger.info(f"Starting session for theme {theme_id}, duration {duration}s")
        self.is_running = True
        self.session_stats = {
            "total_videos": 0,
            "likes": 0,
            "comments": 0,
            "follows": 0,
            "shares": 0,
        }
        
        start_time = time.time()
        
        try:
            # Open TikTok app
            self._open_tiktok()
            time.sleep(2)
            
            # Main loop
            while self.is_running and (time.time() - start_time) < duration:
                if self.behavior_simulator.should_stop_session(
                    self.session_stats["total_videos"],
                    duration
                ):
                    break
                
                # Get next action
                action_type, delay, watch_duration = self.behavior_simulator.get_next_action()
                
                # Perform action
                self._perform_action(action_type, watch_duration)
                
                # Add human randomness
                adjusted_delay = self.behavior_simulator.add_human_randomness(delay)
                time.sleep(adjusted_delay)
            
            logger.info(f"Session ended. Stats: {self.session_stats}")
        
        except Exception as e:
            logger.error(f"Session error: {e}")
        
        finally:
            self.is_running = False
    
    def stop_session(self):
        """Stop current session"""
        logger.info("Stopping session")
        self.is_running = False
    
    def _open_tiktok(self):
        """Open TikTok application"""
        if self.mode == BotMode.MOCK:
            logger.info("[MOCK] Opening TikTok app")
            return
        
        logger.info("Opening TikTok app")
        self.adb.execute_command("shell am start -n com.ss.android.ugc.tiktok/.MainActivity")
    
    def _perform_action(self, action_type, watch_duration):
        """Perform an action on TikTok"""
        if action_type.value == "watch":
            self._watch_video(watch_duration[0], watch_duration[1])
        elif action_type.value == "like":
            self._like_video()
        elif action_type.value == "comment":
            self._comment_video()
        elif action_type.value == "follow":
            self._follow_user()
        elif action_type.value == "share":
            self._share_video()
        elif action_type.value == "scroll":
            self._scroll_feed()
    
    def _watch_video(self, min_duration: float, max_duration: float):
        """Watch current video"""
        duration = random.uniform(min_duration, max_duration)
        logger.info(f"Watching video for {duration:.1f}s")
        
        if self.mode == BotMode.MOCK:
            logger.info(f"[MOCK] Watched video")
            self.session_stats["total_videos"] += 1
            return
        
        time.sleep(duration)
        self.session_stats["total_videos"] += 1
    
    def _like_video(self):
        """Like current video"""
        logger.info("Liking video")
        
        if self.mode == BotMode.MOCK:
            logger.info("[MOCK] Liked video")
            self.session_stats["likes"] += 1
            return
        
        # Tap on heart icon (usually at bottom right)
        self.adb.tap(300, 500)
        self.session_stats["likes"] += 1
    
    def _comment_video(self):
        """Leave a comment on video"""
        logger.info("Commenting on video")
        
        if self.mode == BotMode.MOCK:
            logger.info("[MOCK] Commented on video")
            self.session_stats["comments"] += 1
            return
        
        # Tap comment icon
        self.adb.tap(250, 500)
        time.sleep(1)
        
        # Type comment
        comments = ["Nice!", "Love this!", "Amazing!", "So good!"]
        comment = random.choice(comments)
        self.adb.type_text(comment)
        time.sleep(0.5)
        
        # Send
        self.adb.tap(300, 600)
        self.session_stats["comments"] += 1
    
    def _follow_user(self):
        """Follow current user"""
        logger.info("Following user")
        
        if self.mode == BotMode.MOCK:
            logger.info("[MOCK] Followed user")
            self.session_stats["follows"] += 1
            return
        
        # Tap on follow button
        self.adb.tap(350, 100)
        self.session_stats["follows"] += 1
    
    def _share_video(self):
        """Share current video"""
        logger.info("Sharing video")
        
        if self.mode == BotMode.MOCK:
            logger.info("[MOCK] Shared video")
            self.session_stats["shares"] += 1
            return
        
        # Tap share icon
        self.adb.tap(350, 500)
        time.sleep(0.5)
        
        # Share via WhatsApp or similar
        self.adb.tap(200, 300)
        self.session_stats["shares"] += 1
    
    def _scroll_feed(self):
        """Scroll down to next video"""
        logger.info("Scrolling to next video")
        
        if self.mode == BotMode.MOCK:
            logger.info("[MOCK] Scrolled to next video")
            self.session_stats["total_videos"] += 1
            return
        
        # Swipe up to scroll
        scroll_behavior = self.behavior_simulator.get_scroll_behavior()
        self.adb.swipe(
            240, 400,
            240, 400 - scroll_behavior["scroll_distance"],
            int(scroll_behavior["scroll_speed"] * 1000)
        )
    
    def get_stats(self) -> Dict:
        """Get current session statistics"""
        return {
            **self.session_stats,
            "mode": self.mode.value,
            "profile": self.behavior_profile,
            "is_running": self.is_running
        }
