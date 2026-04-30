# Project Structure - Phase 2 Complete

Complete file structure after Phase 2 implementation.

## Directory Layout

```
project-repository-Francesco-Boccuzzi/
├── QUICKSTART.md                          # Quick start guide
├── PHASE2_IMPLEMENTATION.md               # Full implementation guide
├── PHASE2_SUMMARY.md                      # What was implemented
├── PHASE1_SETUP.md                        # Phase 1 backend setup (existing)
├── plan.md                                # Development plan (existing)
├── spec.md                                # Project specification (existing)
├── README.md                              # Project overview (existing)
├── pyrightconfig.json                     # Python config (existing)
│
├── backend/                               # FastAPI Backend
│   ├── main.py                            # ✅ MODIFIED - CORS & routing
│   ├── requirements.txt                   # ✅ MODIFIED - Added dependencies
│   ├── PHASE1_SETUP.md                    # Phase 1 documentation
│   ├── .env.example                       # Environment template
│   ├── .gitignore                         # Git ignore rules
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py                      # ✅ NEW - API endpoints (Phase 2)
│   │   ├── schemas.py                     # ✅ NEW - Pydantic models (Phase 2)
│   │   ├── utils.py                       # ✅ NEW - Haversine distance (Phase 2)
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py                  # Database configuration
│   │   │   └── database.py                # SQLAlchemy setup
│   │   │
│   │   └── models/
│   │       ├── __init__.py
│   │       └── station.py                 # Station ORM model
│   │
│   ├── scripts/
│   │   ├── init_db.py                     # Database initialization
│   │   └── seed_stations.py               # Sample data seeding
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── unit/
│           ├── test_config.py
│           ├── test_database.py
│           └── test_models.py
│
└── frontend/                              # React Frontend (NEW)
    ├── package.json                       # Dependencies & scripts
    ├── .env.example                       # Environment template
    ├── .gitignore                         # Git ignore rules
    ├── README.md                          # Frontend documentation
    │
    ├── public/
    │   └── index.html                     # HTML template
    │
    └── src/
        ├── index.js                       # React entry point
        ├── index.css                      # Global styles
        ├── App.js                         # Main component
        ├── App.css                        # App styles
        ├── config.js                      # Configuration constants
        │
        ├── components/
        │   ├── SearchBar.js               # Location input & radius
        │   ├── MapComponent.js            # Google Maps visualization
        │   └── StationList.js             # Station sidebar
        │
        ├── context/
        │   └── StationContext.js          # React Context state mgmt
        │
        └── services/
            └── api.js                     # Axios API calls
```

## File Purposes

### Backend - NEW/MODIFIED Files

| File | Status | Purpose |
|------|--------|---------|
| `routes.py` | ✅ NEW | GET/PATCH endpoints for stations |
| `schemas.py` | ✅ NEW | Pydantic models for validation |
| `utils.py` | ✅ NEW | Haversine distance calculation |
| `main.py` | ✅ MODIFIED | Added CORS middleware & routes |
| `requirements.txt` | ✅ MODIFIED | Added python-multipart |

### Frontend - ALL NEW Files

#### Components
| File | Purpose |
|------|---------|
| `SearchBar.js` | Coordinate input + radius slider |
| `MapComponent.js` | Google Maps with markers |
| `StationList.js` | Sidebar with price-sorted stations |

#### State & Services
| File | Purpose |
|------|---------|
| `StationContext.js` | React Context for state management |
| `api.js` | Axios API client |

#### Configuration & Entry
| File | Purpose |
|------|---------|
| `config.js` | Constants & API configuration |
| `App.js` | Main layout & orchestration |
| `index.js` | React DOM entry point |

#### Styles
| File | Purpose |
|------|---------|
| `App.css` | Component-specific styles |
| `index.css` | Global styles |

#### Build & Config
| File | Purpose |
|------|---------|
| `package.json` | Dependencies & npm scripts |
| `.env.example` | Environment template |
| `.gitignore` | Ignore rules |

## What Each Component Does

### 1. SearchBar Component
**Location:** `frontend/src/components/SearchBar.js`

```
User Input (Coordinates)
        ↓
Validation (São Paulo bounds)
        ↓
API Call to /api/stations
        ↓
Display results or error
```

Features:
- Latitude/Longitude input fields
- Dynamic radius slider (1-5km)
- Geofencing validation
- Error messages
- Loading state

### 2. MapComponent
**Location:** `frontend/src/components/MapComponent.js`

```
Station Data from Context
        ↓
Create Markers with color
  - Green: Cheapest
  - Red: Others
        ↓
Add InfoWindows
        ↓
Handle marker clicks
```

Features:
- Google Maps integration
- Color-coded markers
- Info windows with directions link
- Marker animation
- Click handling

### 3. StationList (Sidebar)
**Location:** `frontend/src/components/StationList.js`

```
Station Data from Context
        ↓
Sort by price
        ↓
Display in list format
        ↓
Handle clicks to highlight map
```

Features:
- Price-sorted display
- Click interaction
- Distance calculation
- Date formatting (DD/MM/YYYY)
- Cheapest badge

### 4. StationContext
**Location:** `frontend/src/context/StationContext.js`

```
State Variables:
- stations
- loading
- error
- searchCenter
- searchRadius
- selectedStationId
- cheapestStationId

Actions:
- performSearch()
- clearSearch()
- setSelectedStationId()
```

### 5. API Service
**Location:** `frontend/src/services/api.js`

```
Frontend Component
        ↓
Calls API function (searchStations, updateStationPrice)
        ↓
Axios HTTP request to backend
        ↓
Returns JSON response
```

## Backend API Endpoints

### Phase 2.1: Spatial Search
```
GET /api/stations?latitude=X&longitude=Y&radius_km=Z
Response: StationListResponse with stations, count, cheapest_station_id
```

### Phase 2.2: Admin Override
```
PATCH /api/stations/{station_id}
Body: {"gasolina_comum_price": X, "status": "Success"}
Response: Updated StationResponse
```

## Data Flow

### Search Flow
```
User enters coordinates in SearchBar
        ↓
SearchBar.handleSearch() calls performSearch(lat, lng, radius)
        ↓
StationContext.performSearch() calls api.searchStations()
        ↓
api.js sends GET request to /api/stations
        ↓
Backend queries database using Haversine formula
        ↓
Returns stations within radius
        ↓
Context updates state (stations, cheapestStationId)
        ↓
MapComponent re-renders with markers
        ↓
StationList re-renders with sorted stations
```

### Selection Flow
```
User clicks station in sidebar
        ↓
StationList calls onStationSelect(stationId)
        ↓
App calls setSelectedStationId()
        ↓
MapComponent receives selectedStationId via context
        ↓
Marker animates (bounce)
        ↓
InfoWindow can open on click
```

## Technology Stack

### Backend
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL / SQLite
- **Validation:** Pydantic
- **HTTP:** Uvicorn

### Frontend
- **Framework:** React 18
- **UI Library:** Material-UI v5
- **Maps:** Google Maps API
- **HTTP Client:** Axios
- **State:** React Context
- **Build:** Create React App (npm scripts)

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/db
```

### Frontend (.env)
```
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_GOOGLE_MAPS_API_KEY=YOUR_KEY
```

## Development Commands

### Backend
```bash
# Start server
python -m uvicorn main:app --reload

# Run tests
pytest tests/

# Initialize database
python scripts/init_db.py

# Seed data
python scripts/seed_stations.py
```

### Frontend
```bash
# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build

# Run tests (if configured)
npm test
```

## Key Features Implemented

✅ **Phase 2.1 - Spatial Search**
- Haversine distance calculation
- Radius filtering (1-5km)
- Price identification
- Response structuring

✅ **Phase 2.2 - Admin Override**
- Price updates
- Status updates
- Timestamp management
- Error handling

✅ **Frontend Features**
- Location search interface
- Google Maps visualization
- Station list sidebar
- Responsive design
- Real-time state management
- Material-UI components

## Next Phase (Phase 3)

The codebase is structured to easily add:
- ElevenLabs AI integration
- Cron job scheduler
- Admin dashboard
- Enhanced error handling
- Testing utilities

All Phase 2 components provide clean interfaces for Phase 3 integration.

## Summary

**Phase 2 provides:**
- 2 production-ready API endpoints
- Complete React frontend with 3 main components
- React Context for state management
- Full Material-UI integration
- Google Maps visualization
- Mobile-responsive design
- Comprehensive documentation

The application is ready to be tested, deployed, or extended with Phase 3 features.
