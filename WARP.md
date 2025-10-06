# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a full-stack music ranking application with:
- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and Framer Motion
- **Backend**: FastAPI with Python, SQLAlchemy, and PostgreSQL
- **External APIs**: Spotify integration and OpenAI for AI features

The app allows users to rate albums/songs, generates AI-powered playlists, and provides music recommendations based on listening patterns.

## Development Commands

### Starting the Application
```bash
# Start both frontend and backend concurrently
npm run dev

# Or run separately:
npm run dev:frontend  # Next.js dev server on :3000
npm run dev:backend   # FastAPI server on :8000
```

### Testing
```bash
# Run all tests (both frontend and backend)
npm test

# Frontend tests only
cd frontend && npm test

# Run frontend tests in watch mode
cd frontend && npm run test:watch

# Backend tests only
cd backend && pytest
```

### Building and Linting
```bash
# Build frontend for production
npm run build

# Lint frontend code
npm run lint

# Format backend code
cd backend && black src/
cd backend && flake8 src/
```

### Database Operations
```bash
cd backend

# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

### Backend Setup
```bash
# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Architecture

### Frontend Structure (`frontend/src/`)
- **`app/`**: Next.js App Router pages and layouts
- **`components/`**: React components (currently contains HomePage.tsx)
- **`services/`**: API calls and external service integrations
- **`types/`**: TypeScript type definitions

### Backend Structure (`backend/src/`)
- **`main.py`**: FastAPI application entry point with CORS and basic endpoints
- **`api/`**: API route modules (to be implemented)
- **`models/`**: SQLAlchemy database models
- **`services/`**: Business logic layer
- **`utils/`**: Utility functions

### Key Integration Points
- Frontend fetches from backend at `http://localhost:8000`
- Backend serves API docs at `/docs` (Swagger UI)
- CORS configured for localhost:3000 (Next.js default port)

## Environment Variables

### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SPOTIFY_CLIENT_ID=your_spotify_client_id
```

### Backend (`.env`)
```
DATABASE_URL=postgresql://username:password@localhost/musicrankingdb
SECRET_KEY=your_secret_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
OPENAI_API_KEY=your_openai_api_key
```

## Key Dependencies

### Frontend
- **Next.js 14**: App Router architecture
- **Framer Motion**: Animations (used in HomePage.tsx)
- **Heroicons**: Icon library
- **Axios**: HTTP client for API calls
- **Jest + Testing Library**: Testing framework

### Backend  
- **FastAPI**: Web framework with automatic OpenAPI docs
- **SQLAlchemy + Alembic**: ORM and migrations
- **Pydantic**: Data validation
- **Spotipy**: Spotify API client
- **OpenAI**: AI integration
- **pytest**: Testing framework

## Development Notes

- The project uses workspaces with the frontend as a workspace member
- Backend uses uvicorn with auto-reload for development
- Database migrations handled via Alembic
- Both frontend and backend have their own test suites
- CORS is pre-configured for local development
- API documentation auto-generated and available at `/docs`