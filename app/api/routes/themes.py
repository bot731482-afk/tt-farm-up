"""
FastAPI routes for theme management
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.automation.theme_filter import ThemeFilterManager, Theme

router = APIRouter(prefix="/api/themes", tags=["themes"])

# Initialize theme manager
theme_manager = ThemeFilterManager()


class ThemeRequest(BaseModel):
    """Request model for creating/updating theme"""
    name: str
    description: str
    keywords: List[str]
    hashtags: List[str]
    blacklist_keywords: Optional[List[str]] = []


class ThemeResponse(BaseModel):
    """Response model for theme"""
    id: int
    name: str
    description: str
    keywords: List[str]
    hashtags: List[str]
    blacklist_keywords: List[str]
    is_active: bool


@router.get("/", response_model=List[ThemeResponse])
async def list_themes(active_only: bool = False):
    """Get all themes (optionally filter by active status)"""
    themes = theme_manager.list_themes(active_only=active_only)
    return [
        ThemeResponse(
            id=t.id,
            name=t.name,
            description=t.description,
            keywords=t.keywords,
            hashtags=t.hashtags,
            blacklist_keywords=t.blacklist_keywords,
            is_active=t.is_active
        )
        for t in themes
    ]


@router.get("/{theme_id}", response_model=ThemeResponse)
async def get_theme(theme_id: int):
    """Get theme by ID"""
    theme = theme_manager.get_theme(theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    
    return ThemeResponse(
        id=theme.id,
        name=theme.name,
        description=theme.description,
        keywords=theme.keywords,
        hashtags=theme.hashtags,
        blacklist_keywords=theme.blacklist_keywords,
        is_active=theme.is_active
    )


@router.post("/", response_model=ThemeResponse)
async def create_theme(request: ThemeRequest):
    """Create new theme"""
    theme = theme_manager.create_theme(
        name=request.name,
        description=request.description,
        keywords=request.keywords,
        hashtags=request.hashtags,
        blacklist_keywords=request.blacklist_keywords
    )
    
    return ThemeResponse(
        id=theme.id,
        name=theme.name,
        description=theme.description,
        keywords=theme.keywords,
        hashtags=theme.hashtags,
        blacklist_keywords=theme.blacklist_keywords,
        is_active=theme.is_active
    )


@router.put("/{theme_id}", response_model=ThemeResponse)
async def update_theme(theme_id: int, request: ThemeRequest):
    """Update existing theme"""
    theme = theme_manager.update_theme(
        theme_id=theme_id,
        name=request.name,
        description=request.description,
        keywords=request.keywords,
        hashtags=request.hashtags,
        blacklist_keywords=request.blacklist_keywords
    )
    
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    
    return ThemeResponse(
        id=theme.id,
        name=theme.name,
        description=theme.description,
        keywords=theme.keywords,
        hashtags=theme.hashtags,
        blacklist_keywords=theme.blacklist_keywords,
        is_active=theme.is_active
    )


@router.delete("/{theme_id}")
async def delete_theme(theme_id: int):
    """Delete theme"""
    if not theme_manager.delete_theme(theme_id):
        raise HTTPException(status_code=404, detail="Theme not found")
    
    return {"message": "Theme deleted successfully"}


@router.post("/{theme_id}/toggle")
async def toggle_theme(theme_id: int):
    """Toggle theme active status"""
    theme = theme_manager.toggle_theme(theme_id)
    
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    
    return ThemeResponse(
        id=theme.id,
        name=theme.name,
        description=theme.description,
        keywords=theme.keywords,
        hashtags=theme.hashtags,
        blacklist_keywords=theme.blacklist_keywords,
        is_active=theme.is_active
    )


@router.get("/export/json")
async def export_themes():
    """Export all themes as JSON"""
    json_data = theme_manager.export_themes()
    return {"data": json_data}


@router.post("/import/json")
async def import_themes(data: dict):
    """Import themes from JSON"""
    try:
        json_str = data.get("data", "{}")
        imported = theme_manager.import_themes(json_str)
        return {
            "count": len(imported),
            "themes": [
                {
                    "id": t.id,
                    "name": t.name
                }
                for t in imported
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")
