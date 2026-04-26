# São Paulo Gas Price Tracker - Backend Setup (Phase 1)

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Environment configuration
│   │   └── database.py         # SQLAlchemy setup & session management
│   ├── models/
│   │   ├── __init__.py
│   │   └── station.py          # Station database model
│   └── __init__.py
├── scripts/
│   ├── init_db.py              # Database initialization script
│   └── seed_stations.py        # Seed script with real SP data
├── main.py                      # FastAPI application entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

## Phase 1 Setup Instructions

### Step 1: Prerequisites
Ensure you have the following installed:
- **Python 3.9+**: `python3 --version`
- **PostgreSQL 12+**: Available locally or via Docker

### Step 2: PostgreSQL Setup

#### Option A: Local PostgreSQL Installation (macOS with Homebrew)
```bash
# Install PostgreSQL
brew install postgresql@15

# Start the PostgreSQL service
brew services start postgresql@15

# Verify installation
psql --version
```

#### Option B: Docker PostgreSQL (Recommended for quick setup)
```bash
# Run PostgreSQL in Docker
docker run -d \
  --name gas_tracker_db \
  -e POSTGRES_USER=gas_tracker_user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=gas_tracker_db \
  -p 5432:5432 \
  postgres:15-alpine

# Verify the container is running
docker ps | grep gas_tracker_db
```

#### Option C: Create database manually (if using local PostgreSQL)
```bash
# Connect to PostgreSQL
psql -U postgres

# Inside psql terminal:
CREATE USER gas_tracker_user WITH PASSWORD 'password';
CREATE DATABASE gas_tracker_db OWNER gas_tracker_user;
GRANT ALL PRIVILEGES ON DATABASE gas_tracker_db TO gas_tracker_user;

# Exit psql with \q
```

### Step 3: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Create .env file from example
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Initialize the database (creates all tables)
python scripts/init_db.py

# Seed the database with São Paulo gas stations
python scripts/seed_stations.py
```

### Step 4: Verify Database Setup

```bash
# Connect to the database and verify
psql -U gas_tracker_user -d gas_tracker_db

# Inside psql terminal, run:
SELECT COUNT(*) FROM stations;
SELECT name, bandeira, gasolina_comum_price FROM stations LIMIT 5;

# Exit with \q
```

### Step 5: Run the FastAPI Server

```bash
# From the backend directory with venv activated
python main.py
```

The server will start at `http://localhost:8000`

### Step 6: Test the API

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy"}
```

## Phase 1 Completion

✓ **Project initialized** with clean structure  
✓ **Database configured** with SQLAlchemy ORM  
✓ **Station model created** with all required fields from spec:
  - UUID primary key
  - Name, phone (E.164), address
  - Coordinates (lat/lng)
  - Brand (bandeira)
  - Price (gasolina_comum_price)
  - Verification timestamp (last_verified_at)
  - Status enum (Success, No Data, Pending)

✓ **Real seed data**: 15 São Paulo gas stations from major brands (Shell, Ipiranga, BR, Petrobras)  
✓ **Database initialization scripts** ready to use  
✓ **FastAPI foundation** ready for Phase 2 API endpoints

## Database Schema

The `stations` table includes:

| Column | Type | Notes |
|--------|------|-------|
| station_id | UUID | Primary key |
| name | String(255) | Indexed |
| phone_number | String(20) | E.164 format |
| address | String(500) | |
| city | String(100) | Indexed, default "São Paulo" |
| latitude | Float | Indexed |
| longitude | Float | Indexed |
| bandeira | String(100) | Indexed |
| gasolina_comum_price | Float | Nullable |
| last_verified_at | DateTime | Nullable |
| status | Enum | SUCCESS, NO_DATA, PENDING |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

## Troubleshooting

**Connection Error to PostgreSQL?**
- Verify PostgreSQL is running: `brew services list` or `docker ps`
- Check `.env` DATABASE_URL matches your setup
- Test connection: `psql -U gas_tracker_user -d gas_tracker_db`

**Import errors when running scripts?**
- Ensure virtual environment is activated: `source venv/bin/activate`
- Verify all dependencies installed: `pip install -r requirements.txt`

**Database already exists?**
- The seed script will skip if data already exists
- To reset: `psql -U gas_tracker_user -d gas_tracker_db` then `DROP TABLE stations CASCADE;`

## Next Steps

Phase 2 will implement:
- `GET /api/stations` - Spatial query endpoint with radius filtering
- `PATCH /api/stations/:id` - Admin override endpoint
