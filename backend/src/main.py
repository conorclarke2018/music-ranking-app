"""
Main FastAPI application entry point for the Music Ranking App.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI(
    title="Music Ranking API",
    description="API for music ranking application with Spotify integration and AI recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Music Ranking API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "music-ranking-api"}


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