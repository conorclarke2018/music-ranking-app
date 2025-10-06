# Music Ranking App - Backend

A FastAPI backend for the Music Ranking application with PostgreSQL database, SQLAlchemy ORM, and comprehensive music management features.

## 🏗️ Architecture Overview

The backend is built with:
- **FastAPI**: Modern, fast web framework with automatic OpenAPI documentation
- **PostgreSQL**: Robust relational database for data persistence
- **SQLAlchemy**: Python SQL toolkit and ORM with Alembic for migrations
- **Comprehensive Models**: Users, Artists, Albums, Songs, Ratings, Reviews, and Playlists
- **Service Layer**: Business logic separated from API endpoints
- **Spotify Integration**: Ready for Spotify API integration
- **AI Features**: Prepared for OpenAI integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Virtual environment (recommended)

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Edit `.env` and configure your database:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/musicrankingdb
SECRET_KEY=your-secret-key-here
DEBUG=true
```

### 3. Initialize Database

Run the database initialization script:

```bash
# Initialize database with tables
python scripts/init_db.py

# Or initialize with sample data
python scripts/init_db.py --seed
```

### 4. Start the Server

```bash
# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
backend/
├── src/
│   ├── models/           # SQLAlchemy database models
│   │   ├── user.py       # User model
│   │   ├── music.py      # Artist, Album, Song models
│   │   ├── rating.py     # Rating, Review models
│   │   └── playlist.py   # Playlist, PlaylistSong models
│   ├── services/         # Business logic layer
│   │   ├── user_service.py
│   │   ├── music_service.py
│   │   ├── rating_service.py
│   │   └── playlist_service.py
│   ├── api/              # FastAPI routers
│   │   ├── users.py
│   │   ├── music.py
│   │   ├── ratings.py
│   │   └── playlists.py
│   ├── database.py       # Database configuration
│   ├── config.py         # Application settings
│   └── main.py          # FastAPI application
├── scripts/
│   └── init_db.py       # Database initialization
├── alembic/             # Database migrations
├── requirements.txt
├── alembic.ini
└── .env.example
```

## 🗄️ Database Schema

### Core Models

- **Users**: Authentication, profiles, Spotify integration
- **Artists**: Music artists with metadata
- **Albums**: Album information and relationships
- **Songs**: Individual tracks with audio features
- **Ratings**: Numerical ratings (1-10 scale)
- **Reviews**: Written reviews with optional ratings
- **Playlists**: User-created playlists
- **PlaylistSongs**: Song-playlist associations

### Key Relationships

- Users can rate/review songs and albums
- Users can create multiple playlists
- Songs belong to artists and optionally albums
- Albums belong to artists
- Playlists contain multiple songs with ordering

## 🔌 API Endpoints

### Users (`/api/v1/users`)
- `GET /` - List users
- `POST /` - Create user
- `GET /{user_id}` - Get user details

### Music (`/api/v1/music`)
- `GET /search?q=query` - Search artists, albums, songs
- `GET /artists/{id}` - Get artist details
- `GET /albums/{id}` - Get album details
- `GET /songs/{id}` - Get song details
- `POST /artists` - Create artist

### Ratings (`/api/v1/ratings`)
- `POST /` - Create/update rating
- `GET /song/{song_id}/average` - Get song average rating
- `GET /album/{album_id}/average` - Get album average rating

### Playlists (`/api/v1/playlists`)
- `POST /` - Create playlist
- `GET /{playlist_id}` - Get playlist details
- `GET /user/{user_id}` - Get user playlists
- `POST /{playlist_id}/songs` - Add song to playlist

## 🛠️ Development Commands

### Database Operations

```bash
# Create migration
cd backend
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Quality

```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src tests/
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | Application secret key | Required |
| `DEBUG` | Enable debug mode | `false` |
| `SPOTIFY_CLIENT_ID` | Spotify API client ID | Optional |
| `SPOTIFY_CLIENT_SECRET` | Spotify API client secret | Optional |
| `OPENAI_API_KEY` | OpenAI API key | Optional |

### Database Pool Settings

The application supports PostgreSQL connection pooling configuration:

```env
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=0
DB_POOL_RECYCLE=300
DB_POOL_PRE_PING=true
```

## 🚦 Health Monitoring

The `/health` endpoint provides system status:

```json
{
  "status": "healthy",
  "service": "music-ranking-api",
  "database": "connected",
  "environment": "development"
}
```

## 🔮 Future Features

The backend is designed to support:

- **Authentication**: JWT-based user authentication
- **Spotify Integration**: Import playlists, sync data
- **AI Recommendations**: OpenAI-powered music suggestions
- **Social Features**: Follow users, share playlists
- **Advanced Search**: Full-text search, filters
- **Caching**: Redis for performance optimization
- **File Storage**: Image uploads for users/playlists

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check PostgreSQL is running
   - Verify DATABASE_URL is correct
   - Ensure database exists

2. **Import Errors**
   - Check Python path includes `src/`
   - Verify all dependencies installed

3. **Migration Issues**
   - Run `alembic upgrade head`
   - Check alembic.ini configuration

### Logs

The application logs include:
- Database connection status
- API request/response details (in debug mode)
- Error tracebacks with context

## 📄 License

This project is part of the Music Ranking App and follows the same licensing terms.