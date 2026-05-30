"""
FastAPI routes for content filtering and theme analysis
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.automation.content_analyzer import HybridAnalyzer, ContentCategory
import config

router = APIRouter(prefix="/api/content", tags=["content"])

# Initialize analyzer
analyzer = HybridAnalyzer(
    api_key=config.DEEPSEEK_API_KEY,
    use_ai=config.USE_AI_ANALYSIS
)


class AnalyzeKeywordsRequest(BaseModel):
    """Request model for keyword analysis"""
    keywords: str
    prefer_ai: bool = True


class AnalyzeKeywordsResponse(BaseModel):
    """Response model for keyword analysis"""
    category: str
    keywords: List[str]
    hashtags: List[str]
    blacklist_keywords: List[str]
    confidence: float
    description: str


class BatchAnalyzeRequest(BaseModel):
    """Request model for batch analysis"""
    keywords_list: List[str]


@router.post("/analyze", response_model=AnalyzeKeywordsResponse)
async def analyze_keywords(request: AnalyzeKeywordsRequest):
    """
    Analyze keywords and auto-detect content theme using AI or rule-based method
    
    Example:
        POST /api/content/analyze
        {
            "keywords": "funny videos, laughing, comedy sketches",
            "prefer_ai": true
        }
    """
    try:
        result = analyzer.analyze(request.keywords, prefer_ai=request.prefer_ai)
        
        return AnalyzeKeywordsResponse(
            category=result.category.value,
            keywords=result.keywords,
            hashtags=result.hashtags,
            blacklist_keywords=result.blacklist_keywords,
            confidence=result.confidence,
            description=result.description
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/batch-analyze")
async def batch_analyze(request: BatchAnalyzeRequest):
    """
    Analyze multiple keyword sets
    
    Example:
        POST /api/content/batch-analyze
        {
            "keywords_list": [
                "music videos",
                "dance choreography",
                "comedy sketches"
            ]
        }
    """
    try:
        results = []
        for keywords in request.keywords_list:
            result = analyzer.analyze(keywords, prefer_ai=True)
            results.append({
                "keywords": keywords,
                "category": result.category.value,
                "keywords_detected": result.keywords,
                "hashtags": result.hashtags,
                "confidence": result.confidence
            })
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


@router.get("/categories")
async def get_categories():
    """Get all available content categories"""
    categories = [cat.value for cat in ContentCategory]
    return {"categories": categories}


@router.get("/status")
async def get_analyzer_status():
    """Get analyzer status and capabilities"""
    return {
        "ai_enabled": analyzer.use_ai,
        "analyzer_type": "HybridAnalyzer",
        "fallback_available": True,
        "categories_count": len(ContentCategory),
        "deepseek_configured": bool(config.DEEPSEEK_API_KEY)
    }
