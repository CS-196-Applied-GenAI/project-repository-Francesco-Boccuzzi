/* API service for communicating with the backend */

import axios from "axios";
// Corrected path to go up one level to find config.js
import { API_BASE_URL } from '../config';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Search for gas stations within a specified radius
 * 
 * Phase 2.1 Implementation: Calls GET /api/stations with spatial query parameters
 * 
 * @param {number} latitude - Search center latitude
 * @param {number} longitude - Search center longitude
 * @param {number} radiusKm - Search radius in kilometers (1-5)
 * @returns {Promise} Response containing stations, count, and cheapest station ID
 */
export const searchStations = async (latitude, longitude, radiusKm) => {
  try {
    const response = await apiClient.get("/api/stations", {
      params: {
        latitude,
        longitude,
        radius_km: radiusKm,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error searching stations:", error);
    throw error;
  }
};

/**
 * Update a station's price and status (admin override)
 * 
 * Phase 2.2 Implementation: Calls PATCH /api/stations/:id to update station data
 * Automatically updates last_verified_at timestamp
 * 
 * @param {string} stationId - UUID of the station to update
 * @param {object} updateData - Object containing gasolina_comum_price and/or status
 * @returns {Promise} Updated station data
 */
export const updateStationPrice = async (stationId, updateData) => {
  try {
    const response = await apiClient.patch(`/api/stations/${stationId}`, updateData);
    return response.data;
  } catch (error) {
    console.error("Error updating station:", error);
    throw error;
  }
};

export default apiClient;
