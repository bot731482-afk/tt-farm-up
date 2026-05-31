"""
Main entry point for TT Farm application
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import content_filtering, themes, bot
from app.scheduler.routes import router as scheduler_router
from app.database.database import init_db
from loguru import logger
import config
import sys

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="TT Farm API",
    description="TikTok Automation Platform with AI Content Analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(content_filtering.router)
app.include_router(themes.router)
app.include_router(bot.router)
app.include_router(scheduler_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to TT Farm API",
        "docs": "/docs",
        "version": "1.0.0",
        "ui": "http://localhost:8001"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_enabled": config.USE_AI_ANALYSIS,
        "api_port": config.API_PORT
    }


if __name__ == "__main__":
    logger.info("Starting TT Farm Application...")
    logger.info(f"API will run on http://{config.API_HOST}:{config.API_PORT}")
    logger.info(f"Documentation: http://{config.API_HOST}:{config.API_PORT}/docs")
    logger.info(f"Database: {config.DATABASE_PATH}")
    
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level=config.LOG_LEVEL.lower()
    )
