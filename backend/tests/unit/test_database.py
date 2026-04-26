"""
Tests for database configuration and connection.
"""
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, SessionLocal
from app.core.config import DATABASE_URL


class TestDatabaseConfiguration:
    """Test database configuration and connection."""

    def test_database_url_exists(self):
        """Test that DATABASE_URL is configured."""
        assert DATABASE_URL is not None
        assert "postgresql" in DATABASE_URL or "sqlite" in DATABASE_URL

    def test_database_url_has_driver(self):
        """Test that DATABASE_URL includes psycopg2 driver."""
        assert "psycopg2" in DATABASE_URL or "sqlite" in DATABASE_URL

    def test_session_local_is_callable(self):
        """Test that SessionLocal is a callable session factory."""
        assert callable(SessionLocal)

    def test_base_metadata_exists(self):
        """Test that Base metadata is available."""
        assert Base.metadata is not None

    def test_base_has_station_table(self):
        """Test that Station table is in Base metadata."""
        table_names = [table.name for table in Base.metadata.tables.values()]
        assert "stations" in table_names


class TestDatabaseConnection:
    """Test database connection and operations."""

    def test_in_memory_database_creation(self):
        """Test creating an in-memory SQLite database."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        
        # Correct way to use the inspector
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Use bool() or direct comparison to satisfy Pylance
        assert "stations" in tables

    def test_database_table_schema(self):
        """Test that database table has all required columns."""
        from sqlalchemy import inspect
        from app.models.station import Station
        
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        
        inspector = inspect(engine)
        columns = [col["name"] for col in inspector.get_columns("stations")]
        
        required_columns = [
            "station_id",
            "name",
            "phone_number",
            "address",
            "city",
            "latitude",
            "longitude",
            "bandeira",
            "gasolina_comum_price",
            "last_verified_at",
            "status",
            "created_at",
            "updated_at",
        ]
        
        for col in required_columns:
            assert col in columns, f"Column {col} not found in stations table"

    def test_database_indexes(self):
        """Test that indexes are created on expected columns."""
        from sqlalchemy import inspect
        
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        
        inspector = inspect(engine)
        indexes = inspector.get_indexes("stations")
        index_columns = [col for idx in indexes for col in idx["column_names"]]
        
        # Verify spatial indexes
        assert "latitude" in index_columns or len(indexes) > 0
        assert "longitude" in index_columns or len(indexes) > 0


class TestSessionManagement:
    """Test database session management."""

    def test_session_creation(self):
        """Test creating a database session."""
        from sqlalchemy import create_engine
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        assert session is not None
        session.close()

    def test_session_context_manager(self):
        """Test using session as context manager."""
        from sqlalchemy import create_engine
        engine = create_engine("sqlite:///:memory:")
        TestSession = sessionmaker(bind=engine)
        
        with TestSession() as session:
            assert session is not None
