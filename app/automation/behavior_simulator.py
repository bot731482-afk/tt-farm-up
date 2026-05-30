"""
Behavior simulator for realistic user-like actions
"""
import random
import time
from typing import List, Tuple, Dict
from enum import Enum
from dataclasses import dataclass


class ActionType(Enum):
    SCROLL = "scroll"
    LIKE = "like"
    COMMENT = "comment"
    FOLLOW = "follow"
    SHARE = "share"
    WATCH = "watch"


@dataclass
class BehaviorPattern:
    """Pattern of user behavior"""
    action: ActionType
    probability: float  # 0.0 to 1.0
    min_delay: float    # seconds
    max_delay: float    # seconds
    duration: Tuple[float, float] = (0, 0)  # for watch action


class BehaviorSimulator:
    """Simulates realistic TikTok user behavior to avoid detection"""
    
    # Different user behavior profiles
    PROFILES = {
        "casual": [
            BehaviorPattern(ActionType.WATCH, 0.95, 3, 8, (5, 15)),
            BehaviorPattern(ActionType.LIKE, 0.3, 1, 3),
            BehaviorPattern(ActionType.COMMENT, 0.05, 2, 5),
            BehaviorPattern(ActionType.SHARE, 0.02, 1, 2),
            BehaviorPattern(ActionType.FOLLOW, 0.05, 1, 3),
        ],
        "active": [
            BehaviorPattern(ActionType.WATCH, 0.90, 2, 6, (4, 12)),
            BehaviorPattern(ActionType.LIKE, 0.6, 0.5, 2),
            BehaviorPattern(ActionType.COMMENT, 0.2, 1, 4),
            BehaviorPattern(ActionType.SHARE, 0.1, 0.5, 2),
            BehaviorPattern(ActionType.FOLLOW, 0.15, 0.5, 2),
        ],
        "passive": [
            BehaviorPattern(ActionType.WATCH, 0.98, 5, 12, (8, 20)),
            BehaviorPattern(ActionType.LIKE, 0.15, 2, 5),
            BehaviorPattern(ActionType.COMMENT, 0.02, 3, 8),
            BehaviorPattern(ActionType.SHARE, 0.01, 2, 4),
            BehaviorPattern(ActionType.FOLLOW, 0.02, 2, 4),
        ],
        "aggressive": [
            BehaviorPattern(ActionType.WATCH, 0.85, 1, 3, (2, 8)),
            BehaviorPattern(ActionType.LIKE, 0.85, 0.2, 1),
            BehaviorPattern(ActionType.COMMENT, 0.35, 0.5, 2),
            BehaviorPattern(ActionType.SHARE, 0.15, 0.5, 1),
            BehaviorPattern(ActionType.FOLLOW, 0.25, 0.3, 1),
        ],
    }
    
    def __init__(self, profile: str = "casual"):
        """
        Initialize behavior simulator
        
        Args:
            profile: One of 'casual', 'active', 'passive', 'aggressive'
        """
        if profile not in self.PROFILES:
            raise ValueError(f"Unknown profile: {profile}. Must be one of {list(self.PROFILES.keys())}")
        
        self.profile = profile
        self.patterns = self.PROFILES[profile]
        self.action_history = []
        self.session_start = time.time()
    
    def get_next_action(self) -> Tuple[ActionType, float, Tuple[float, float]]:
        """
        Get next action with realistic behavior
        
        Returns:
            Tuple of (action_type, delay_before_action, (watch_min, watch_max) for watch actions)
        """
        # Select random action based on probabilities
        rand = random.random()
        cumulative_prob = 0
        
        for pattern in self.patterns:
            cumulative_prob += pattern.probability
            if rand <= cumulative_prob:
                delay = random.uniform(pattern.min_delay, pattern.max_delay)
                # Add slight randomness to delay (gaussian distribution)
                delay += random.gauss(0, delay * 0.1)
                delay = max(0.1, delay)  # Ensure positive
                
                self.action_history.append({
                    'action': pattern.action,
                    'delay': delay,
                    'timestamp': time.time()
                })
                
                return (pattern.action, delay, pattern.duration)
        
        # Fallback: watch video
        return (ActionType.WATCH, random.uniform(3, 8), (5, 15))
    
    def should_stop_session(self, actions_count: int, session_duration: int = 3600) -> bool:
        """
        Determine if session should end (avoid looking too bot-like)
        
        Args:
            actions_count: Number of actions performed
            session_duration: Max session duration in seconds
        
        Returns:
            True if session should end
        """
        elapsed = time.time() - self.session_start
        
        # Check session duration
        if elapsed > session_duration:
            return True
        
        # Check for suspicious action patterns
        if actions_count > 100 and elapsed < 600:  # 100 actions in 10 min
            return True
        
        # Randomly decide (more likely as session goes on)
        probability_stop = (elapsed / session_duration) * 0.5
        return random.random() < probability_stop
    
    def get_typing_speed(self) -> float:
        """Get realistic typing speed (characters per second)"""
        # Humans type 40-60 WPM, ~5 chars per word
        wpm = random.uniform(40, 60)
        chars_per_second = (wpm * 5) / 60
        return chars_per_second + random.gauss(0, 2)  # Add variance
    
    def get_scroll_behavior(self) -> Dict:
        """Get realistic scroll behavior"""
        return {
            'scroll_distance': random.uniform(200, 600),  # pixels
            'scroll_speed': random.uniform(1, 3),  # seconds to scroll
            'jitter': random.uniform(0, 50),  # random pause during scroll
        }
    
    def add_human_randomness(self, delay: float) -> float:
        """
        Add human-like randomness to delay
        
        Args:
            delay: Base delay in seconds
        
        Returns:
            Adjusted delay with human randomness
        """
        # 5% chance of pause
        if random.random() < 0.05:
            delay += random.uniform(1, 3)
        
        # Gaussian noise
        delay += random.gauss(0, delay * 0.15)
        
        return max(0.1, delay)
    
    def get_session_stats(self) -> Dict:
        """Get statistics of current session"""
        action_types = {}
        for action_info in self.action_history:
            action = action_info['action']
            action_types[action] = action_types.get(action, 0) + 1
        
        elapsed = time.time() - self.session_start
        
        return {
            'profile': self.profile,
            'total_actions': len(self.action_history),
            'action_breakdown': action_types,
            'session_duration': elapsed,
            'actions_per_minute': (len(self.action_history) / (elapsed / 60)) if elapsed > 0 else 0,
        }
