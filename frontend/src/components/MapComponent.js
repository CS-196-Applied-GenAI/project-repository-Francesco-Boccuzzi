/* Google Maps Embed API component for displaying a static map */

import React from "react";
import { Box, Typography, Button } from "@mui/material";
import { useStations } from "../context/StationContext";
import { GOOGLE_MAPS_API_KEY } from "../config";

/**
 * MapComponent
 * 
 * Uses Google Maps Embed API to display a static map of the search area.
 * 
 * Features:
 * - Shows search center location with embedded map
 * - Static map (no interactive markers due to Embed API limitations)
 * - Station details available in the sidebar list
 * - Direct links to Google Maps for each station
 */
const MapComponent = () => {
  const { searchCenter, stations, cheapestStationId } = useStations();

  /**
   * Find the cheapest station to highlight on map
   */
  const getCheapestStation = () => {
    if (!cheapestStationId || !stations) return null;
    return stations.find(s => s.station_id === cheapestStationId);
  };

  /**
   * Generate embedded map URL
   * Uses the search center coordinates
   */
  const getEmbedMapUrl = () => {
    if (!searchCenter) return null;
    
    const { latitude, longitude } = searchCenter;
    const embedUrl = `https://www.google.com/maps/embed/v1/place?key=${GOOGLE_MAPS_API_KEY}&q=${latitude},${longitude}&zoom=14`;
    return embedUrl;
  };

  const embedUrl = getEmbedMapUrl();
  const cheapestStation = getCheapestStation();

  if (!searchCenter) {
    return (
      <Box
        sx={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#f5f5f5",
          flexDirection: "column",
          gap: 2,
        }}
      >
        <Typography variant="body2" sx={{ color: "#999" }}>
          Search for a location to see the map
        </Typography>
      </Box>
    );
  }

  if (!embedUrl) {
    return (
      <Box
        sx={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#f5f5f5",
        }}
      >
        <Typography variant="body2" sx={{ color: "#d32f2f" }}>
          Map API key not configured
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: "100%", height: "100%", display: "flex", flexDirection: "column" }}>
      {/* Embedded Map */}
      <Box sx={{ flex: 1, position: "relative" }}>
        <iframe
          title="Gas Stations Map"
          width="100%"
          height="100%"
          style={{ border: 0, borderRadius: "8px" }}
          src={embedUrl}
          allowFullScreen=""
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
        />
      </Box>

      {/* Cheapest Station Info Bar */}
      {cheapestStation && (
        <Box
          sx={{
            p: 2,
            backgroundColor: "#e8f5e9",
            borderTop: "2px solid #4caf50",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: 2,
          }}
        >
          <Box>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, color: "#2e7d32" }}>
              💰 Cheapest: {cheapestStation.name}
            </Typography>
            <Typography variant="caption" sx={{ color: "#388e3c" }}>
              R$ {cheapestStation.gasolina_comum_price?.toFixed(2) || "N/A"} •{" "}
              {cheapestStation.distance_km?.toFixed(2) || "0"} km away
            </Typography>
          </Box>
          <Button
            variant="contained"
            size="small"
            href={`https://www.google.com/maps/dir/?api=1&destination=${cheapestStation.latitude},${cheapestStation.longitude}`}
            target="_blank"
            rel="noopener noreferrer"
            sx={{
              backgroundColor: "#4caf50",
              "&:hover": { backgroundColor: "#388e3c" },
            }}
          >
            📍 Navigate
          </Button>
        </Box>
      )}

      {/* Info Text */}
      <Typography
        variant="caption"
        sx={{
          p: 1,
          backgroundColor: "#f5f5f5",
          textAlign: "center",
          color: "#999",
          borderTop: "1px solid #e0e0e0",
        }}
      >
        💡 Use the sidebar to view all stations and their details. Click to navigate to each station.
      </Typography>
    </Box>
  );
};

export default MapComponent;
