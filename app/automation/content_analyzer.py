"""
AI-powered content analyzer with DeepSeek API integration
"""
import os
import requests
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ContentCategory(Enum):
    MUSIC = "music"
    DANCE = "dance"
    COMEDY = "comedy"
    SPORTS = "sports"
    EDUCATION = "education"
    LIFESTYLE = "lifestyle"
    TECH = "tech"
    BEAUTY = "beauty"
    FOOD = "food"
    TRAVEL = "travel"
    ART = "art"
    GAMING = "gaming"
    CRYPTO = "crypto"
    BUSINESS = "business"
    OTHER = "other"


@dataclass
class AnalysisResult:
    """Result of AI content analysis"""
    category: ContentCategory
    keywords: List[str]
    hashtags: List[str]
    blacklist_keywords: List[str]
    confidence: float
    description: str


class DeepSeekAnalyzer:
    """AI-powered content analyzer using DeepSeek API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize DeepSeek analyzer
        
        Args:
            api_key: DeepSeek API key (if None, uses DEEPSEEK_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError(
                "DeepSeek API key not provided. "
                "Set DEEPSEEK_API_KEY environment variable or pass it as argument."
            )
    
    def analyze_keywords(self, keywords: str) -> AnalysisResult:
        """
        Analyze user-provided keywords and auto-detect theme
        
        Args:
            keywords: User input (e.g. "funny videos, laughing, comedy sketches")
        
        Returns:
            AnalysisResult with detected category, keywords, hashtags, etc.
        """
        prompt = f"""Analyze the following user input and determine the content theme/category.

User input: "{keywords}"

Please provide:
1. Main category (must be one of: music, dance, comedy, sports, education, lifestyle, tech, beauty, food, travel, art, gaming, crypto, business, other)
2. Relevant keywords (list 5-10)
3. Popular hashtags (list 5-10 without the #)
4. Content to avoid/blacklist (list 3-5 keywords)
5. Confidence level (0.0-1.0)
6. Brief description of the theme

Format your response as JSON with these exact keys:
{{
    "category": "category_name",
    "keywords": ["keyword1", "keyword2", ...],
    "hashtags": ["hashtag1", "hashtag2", ...],
    "blacklist_keywords": ["bad1", "bad2", ...],
    "confidence": 0.95,
    "description": "Brief description"
}}

Only respond with valid JSON, no other text."""
        
        try:
            response = self._call_deepseek_api(prompt)
            result = self._parse_response(response, keywords)
            return result
        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
            return self._create_fallback_result(keywords)
    
    def _call_deepseek_api(self, prompt: str) -> str:
        """Call DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    
    def _parse_response(self, response_text: str, original_keywords: str) -> AnalysisResult:
        """Parse DeepSeek API response"""
        try:
            data = json.loads(response_text)
            
            # Validate category
            try:
                category = ContentCategory[data.get('category', 'other').upper()]
            except KeyError:
                category = ContentCategory.OTHER
            
            return AnalysisResult(
                category=category,
                keywords=data.get('keywords', []),
                hashtags=data.get('hashtags', []),
                blacklist_keywords=data.get('blacklist_keywords', []),
                confidence=float(data.get('confidence', 0.8)),
                description=data.get('description', '')
            )
        except json.JSONDecodeError:
            return self._create_fallback_result(original_keywords)
    
    def _create_fallback_result(self, keywords: str) -> AnalysisResult:
        """Create fallback result if API fails"""
        keywords_list = [kw.strip() for kw in keywords.split(',')]
        
        return AnalysisResult(
            category=ContentCategory.OTHER,
            keywords=keywords_list,
            hashtags=keywords_list,
            blacklist_keywords=[],
            confidence=0.5,
            description=f"Auto-detected from user input: {keywords}"
        )
    
    def refine_analysis(self, keywords: str, user_feedback: str) -> AnalysisResult:
        """
        Refine analysis based on user feedback
        
        Args:
            keywords: Original keywords
            user_feedback: User's feedback/corrections
        
        Returns:
            Refined AnalysisResult
        """
        prompt = f"""Refine the content theme analysis based on user feedback.

Original input: "{keywords}"
User feedback: "{user_feedback}"

Please provide updated:
1. Main category (must be one of: music, dance, comedy, sports, education, lifestyle, tech, beauty, food, travel, art, gaming, crypto, business, other)
2. Relevant keywords (list 5-10)
3. Popular hashtags (list 5-10 without the #)
4. Content to avoid/blacklist (list 3-5 keywords)
5. Confidence level (0.0-1.0)
6. Brief description

Format as JSON with keys: category, keywords, hashtags, blacklist_keywords, confidence, description
Only respond with valid JSON, no other text."""
        
        try:
            response = self._call_deepseek_api(prompt)
            return self._parse_response(response, keywords)
        except Exception as e:
            print(f"Error refining analysis: {e}")
            return self._create_fallback_result(keywords)
    
    def batch_analyze(self, keywords_list: List[str]) -> List[Tuple[str, AnalysisResult]]:
        """
        Analyze multiple keyword sets
        
        Args:
            keywords_list: List of keyword strings
        
        Returns:
            List of (keywords, AnalysisResult) tuples
        """
        results = []
        for keywords in keywords_list:
            try:
                result = self.analyze_keywords(keywords)
                results.append((keywords, result))
            except Exception as e:
                print(f"Error analyzing '{keywords}': {e}")
                results.append((keywords, self._create_fallback_result(keywords)))
        
        return results


class HybridAnalyzer:
    """Combines rule-based and AI analysis"""
    
    # Fallback rule-based categories
    RULE_BASED_CATEGORIES = {
        ContentCategory.MUSIC: ["music", "song", "beat", "remix", "cover", "artist", "singer", "audio"],
        ContentCategory.DANCE: ["dance", "dancing", "choreography", "tiktok dance", "hiphop", "freestyle", "move"],
        ContentCategory.COMEDY: ["funny", "comedy", "laugh", "meme", "joke", "hilarious", "lol", "humor"],
        ContentCategory.SPORTS: ["sports", "football", "basketball", "soccer", "gym", "workout", "fitness", "athlete"],
        ContentCategory.EDUCATION: ["tutorial", "learn", "education", "tips", "guide", "howto", "diy", "course"],
        ContentCategory.LIFESTYLE: ["lifestyle", "daily", "morning", "routine", "vlog", "life", "dayinmylife"],
        ContentCategory.TECH: ["tech", "gadget", "phone", "app", "software", "coding", "tech tips", "innovation"],
        ContentCategory.BEAUTY: ["beauty", "makeup", "skincare", "cosmetics", "fashion", "style", "hair"],
        ContentCategory.FOOD: ["food", "cooking", "recipe", "eat", "restaurant", "cuisine", "chef", "cooking"],
        ContentCategory.TRAVEL: ["travel", "trip", "adventure", "explore", "tourism", "destination", "vacation"],
        ContentCategory.ART: ["art", "drawing", "painting", "creative", "design", "artist", "creative"],
        ContentCategory.GAMING: ["gaming", "game", "gamer", "esports", "gameplay", "stream", "video game"],
        ContentCategory.CRYPTO: ["crypto", "bitcoin", "ethereum", "nft", "blockchain", "trading", "defi"],
        ContentCategory.BUSINESS: ["business", "entrepreneurship", "startup", "money", "marketing", "finance"],
    }
    
    def __init__(self, api_key: Optional[str] = None, use_ai: bool = True):
        """
        Initialize hybrid analyzer
        
        Args:
            api_key: DeepSeek API key
            use_ai: Whether to use AI analysis (fallback to rules if False or API unavailable)
        """
        self.use_ai = use_ai
        self.deepseek_analyzer = None
        
        if use_ai:
            try:
                self.deepseek_analyzer = DeepSeekAnalyzer(api_key)
            except ValueError as e:
                print(f"Warning: {e}. Will use rule-based analysis.")
                self.use_ai = False
    
    def analyze(self, keywords: str, prefer_ai: bool = True) -> AnalysisResult:
        """
        Analyze keywords using AI or rule-based method
        
        Args:
            keywords: User input keywords
            prefer_ai: Prefer AI analysis if available
        
        Returns:
            AnalysisResult
        """
        if prefer_ai and self.use_ai and self.deepseek_analyzer:
            try:
                return self.deepseek_analyzer.analyze_keywords(keywords)
            except Exception as e:
                print(f"AI analysis failed, falling back to rules: {e}")
        
        # Fallback to rule-based analysis
        return self._rule_based_analyze(keywords)
    
    def _rule_based_analyze(self, keywords: str) -> AnalysisResult:
        """Rule-based analysis fallback"""
        keywords_lower = keywords.lower()
        category_scores = {}
        
        for category, rules in self.RULE_BASED_CATEGORIES.items():
            score = sum(1 for rule in rules if rule in keywords_lower)
            if score > 0:
                category_scores[category] = score
        
        if not category_scores:
            category = ContentCategory.OTHER
            confidence = 0.3
        else:
            category = max(category_scores, key=category_scores.get)
            confidence = min(0.85, 0.5 + len(category_scores) * 0.1)
        
        keywords_list = [kw.strip() for kw in keywords.split(',')]
        
        return AnalysisResult(
            category=category,
            keywords=keywords_list,
            hashtags=[kw.replace(' ', '') for kw in keywords_list],
            blacklist_keywords=[],
            confidence=confidence,
            description=f"Rule-based analysis for {category.value}"
        )
