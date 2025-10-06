"""
Main FastAPI application entry point for the Music Ranking App.
"""

import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database components
from .database import init_db, get_db
from .api import api_router
from .middleware.cors import register_middleware
from .config import settings
from .services.spotify_auth import SpotifyAuthService, spotify_auth_service

# Create FastAPI instance
app = FastAPI(
    title="Music Ranking API",
    description="API for music ranking application with Spotify integration and AI recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Register middleware (e.g., CORS)
register_middleware(app)

# Include API routes
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        init_db()
        print("✅ Database initialized successfully")
        # Initialize Spotify app-level token refresh
        if settings.spotify_client_id and settings.spotify_client_secret:
            # Create singleton instance if not created yet
            global spotify_auth_service
            if spotify_auth_service is None:
                spotify_auth_service = SpotifyAuthService(
                    client_id=settings.spotify_client_id,
                    client_secret=settings.spotify_client_secret,
                )
            await spotify_auth_service.start()
            print("🎧 Spotify client token refresh started")
        else:
            print("⚠️ Spotify credentials not configured; skipping token refresh")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Music Ranking API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/spotify/auth")
async def spotify_auth():
    
    return {
        "message": "Spotify authentication endpoint"
    }

@app.get("/spotify/token")
async def get_spotify_token():
    """Return current app-level Spotify access token."""
    if spotify_auth_service and spotify_auth_service.access_token:
        return {"access_token": spotify_auth_service.access_token}
    return JSONResponse(
        status_code=503,
        content={"detail": "Spotify token not initialized"}
    )


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint with database connectivity test."""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": "music-ranking-api",
        "database": db_status,
        "environment": os.getenv("NODE_ENV", "development")
    }


@app.get("/api/test")
async def test_endpoint():
    """Test endpoint for frontend-backend connectivity."""
    return {
        "message": "Backend connection successful!",
        "timestamp": "2024-01-01T00:00:00Z",
        "features": [
            "Music rating and reviews",
            "Spotify integration",
            "AI-powered recommendations",
            "Playlist generation"
        ]
    }


# Exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )