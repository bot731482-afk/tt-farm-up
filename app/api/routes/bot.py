"""
FastAPI routes for bot control
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.scheduler.scheduler import BotScheduler, SessionStatus
from app.bot.tiktok_bot import BotMode
from loguru import logger

router = APIRouter(prefix="/api/bot", tags=["bot"])

# Global scheduler instance
scheduler = BotScheduler()


class SessionCreateRequest(BaseModel):
    """Request model for creating session"""
    device_id: Optional[str] = None
    theme_id: int
    behavior_profile: str = "casual"
    duration: int = 3600
    mode: str = "mock"  # mock or real


class SessionResponse(BaseModel):
    """Response model for session"""
    id: str
    device_id: Optional[str]
    theme_id: int
    status: str
    start_time: Optional[str]
    end_time: Optional[str]
    stats: dict


@router.post("/sessions", response_model=SessionResponse)
async def create_session(request: SessionCreateRequest):
    """Create new bot session"""
    try:
        mode = BotMode.REAL if request.mode == "real" else BotMode.MOCK
        
        # Generate session ID
        import time
        session_id = f"session_{int(time.time())}"
        
        # Create session
        session = scheduler.create_session(
            session_id=session_id,
            device_id=request.device_id,
            theme_id=request.theme_id,
            behavior_profile=request.behavior_profile,
            duration=request.duration,
            mode=mode
        )
        
        logger.info(f"Created session {session_id}")
        
        return SessionResponse(
            id=session["id"],
            device_id=session["device_id"],
            theme_id=session["theme_id"],
            status=session["status"].value,
            start_time=None,
            end_time=None,
            stats={}
        )
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions/{session_id}/start")
async def start_session(session_id: str):
    """Start a session"""
    try:
        scheduler.start_session(session_id)
        logger.info(f"Started session {session_id}")
        return {"message": "Session started", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error starting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions/{session_id}/stop")
async def stop_session(session_id: str):
    """Stop a session"""
    try:
        scheduler.stop_session(session_id)
        logger.info(f"Stopped session {session_id}")
        return {"message": "Session stopped", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error stopping session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions/{session_id}/pause")
async def pause_session(session_id: str):
    """Pause a session"""
    try:
        scheduler.pause_session(session_id)
        logger.info(f"Paused session {session_id}")
        return {"message": "Session paused", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error pausing session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions/{session_id}/resume")
async def resume_session(session_id: str):
    """Resume a paused session"""
    try:
        scheduler.resume_session(session_id)
        logger.info(f"Resumed session {session_id}")
        return {"message": "Session resumed", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error resuming session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session info"""
    try:
        stats = scheduler.get_session_stats(session_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Session not found")
        return stats
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions")
async def list_sessions():
    """List all sessions"""
    try:
        sessions = scheduler.list_sessions()
        return {
            "count": len(sessions),
            "sessions": [
                {
                    "id": s["id"],
                    "status": s["status"].value,
                    "theme_id": s["theme_id"],
                    "start_time": s["start_time"].isoformat() if s["start_time"] else None,
                }
                for s in sessions
            ]
        }
    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_bot_status():
    """Get overall bot status"""
    try:
        sessions = scheduler.list_sessions()
        running_count = sum(1 for s in sessions if s["status"] == SessionStatus.RUNNING)
        
        return {
            "total_sessions": len(sessions),
            "running_sessions": running_count,
            "current_session_id": scheduler.current_session_id,
            "scheduler_running": scheduler.is_running
        }
    except Exception as e:
        logger.error(f"Error getting bot status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
