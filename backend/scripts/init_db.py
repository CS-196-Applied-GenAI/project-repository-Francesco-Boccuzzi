"""
Database initialization script.
Run this to create all tables in PostgreSQL.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import init_db, engine

if __name__ == "__main__":
    print("Initializing database...")
    try:
        init_db()
        print("✓ Database initialized successfully!")
        print(f"✓ Connected to: {engine.url}")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)
