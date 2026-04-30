# Frontend Setup Instructions - Maps Embed API

## Overview

This is a React application for the São Paulo Gas Price Tracker using the **free Google Maps Embed API**.

## Prerequisites

- **Node.js** 14+ and npm
- **Google Maps Embed API Key** - Free tier from [Google Cloud Console](https://console.cloud.google.com/)

## Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   Create a `.env` file:
   ```env
   REACT_APP_API_BASE_URL=http://localhost:8000
   REACT_APP_GOOGLE_MAPS_API_KEY=AIzaSyD5G-tz32Qc5ZA4FqnO1ChEeq2ShelK-vs
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   Opens at `http://localhost:3000`

## What Changed

### Map Component Now Uses Embed API
- ✅ Static embedded map (instead of interactive markers)
- ✅ Centered on search location
- ✅ Shows interactive controls (zoom, pan, satellite)
- ✅ Free tier (no credit card required)
- ⚠️ No custom color-coded markers

### Station List Enhanced with Navigation
- ✅ Direct "Navigate" button on each station
- ✅ Opens Google Maps directions in new tab
- ✅ Cheapest station shown in green bar on map

### Removed Dependencies
- ❌ `@react-google-maps/api` (no longer needed)

## How to Use

### 1. Search for Stations
- Enter latitude/longitude (e.g., -23.5505, -46.6561)
- Set radius (1-5km)
- Click "Search"

### 2. View Results
- **Map**: Shows embedded Google Maps of search area
- **Sidebar**: Lists all stations sorted by price
- **Green Bar**: Highlights cheapest station with navigate button

### 3. Navigate to Station
- Click **"Navigate"** button on any station
- Opens Google Maps with directions
- Or click the green "Navigate" button for cheapest station

## Features

✅ **Spatial Search** - Find stations within 1-5km radius
✅ **Distance Calculation** - Haversine formula for accuracy
✅ **Price Sorting** - Stations sorted cheapest first
✅ **Navigation Links** - Direct to Google Maps
✅ **Responsive Design** - Desktop and mobile layouts
✅ **Free Maps API** - No credit card required

## Testing

**Sample Coordinates:** Avenida Paulista, São Paulo
- Latitude: `-23.5505`
- Longitude: `-46.6561`
- Radius: `2.0 km`

## Build

```bash
npm run build
```

## Notes

- Uses **free Google Maps Embed API** (no billing)
- All dates in DD/MM/YYYY format
- Full station details in sidebar
- Navigation links open in new tab
