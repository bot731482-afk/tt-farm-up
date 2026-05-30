"""
Theme and content filter management
"""
from typing import List, Optional, Dict
from dataclasses import dataclass
from enum import Enum
import json


@dataclass
class Theme:
    """Content theme configuration"""
    id: int
    name: str
    description: str
    keywords: List[str]
    hashtags: List[str]
    blacklist_keywords: List[str]
    is_active: bool


class ThemeFilterManager:
    """Manages content themes and filtering"""
    
    def __init__(self):
        self.themes: Dict[int, Theme] = {}
        self.next_id = 1
        self._initialize_default_themes()
    
    def _initialize_default_themes(self):
        """Initialize with common default themes"""
        default_themes = [
            {
                "name": "Music",
                "description": "Music covers, remixes, and original songs",
                "keywords": ["music", "song", "beat", "remix", "cover", "artist"],
                "hashtags": ["music", "song", "remix", "beat"],
                "blacklist_keywords": ["explicit"]
            },
            {
                "name": "Dance",
                "description": "Dance videos and choreography",
                "keywords": ["dance", "dancing", "choreography", "freestyle", "hiphop"],
                "hashtags": ["dance", "choreography", "tiktokdance", "hiphop"],
                "blacklist_keywords": []
            },
            {
                "name": "Comedy",
                "description": "Funny and humorous content",
                "keywords": ["funny", "comedy", "laugh", "meme", "joke"],
                "hashtags": ["funny", "comedy", "meme", "humor"],
                "blacklist_keywords": []
            },
            {
                "name": "Education",
                "description": "Educational tutorials and tips",
                "keywords": ["tutorial", "learn", "education", "tips", "guide"],
                "hashtags": ["tutorial", "education", "tips", "howto"],
                "blacklist_keywords": []
            },
            {
                "name": "Lifestyle",
                "description": "Daily life and lifestyle content",
                "keywords": ["lifestyle", "daily", "routine", "vlog", "day"],
                "hashtags": ["lifestyle", "dailyvlog", "routine", "dayinmylife"],
                "blacklist_keywords": []
            },
        ]
        
        for theme_data in default_themes:
            theme = Theme(
                id=self.next_id,
                name=theme_data["name"],
                description=theme_data["description"],
                keywords=theme_data["keywords"],
                hashtags=theme_data["hashtags"],
                blacklist_keywords=theme_data["blacklist_keywords"],
                is_active=True
            )
            self.themes[self.next_id] = theme
            self.next_id += 1
    
    def create_theme(
        self,
        name: str,
        description: str,
        keywords: List[str],
        hashtags: List[str],
        blacklist_keywords: List[str] = None
    ) -> Theme:
        """Create new theme"""
        theme = Theme(
            id=self.next_id,
            name=name,
            description=description,
            keywords=keywords,
            hashtags=hashtags,
            blacklist_keywords=blacklist_keywords or [],
            is_active=True
        )
        self.themes[self.next_id] = theme
        self.next_id += 1
        return theme
    
    def get_theme(self, theme_id: int) -> Optional[Theme]:
        """Get theme by ID"""
        return self.themes.get(theme_id)
    
    def list_themes(self, active_only: bool = False) -> List[Theme]:
        """List all themes"""
        themes = list(self.themes.values())
        if active_only:
            themes = [t for t in themes if t.is_active]
        return themes
    
    def update_theme(
        self,
        theme_id: int,
        name: str = None,
        description: str = None,
        keywords: List[str] = None,
        hashtags: List[str] = None,
        blacklist_keywords: List[str] = None,
        is_active: bool = None
    ) -> Optional[Theme]:
        """Update existing theme"""
        theme = self.themes.get(theme_id)
        if not theme:
            return None
        
        if name is not None:
            theme.name = name
        if description is not None:
            theme.description = description
        if keywords is not None:
            theme.keywords = keywords
        if hashtags is not None:
            theme.hashtags = hashtags
        if blacklist_keywords is not None:
            theme.blacklist_keywords = blacklist_keywords
        if is_active is not None:
            theme.is_active = is_active
        
        return theme
    
    def delete_theme(self, theme_id: int) -> bool:
        """Delete theme"""
        if theme_id in self.themes:
            del self.themes[theme_id]
            return True
        return False
    
    def toggle_theme(self, theme_id: int) -> Optional[Theme]:
        """Toggle theme active status"""
        theme = self.themes.get(theme_id)
        if theme:
            theme.is_active = not theme.is_active
        return theme
    
    def get_active_themes(self) -> List[Theme]:
        """Get all active themes"""
        return [t for t in self.themes.values() if t.is_active]
    
    def matches_theme(self, theme_id: int, text: str) -> bool:
        """Check if text matches theme"""
        theme = self.themes.get(theme_id)
        if not theme:
            return False
        
        text_lower = text.lower()
        
        # Check if contains any keyword
        has_keyword = any(kw.lower() in text_lower for kw in theme.keywords)
        
        # Check blacklist
        has_blacklist = any(kw.lower() in text_lower for kw in theme.blacklist_keywords)
        
        return has_keyword and not has_blacklist
    
    def export_themes(self) -> str:
        """Export themes as JSON"""
        themes_data = []
        for theme in self.themes.values():
            themes_data.append({
                'id': theme.id,
                'name': theme.name,
                'description': theme.description,
                'keywords': theme.keywords,
                'hashtags': theme.hashtags,
                'blacklist_keywords': theme.blacklist_keywords,
                'is_active': theme.is_active
            })
        return json.dumps(themes_data, indent=2)
    
    def import_themes(self, json_str: str) -> List[Theme]:
        """Import themes from JSON"""
        themes_data = json.loads(json_str)
        imported = []
        
        for data in themes_data:
            theme = self.create_theme(
                name=data.get('name'),
                description=data.get('description'),
                keywords=data.get('keywords', []),
                hashtags=data.get('hashtags', []),
                blacklist_keywords=data.get('blacklist_keywords', [])
            )
            imported.append(theme)
        
        return imported
