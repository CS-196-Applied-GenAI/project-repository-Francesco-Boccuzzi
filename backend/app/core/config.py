import os
from dotenv import load_dotenv

load_dotenv()

# Change the default to a local SQLite file if no DATABASE_URL is found
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./gas_tracker.db"
)

# Remove or comment out the block that forces psycopg2
# if "postgresql://" in DATABASE_URL and "psycopg2" not in DATABASE_URL:
#     DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")