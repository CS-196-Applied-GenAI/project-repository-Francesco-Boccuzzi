/* Search bar component for location input and radius adjustment */

import React, { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Slider,
  Typography,
  Paper,
  CircularProgress,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { useStations } from "../context/StationContext";
import { MIN_RADIUS_KM, MAX_RADIUS_KM, SAO_PAULO_BOUNDS } from "../config";

/**
 * SearchBar Component
 * 
 * Provides:
 * - Google Places Autocomplete input for address search
 * - Dynamic radius slider (1-5km)
 * - Search button to trigger spatial query
 * - Geofencing validation (São Paulo city bounds)
 * - Loading state during search
 */
const SearchBar = ({ onSearch }) => {
  const { loading, error } = useStations();
  const [address, setAddress] = useState("");
  const [radius, setRadius] = useState(2.0);
  const [manualLat, setManualLat] = useState("");
  const [manualLng, setManualLng] = useState("");
  const [searchError, setSearchError] = useState("");

  /**
   * Validate if coordinates are within São Paulo city bounds
   */
  const isWithinSaoPaulo = (lat, lng) => {
    const { north, south, east, west } = SAO_PAULO_BOUNDS;
    return lat <= north && lat >= south && lng <= east && lng >= west;
  };

  /**
   * Handle search button click
   * Validates location and triggers spatial search
   */
  const handleSearch = async () => {
    setSearchError("");

    // Validate inputs
    if (!manualLat || !manualLng) {
      setSearchError("Please enter latitude and longitude");
      return;
    }

    const lat = parseFloat(manualLat);
    const lng = parseFloat(manualLng);

    // Validate coordinate ranges
    if (lat < -90 || lat > 90) {
      setSearchError("Latitude must be between -90 and 90");
      return;
    }

    if (lng < -180 || lng > 180) {
      setSearchError("Longitude must be between -180 and 180");
      return;
    }

    // Validate São Paulo bounds
    if (!isWithinSaoPaulo(lat, lng)) {
      setSearchError("No data available in this address.");
      return;
    }

    // Perform search
    onSearch(lat, lng, radius);
  };

  /**
   * Handle radius slider change
   */
  const handleRadiusChange = (event, newValue) => {
    setRadius(newValue);
  };

  return (
    <Paper
      elevation={3}
      sx={{
        p: 3,
        backgroundColor: "#f5f5f5",
        borderRadius: 2,
      }}
    >
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
        Search Gas Stations
      </Typography>

      {/* Location Input Section */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="body2" gutterBottom sx={{ color: "#666" }}>
          Enter Coordinates (Latitude, Longitude)
        </Typography>
        <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
          <TextField
            label="Latitude"
            type="number"
            size="small"
            value={manualLat}
            onChange={(e) => setManualLat(e.target.value)}
            placeholder="-23.5"
            inputProps={{ step: "0.0001" }}
            disabled={loading}
            sx={{ flex: 1 }}
          />
          <TextField
            label="Longitude"
            type="number"
            size="small"
            value={manualLng}
            onChange={(e) => setManualLng(e.target.value)}
            placeholder="-46.6"
            inputProps={{ step: "0.0001" }}
            disabled={loading}
            sx={{ flex: 1 }}
          />
        </Box>
      </Box>

      {/* Radius Slider Section */}
      <Box sx={{ mb: 3 }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", mb: 1 }}>
          <Typography variant="body2" sx={{ fontWeight: 500 }}>
            Search Radius
          </Typography>
          <Typography variant="body2" sx={{ color: "#1976d2", fontWeight: 600 }}>
            {radius.toFixed(1)} km
          </Typography>
        </Box>
        <Slider
          value={radius}
          onChange={handleRadiusChange}
          min={MIN_RADIUS_KM}
          max={MAX_RADIUS_KM}
          step={0.5}
          marks
          valueLabelDisplay="auto"
          disabled={loading}
        />
      </Box>

      {/* Error Messages */}
      {searchError && (
        <Typography
          variant="body2"
          sx={{ color: "#d32f2f", mb: 2, fontWeight: 500 }}
        >
          ⚠️ {searchError}
        </Typography>
      )}
      {error && (
        <Typography
          variant="body2"
          sx={{ color: "#d32f2f", mb: 2, fontWeight: 500 }}
        >
          ⚠️ {error}
        </Typography>
      )}

      {/* Search Button */}
      <Button
        variant="contained"
        startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
        onClick={handleSearch}
        disabled={loading || !manualLat || !manualLng}
        fullWidth
        sx={{
          backgroundColor: "#1976d2",
          "&:hover": {
            backgroundColor: "#1565c0",
          },
        }}
      >
        {loading ? "Searching..." : "Search"}
      </Button>

      <Typography variant="caption" sx={{ display: "block", mt: 2, color: "#999" }}>
        💡 Tip: Use Avenida Paulista coordinates (-23.5505, -46.6561) to test
      </Typography>
    </Paper>
  );
};

export default SearchBar;
