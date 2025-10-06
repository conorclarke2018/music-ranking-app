#!/usr/bin/env python3
"""
Simple database test script to verify database connectivity.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from database import init_db, engine
    from sqlalchemy import text
    
    print("🎵 Testing Database Connection...")
    print("=" * 40)
    
    # Test database connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ PostgreSQL Connection: {version}")
    
    # Initialize database
    print("Creating database tables...")
    init_db()
    
    print("\n✅ Database setup completed successfully!")
    print("\nYou can now start the server with:")
    print("  source venv/bin/activate")
    print("  uvicorn src.main:app --reload")
    
except Exception as e:
    print(f"❌ Database error: {e}")
    sys.exit(1)