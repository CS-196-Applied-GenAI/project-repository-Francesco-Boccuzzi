/* Station sidebar component showing list of nearby stations */

import React from "react";
import {
  Box,
  Paper,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
  Chip,
  Divider,
  Button,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import LocalGasStationIcon from "@mui/icons-material/LocalGasStation";
import { useStations } from "../context/StationContext";

/**
 * StationList Component
 * 
 * Displays stations in a sidebar with:
 * - Sorting by price (cheapest first)
 * - Station name, brand, price, and distance
 * - Last verified date in DD/MM/YYYY format
 * - Visual highlight for cheapest station (green chip)
 * - Direct links to navigate to each station
 * - Mobile-responsive design
 */
const StationList = ({ onStationSelect }) => {
  const {
    stations,
    loading,
    error,
    selectedStationId,
    cheapestStationId,
    searchCenter,
  } = useStations();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  /**
   * Format date to DD/MM/YYYY format
   */
  const formatDate = (dateString) => {
    if (!dateString) return "Not verified";
    const date = new Date(dateString);
    return date.toLocaleDateString("pt-BR");
  };

  /**
   * Format price with currency symbol
   */
  const formatPrice = (price) => {
    if (price === null || price === undefined) return "N/A";
    return `R$ ${price.toFixed(2)}`;
  };

  /**
   * Generate Google Maps navigation link
   */
  const getGoogleMapsLink = (lat, lng) => {
    return `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
  };

  // Show loading state
  if (loading) {
    return (
      <Paper
        sx={{
          p: 2,
          backgroundColor: "#fff",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Typography variant="body2">Loading stations...</Typography>
      </Paper>
    );
  }

  // Show error state
  if (error) {
    return (
      <Paper
        sx={{
          p: 2,
          backgroundColor: "#fff",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Typography variant="body2" sx={{ color: "#d32f2f" }}>
          {error}
        </Typography>
      </Paper>
    );
  }

  // Show empty state
  if (stations.length === 0) {
    return (
      <Paper
        sx={{
          p: 2,
          backgroundColor: "#fff",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Typography variant="body2" sx={{ color: "#999" }}>
          Search for a location to see nearby stations
        </Typography>
      </Paper>
    );
  }

  // Sort stations by price (cheapest first)
  const sortedStations = [...stations].sort((a, b) => {
    const priceA = a.gasolina_comum_price ?? Infinity;
    const priceB = b.gasolina_comum_price ?? Infinity;
    return priceA - priceB;
  });

  return (
    <Paper
      sx={{
        backgroundColor: "#fff",
        height: "100%",
        overflow: "auto",
        borderRadius: 2,
      }}
    >
      {/* Header with count */}
      <Box sx={{ p: 2, backgroundColor: "#f5f5f5", borderBottom: "1px solid #e0e0e0" }}>
        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
          Nearby Stations ({stations.length})
        </Typography>
        <Typography variant="caption" sx={{ color: "#999" }}>
          Sorted by price (cheapest first)
        </Typography>
      </Box>

      {/* Stations List */}
      <List sx={{ p: 0 }}>
        {sortedStations.map((station, index) => {
          const isCheapest = cheapestStationId === station.station_id;

          return (
            <Box key={station.station_id}>
              <ListItem
                disablePadding
                secondaryAction={
                  <Button
                    variant="text"
                    size="small"
                    href={getGoogleMapsLink(station.latitude, station.longitude)}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{ color: "#1976d2", textTransform: "none", fontSize: "0.75rem" }}
                  >
                    📍 Go
                  </Button>
                }
              >
                <ListItemButton
                  onClick={() => onStationSelect(station.station_id)}
                  sx={{
                    backgroundColor: selectedStationId === station.station_id ? "#e3f2fd" : "transparent",
                    "&:hover": {
                      backgroundColor: "#f5f5f5",
                    },
                    borderLeft:
                      selectedStationId === station.station_id
                        ? "4px solid #1976d2"
                        : "4px solid transparent",
                  }}
                >
                  <ListItemText
                    primary={
                      <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 0.5 }}>
                        <LocalGasStationIcon sx={{ fontSize: "1.2rem", color: "#1976d2" }} />
                        <Typography variant="body2" sx={{ fontWeight: 600, flex: 1 }}>
                          {station.name}
                        </Typography>
                        {isCheapest && (
                          <Chip
                            label="Cheapest"
                            size="small"
                            sx={{
                              backgroundColor: "#4caf50",
                              color: "white",
                              height: "24px",
                              fontWeight: 600,
                            }}
                          />
                        )}
                      </Box>
                    }
                    secondary={
                      <Box sx={{ mt: 0.5 }}>
                        <Typography variant="caption" sx={{ display: "block", color: "#666" }}>
                          <strong>Brand:</strong> {station.bandeira}
                        </Typography>
                        <Typography variant="caption" sx={{ display: "block", color: "#666" }}>
                          <strong>Price:</strong> {formatPrice(station.gasolina_comum_price)}
                        </Typography>
                        <Typography variant="caption" sx={{ display: "block", color: "#666" }}>
                          <strong>Distance:</strong> {station.distance_km?.toFixed(2) || "N/A"} km
                        </Typography>
                        <Typography variant="caption" sx={{ display: "block", color: "#999", mt: 0.5 }}>
                          Last verified: {formatDate(station.last_verified_at)}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItemButton>
              </ListItem>
              {index < sortedStations.length - 1 && <Divider />}
            </Box>
          );
        })}
      </List>
    </Paper>
  );
};

export default StationList;
