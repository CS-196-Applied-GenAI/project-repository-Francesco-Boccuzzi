/* React Context for managing application state (stations, search, etc.) */

import React, { createContext, useContext, useState, useCallback } from "react";
import { searchStations } from "../services/api";

// Create the context
// Add 'export' here
export const StationContext = createContext();

/**
 * Provider component for station state management
 * 
 * State includes:
 * - stations: List of stations from search results
 * - loading: Loading state for API calls
 * - error: Error message if any
 * - searchCenter: Coordinates of the last search
 * - searchRadius: Radius used in the last search
 * - selectedStationId: Currently selected station (for map interaction)
 */
export const StationProvider = ({ children }) => {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchCenter, setSearchCenter] = useState(null);
  const [searchRadius, setSearchRadius] = useState(2.0);
  const [selectedStationId, setSelectedStationId] = useState(null);
  const [cheapestStationId, setCheapestStationId] = useState(null);

  /**
   * Perform a spatial search for gas stations
   * Handles loading state and error management
   */
  const performSearch = useCallback(async (latitude, longitude, radius = 2.0) => {
    setLoading(true);
    setError(null);

    try {
      const data = await searchStations(latitude, longitude, radius);
      setStations(data.stations || []);
      setSearchCenter({ latitude, longitude });
      setSearchRadius(radius);
      setCheapestStationId(data.cheapest_station_id);
    } catch (err) {
      setError(err.message || "Failed to fetch stations");
      setStations([]);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Clear all search results and reset state
   */
  const clearSearch = useCallback(() => {
    setStations([]);
    setSearchCenter(null);
    setError(null);
    setSelectedStationId(null);
    setCheapestStationId(null);
  }, []);

  const value = {
    // State
    stations,
    loading,
    error,
    searchCenter,
    searchRadius,
    selectedStationId,
    cheapestStationId,

    // Actions
    performSearch,
    clearSearch,
    setSelectedStationId,
    setStations,
  };

  return (
    <StationContext.Provider value={value}>
      {children}
    </StationContext.Provider>
  );
};

/**
 * Hook to access station context
 * Must be called within a StationProvider
 */
export const useStations = () => {
  const context = useContext(StationContext);
  if (!context) {
    throw new Error("useStations must be used within a StationProvider");
  }
  return context;
};
