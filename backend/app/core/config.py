import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://gas_tracker_user:password@localhost:5432/gas_tracker_db"
)

# Ensure DATABASE_URL uses psycopg2 driver
if "postgresql://" in DATABASE_URL and "psycopg2" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
