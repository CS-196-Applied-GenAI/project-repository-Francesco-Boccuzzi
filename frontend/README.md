# Frontend Setup Instructions

## Overview

This is a React application for the São Paulo Gas Price Tracker. It implements Phase 2 of the project plan with a responsive, Material-UI based interface.

## Prerequisites

- **Node.js** 14+ and npm
- **Google Maps API Key** - Get one from [Google Cloud Console](https://console.cloud.google.com/)

## Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   Create a `.env` file in the frontend directory:
   ```env
   REACT_APP_API_BASE_URL=http://localhost:8000
   REACT_APP_GOOGLE_MAPS_API_KEY=YOUR_GOOGLE_MAPS_API_KEY
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   The app will open at `http://localhost:3000`

## Features Implemented (Phase 2)

### 2.1 Spatial Query Endpoint
- ✅ **GET /api/stations** - Search stations within 1-5km radius
- ✅ Haversine distance calculation
- ✅ Returns distance for each station
- ✅ Identifies cheapest station

### 2.2 Admin Override API
- ✅ **PATCH /api/stations/:id** - Update price and status
- ✅ Automatic timestamp update (`last_verified_at`)

### Frontend Features
- **Search Bar**
  - Latitude/Longitude coordinate input
  - Dynamic radius slider (1-5km)
  - São Paulo geofencing validation
  - Loading and error states

- **Map Component** (Google Maps)
  - Green marker (#00FF00) for cheapest station
  - Red markers (#FF0000) for other stations
  - Search center marker
  - InfoWindows with:
    - Station name, price, brand
    - Last verified date (DD/MM/YYYY format)
    - Google Maps directions link
  - Marker bounce animation on selection

- **Sidebar (Station List)**
  - Sorted by price (cheapest first)
  - Shows: Name, Brand, Price, Distance, Last Verified Date
  - Visual "Cheapest" badge
  - Click to highlight marker on map
  - Mobile-responsive (collapses to bottom sheet)

- **Responsive Design**
  - Desktop: 2-column layout (Map + Sidebar)
  - Mobile: Stacked vertical layout
  - Material-UI components

## Architecture

### Context (State Management)
- **StationContext** - Centralized state for stations, search, and UI interactions
- Provides hooks: `useStations()`

### Services
- **api.js** - API calls to FastAPI backend
  - `searchStations(lat, lng, radius)`
  - `updateStationPrice(stationId, data)`

### Components
- **SearchBar** - Location input and radius control
- **MapComponent** - Google Maps visualization
- **StationList** - Station sidebar
- **App** - Main layout and orchestration

## Testing the Frontend

1. **Ensure backend is running:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

2. **Test with sample coordinates:**
   - Avenida Paulista: Lat `-23.5505`, Lng `-46.6561`
   - Radius: `2.0 km`

3. **Expected behavior:**
   - Map shows stations with green (cheapest) and red markers
   - Sidebar lists stations sorted by price
   - Click stations to see info and Google Maps link
   - Dates shown in DD/MM/YYYY format

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## Dependencies

- **@mui/material** - Material Design components
- **@react-google-maps/api** - Google Maps integration
- **axios** - HTTP client
- **react** - UI framework
- **react-dom** - DOM rendering

## Notes

- The app requires CORS to be enabled on the backend (already configured in Phase 2)
- Google Maps API key is required for map functionality
- All times are displayed in DD/MM/YYYY format per spec
- Brand names are only visible in InfoWindows/Sidebar (not on map markers)
- No authentication required (public access as per spec)
