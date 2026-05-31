"""
FastAPI routes for scheduler
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.scheduler.scheduler import BotScheduler
from app.bot.tiktok_bot import BotMode
from loguru import logger

router = APIRouter(prefix="/api/scheduler", tags=["scheduler"])

scheduler = BotScheduler()


class ScheduleRequest(BaseModel):
    """Request model for scheduling"""
    device_id: Optional[str] = None
    theme_id: int
    start_hour: int
    end_hour: int
    duration: int = 3600
    mode: str = "mock"


@router.post("/schedule")
async def schedule_sessions(request: ScheduleRequest):
    """Schedule recurring bot sessions"""
    try:
        mode = BotMode.REAL if request.mode == "real" else BotMode.MOCK
        
        scheduler.schedule_recurring(
            session_id_prefix="scheduled",
            device_id=request.device_id,
            theme_id=request.theme_id,
            start_hour=request.start_hour,
            end_hour=request.end_hour,
            duration=request.duration,
            mode=mode
        )
        
        logger.info(
            f"Scheduled sessions from {request.start_hour}:00 to {request.end_hour}:00"
        )
        
        return {
            "message": "Sessions scheduled",
            "start_hour": request.start_hour,
            "end_hour": request.end_hour
        }
    except Exception as e:
        logger.error(f"Error scheduling sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop-schedule")
async def stop_schedule():
    """Stop the scheduler"""
    try:
        scheduler.stop_scheduler()
        logger.info("Scheduler stopped")
        return {"message": "Scheduler stopped"}
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")
        raise HTTPException(status_code=500, detail=str(e))
