# Phase 2 Implementation Guide

Complete guide for setting up and running Phase 2 of the São Paulo Gas Price Tracker project.

## Overview

Phase 2 includes:
1. **Backend API Endpoints** (FastAPI)
   - GET `/api/stations` - Spatial query with Haversine distance calculation
   - PATCH `/api/stations/:id` - Admin override for price updates

2. **Frontend Application** (React + Material-UI)
   - Location search with coordinate input
   - Google Maps visualization with color-coded markers
   - Station list sidebar with price sorting
   - Responsive mobile design

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│  - Search Bar (location + radius)                           │
│  - Google Maps (markers, info windows)                      │
│  - Station List (sorted by price)                           │
│  - React Context (state management)                         │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP (Axios)
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                         │
│  - GET /api/stations (spatial query)                        │
│  - PATCH /api/stations/:id (price update)                   │
│  - Haversine distance calculation                           │
│  - CORS enabled for frontend integration                    │
└────────────────┬────────────────────────────────────────────┘
                 │ SQLAlchemy ORM
                 ↓
┌─────────────────────────────────────────────────────────────┐
│               DATABASE (PostgreSQL/SQLite)                  │
│  - Station model with coordinates, price, status           │
│  - Indexed for efficient geospatial queries                 │
└─────────────────────────────────────────────────────────────┘
```

## Backend Setup

### 1. Prerequisites
- Python 3.9+
- PostgreSQL or SQLite (for development)

### 2. Install Dependencies

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend` directory:

```env
# Database URL - PostgreSQL
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/gas_tracker_db

# Or use SQLite for development
# DATABASE_URL=sqlite:///./gas_tracker.db
```

### 4. Initialize Database

```bash
# Create tables
python scripts/init_db.py

# (Optional) Seed with sample data
python scripts/seed_stations.py
```

### 5. Run Backend

```bash
# Start FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs` (Swagger UI)

## Frontend Setup

### 1. Prerequisites
- Node.js 14+ and npm
- Google Maps API Key (from Google Cloud Console)

### 2. Install Dependencies

```bash
cd frontend

npm install
```

### 3. Environment Configuration

Create a `.env` file in the `frontend` directory:

```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_GOOGLE_MAPS_API_KEY=YOUR_GOOGLE_MAPS_API_KEY
```

### 4. Run Frontend

```bash
npm start
```

Frontend will open at: `http://localhost:3000`

## Testing Phase 2 Features

### Test 1: Spatial Search (2.1)

**Endpoint:** `GET /api/stations`

**Using cURL:**
```bash
curl "http://localhost:8000/api/stations?latitude=-23.5505&longitude=-46.6561&radius_km=2.0"
```

**Expected Response:**
```json
{
  "stations": [
    {
      "station_id": "uuid-string",
      "name": "Station Name",
      "price": 5.80,
      "distance_km": 0.5,
      "last_verified_at": "2024-04-30T10:00:00Z"
    }
  ],
  "count": 5,
  "cheapest_station_id": "uuid-string",
  "search_center": {"latitude": -23.5505, "longitude": -46.6561},
  "search_radius_km": 2.0
}
```

### Test 2: Price Update (2.2)

**Endpoint:** `PATCH /api/stations/:id`

**Using cURL:**
```bash
curl -X PATCH "http://localhost:8000/api/stations/{station_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "gasolina_comum_price": 6.50,
    "status": "Success"
  }'
```

**Expected Response:**
```json
{
  "station_id": "uuid-string",
  "name": "Station Name",
  "gasolina_comum_price": 6.50,
  "status": "Success",
  "last_verified_at": "2024-04-30T15:30:00Z"
}
```

### Test 3: Frontend with Sample Coordinates

1. Open `http://localhost:3000` in browser
2. Enter coordinates:
   - **Latitude:** `-23.5505` (Avenida Paulista)
   - **Longitude:** `-46.6561`
   - **Radius:** `2.0 km`
3. Click "Search"

**Expected behavior:**
- Map centers on search point
- Green marker shows cheapest station
- Red markers show other stations
- Sidebar lists stations sorted by price
- Click sidebar card to highlight marker

### Test 4: Geofencing Validation

Try coordinates outside São Paulo bounds:
- **Latitude:** `40.7128` (New York)
- **Longitude:** `-74.0060`

**Expected:** Error message "No data available in this address."

## Backend Implementation Details

### Phase 2.1: Spatial Query Endpoint

**File:** `backend/app/routes.py`

```python
@router.get("", response_model=StationListResponse)
def search_stations(
    latitude: float,
    longitude: float,
    radius_km: float,
    db: Session = Depends(get_db),
):
    # Uses Haversine formula to calculate distances
    # Returns stations within radius_km
    # Identifies cheapest station in results
```

**Distance Calculation:** Implemented in `backend/app/utils.py` using the Haversine formula:
- Converts coordinates to radians
- Calculates great-circle distance on Earth
- Returns distance in kilometers

### Phase 2.2: Admin Override API

**File:** `backend/app/routes.py`

```python
@router.patch("/{station_id}", response_model=StationResponse)
def update_station_price(
    station_id: str,
    update_data: StationUpdate,
    db: Session = Depends(get_db),
):
    # Updates gasolina_comum_price and/or status
    # Automatically updates last_verified_at timestamp
    # Returns updated station data
```

## Frontend Implementation Details

### Component Architecture

**StationContext** (State Management)
- Centralized state for stations, search results, and UI
- Provides: `useStations()` hook for component access

**SearchBar Component**
- Latitude/longitude input fields
- Dynamic radius slider (1-5km)
- Validates coordinates within São Paulo bounds
- Handles loading and error states

**MapComponent**
- Google Maps integration with `@react-google-maps/api`
- Color-coded markers:
  - Green (#00FF00) = Cheapest station
  - Red (#FF0000) = Other stations
- InfoWindows with price, brand, verified date, and directions link
- Marker bounce animation on selection

**StationList Component**
- Displays stations sorted by price (cheapest first)
- Shows: Name, Brand, Price, Distance, Last Verified Date
- Click to highlight corresponding map marker
- Mobile-responsive design

### Key Features

1. **Haversine Distance Calculation**
   - Accurate great-circle distance on Earth
   - Used for filtering and sorting
   - Displayed in sidebar as "Distance"

2. **Date Formatting**
   - All dates display as DD/MM/YYYY (Brazilian format)
   - Uses `toLocaleDateString("pt-BR")`

3. **Responsive Design**
   - Desktop: 2-column layout (Search/Map + Sidebar)
   - Mobile: Vertical stack layout
   - Uses Material-UI's Grid and useMediaQuery

4. **Error Handling**
   - Validates coordinate ranges
   - Checks São Paulo geofencing bounds
   - Displays user-friendly error messages
   - Handles API failures gracefully

## Development Workflow

### Making Changes

**Backend:**
```bash
cd backend
# Edit files in app/
# Changes auto-reload with uvicorn --reload
```

**Frontend:**
```bash
cd frontend
# Edit files in src/
# Changes hot-reload with React Dev Server
```

### Code Quality

Both backend and frontend include:
- Type hints (Python type annotations, TypeScript-ready)
- Comprehensive comments explaining logic
- Error handling and validation
- Clean, modular architecture

## Deployment Checklist

- [ ] Backend database initialized with seed data
- [ ] Environment variables configured
- [ ] Google Maps API key obtained and configured
- [ ] CORS enabled on backend (already done)
- [ ] Backend running on port 8000
- [ ] Frontend environment variables set
- [ ] Frontend dependencies installed
- [ ] Test spatial search with sample coordinates
- [ ] Test price update endpoint
- [ ] Verify markers display correctly on map
- [ ] Check mobile responsiveness

## Troubleshooting

### Backend Issues

**Issue:** `ModuleNotFoundError: No module named 'app'`
- Solution: Ensure you're running from the backend directory
- Check `PYTHONPATH` is set correctly

**Issue:** Database connection error
- Solution: Verify DATABASE_URL in .env
- Check PostgreSQL is running
- Use SQLite for development

**Issue:** CORS errors in frontend console
- Solution: Verify CORS middleware in main.py
- Check API_BASE_URL in frontend .env

### Frontend Issues

**Issue:** "Google Maps API key is not valid"
- Solution: Get valid API key from Google Cloud Console
- Enable Maps SDK, Places API, and Geometry Library
- Add to .env as REACT_APP_GOOGLE_MAPS_API_KEY

**Issue:** Stations not showing on map
- Solution: Verify backend is running
- Check API base URL in .env
- Ensure database has station data

**Issue:** Mobile layout not responding
- Solution: Clear browser cache
- Check viewport meta tag in index.html

## Next Steps (Phase 3)

After Phase 2 is complete:
- Implement ElevenLabs AI integration for automated price collection
- Create cron job scheduler for monthly updates
- Build admin dashboard for manual overrides

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Material-UI Components](https://mui.com/material-ui/)
- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
- [Haversine Formula](https://en.wikipedia.org/wiki/Haversine_formula)
