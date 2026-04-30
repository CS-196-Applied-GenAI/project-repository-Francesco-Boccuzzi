/* Frontend environment configuration */

// API Base URL - points to the FastAPI backend
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

// Google Maps API Key - Set via environment variables
// Using Maps Embed API (free tier)
const GOOGLE_MAPS_API_KEY = process.env.REACT_APP_GOOGLE_MAPS_API_KEY || "AIzaSyD5G-tz32Qc5ZA4FqnO1ChEeq2ShelK-vs";

// Default search radius in kilometers
const DEFAULT_RADIUS_KM = 2.0;

// Minimum and maximum search radius
const MIN_RADIUS_KM = 1.0;
const MAX_RADIUS_KM = 5.0;

// São Paulo city bounds (approximate)
// Used for geofencing validation
const SAO_PAULO_BOUNDS = {
  north: -23.4,
  south: -23.8,
  east: -46.3,
  west: -46.8,
};

export {
  API_BASE_URL,
  GOOGLE_MAPS_API_KEY,
  DEFAULT_RADIUS_KM,
  MIN_RADIUS_KM,
  MAX_RADIUS_KM,
  SAO_PAULO_BOUNDS,
};
