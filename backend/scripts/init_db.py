#!/usr/bin/env python3
"""
Database initialization script for the Music Ranking App.

This script:
1. Creates the database if it doesn't exist
2. Initializes tables using SQLAlchemy
3. Runs Alembic migrations
4. Optionally seeds the database with sample data
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to Python path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from alembic import command
from alembic.config import Config

# Load environment variables
load_dotenv()

import database
from database import DATABASE_URL, Base, engine
import models
from models import User, Artist, Album, Song, Rating, Review, Playlist, PlaylistSong


def create_database_if_not_exists(database_url: str):
    """Create the database if it doesn't exist."""
    # Parse database URL to get connection info
    from urllib.parse import urlparse
    parsed = urlparse(database_url)
    
    db_name = parsed.path[1:]  # Remove leading slash
    connection_params = {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 5432,
        'user': parsed.username or 'postgres',
        'password': parsed.password or ''
    }
    
    # Connect to PostgreSQL server (not specific database)
    try:
        conn = psycopg2.connect(
            host=connection_params['host'],
            port=connection_params['port'],
            user=connection_params['user'],
            password=connection_params['password'],
            database='postgres'  # Connect to default database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database '{db_name}'...")
            cur.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Database '{db_name}' created successfully")
        else:
            print(f"✅ Database '{db_name}' already exists")
        
        cur.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error creating database: {e}")
        sys.exit(1)


def create_tables():
    """Create all tables using SQLAlchemy."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)


def run_alembic_migrations():
    """Run Alembic migrations."""
    print("Running Alembic migrations...")
    try:
        alembic_cfg = Config(str(backend_dir / "alembic.ini"))
        alembic_cfg.set_main_option("script_location", str(backend_dir / "alembic"))
        command.upgrade(alembic_cfg, "head")
        print("✅ Alembic migrations completed successfully")
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        print("Note: This is expected if no migrations exist yet.")


def seed_sample_data():
    """Seed the database with sample data."""
    from sqlalchemy.orm import sessionmaker
    import services
    from services import UserService, MusicService, RatingService, PlaylistService
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("Seeding sample data...")
        
        # Create sample users
        user1 = UserService.create_user(
            db=session,
            username="demo_user",
            email="demo@example.com",
            password="demo123",
            first_name="Demo",
            last_name="User"
        )
        
        user2 = UserService.create_user(
            db=session,
            username="music_lover",
            email="music@example.com", 
            password="music123",
            first_name="Music",
            last_name="Lover"
        )
        
        # Create sample artists
        artist1 = MusicService.create_artist(
            db=session,
            name="The Beatles",
            bio="Legendary British rock band"
        )
        
        artist2 = MusicService.create_artist(
            db=session,
            name="Taylor Swift",
            bio="American singer-songwriter"
        )
        
        # Create sample albums
        album1 = MusicService.create_album(
            db=session,
            title="Abbey Road",
            artist_id=artist1.id,
            release_date="1969-09-26",
            album_type="album"
        )
        
        album2 = MusicService.create_album(
            db=session,
            title="1989",
            artist_id=artist2.id,
            release_date="2014-10-27",
            album_type="album"
        )
        
        # Create sample songs
        song1 = MusicService.create_song(
            db=session,
            title="Come Together",
            artist_id=artist1.id,
            album_id=album1.id,
            track_number=1,
            duration_ms=259000
        )
        
        song2 = MusicService.create_song(
            db=session,
            title="Shake It Off",
            artist_id=artist2.id,
            album_id=album2.id,
            track_number=6,
            duration_ms=219000
        )
        
        # Create sample ratings
        RatingService.create_rating(
            db=session,
            user_id=user1.id,
            song_id=song1.id,
            rating=9.5
        )
        
        RatingService.create_rating(
            db=session,
            user_id=user2.id,
            album_id=album2.id,
            rating=8.8
        )
        
        # Create sample playlist
        playlist = PlaylistService.create_playlist(
            db=session,
            user_id=user1.id,
            name="My Favorites",
            description="Songs I love",
            is_public=True
        )
        
        PlaylistService.add_song_to_playlist(
            db=session,
            playlist_id=playlist.id,
            song_id=song1.id,
            user_id=user1.id
        )
        
        print("✅ Sample data seeded successfully")
        
    except Exception as e:
        print(f"❌ Error seeding sample data: {e}")
        session.rollback()
    finally:
        session.close()


def main():
    """Main initialization function."""
    parser = argparse.ArgumentParser(description="Initialize Music Ranking App database")
    parser.add_argument("--seed", action="store_true", help="Seed database with sample data")
    parser.add_argument("--skip-create", action="store_true", help="Skip database creation")
    parser.add_argument("--skip-tables", action="store_true", help="Skip table creation")
    parser.add_argument("--skip-migrations", action="store_true", help="Skip Alembic migrations")
    
    args = parser.parse_args()
    
    print("🎵 Music Ranking App - Database Initialization")
    print("=" * 50)
    
    # Step 1: Create database
    if not args.skip_create:
        create_database_if_not_exists(DATABASE_URL)
    
    # Step 2: Create tables
    if not args.skip_tables:
        create_tables()
    
    # Step 3: Run migrations
    if not args.skip_migrations:
        run_alembic_migrations()
    
    # Step 4: Seed sample data (optional)
    if args.seed:
        seed_sample_data()
    
    print("\n✅ Database initialization completed!")
    print("\nYou can now:")
    print("  • Start the FastAPI server: uvicorn src.main:app --reload")
    print("  • View API docs at: http://localhost:8000/docs")
    print("  • Check health at: http://localhost:8000/health")


if __name__ == "__main__":
    main()