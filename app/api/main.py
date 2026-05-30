"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import content_filtering, themes
import config

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


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to TT Farm API",
        "docs": "/docs",
        "version": "1.0.0"
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
    import uvicorn
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level=config.LOG_LEVEL.lower()
    )
