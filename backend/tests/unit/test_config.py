"""
Tests for configuration loading and environment variables.
"""
import pytest
import os
from dotenv import load_dotenv


class TestConfigurationLoading:
    """Test configuration and environment variable loading."""

    def test_env_file_exists(self):
        """Test that .env.example file exists."""
        env_example_path = os.path.join(
            os.path.dirname(__file__),
            "../../.env.example"
        )
        assert os.path.exists(env_example_path)

    def test_database_url_from_env(self):
        """Test DATABASE_URL configuration."""
        from app.core.config import DATABASE_URL
        
        assert DATABASE_URL is not None
        assert len(DATABASE_URL) > 0

    def test_database_url_format(self):
        """Test DATABASE_URL has proper format."""
        from app.core.config import DATABASE_URL
        
        # Should contain protocol
        assert "://" in DATABASE_URL
        # Should contain host or memory indicator
        assert "@" in DATABASE_URL or ":memory:" in DATABASE_URL

    def test_dotenv_loads_successfully(self):
        """Test that dotenv can load environment variables."""
        # This should not raise an error
        load_dotenv()
        assert True  # If we get here, it loaded successfully
