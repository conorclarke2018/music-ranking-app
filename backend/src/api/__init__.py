"""
API package for FastAPI routers.
"""

from fastapi import APIRouter
from .users import router as users_router
from .music import router as music_router
from .ratings import router as ratings_router
from .playlists import router as playlists_router

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(music_router, prefix="/music", tags=["music"])
api_router.include_router(ratings_router, prefix="/ratings", tags=["ratings"])
api_router.include_router(playlists_router, prefix="/playlists", tags=["playlists"])