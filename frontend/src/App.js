/* Main application component */

import React, { useRef } from "react";
import { Box, Container, Grid, AppBar, Toolbar, Typography, useTheme, useMediaQuery } from "@mui/material";
import { StationProvider, useStations } from "./context/StationContext";
import SearchBar from "./components/SearchBar";
import MapComponent from "./components/MapComponent";
import StationList from "./components/StationList";
import "./App.css";

/**
 * Inner App Component
 * Uses StationContext and renders the main layout
 */
const AppContent = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const googleMapRef = useRef(null);
  const { performSearch, setSelectedStationId } = useStations();

  /**
   * Handle search from SearchBar component
   */
  const handleSearch = (latitude, longitude, radius) => {
    performSearch(latitude, longitude, radius);
  };

  /**
   * Handle station selection from StationList
   */
  const handleStationSelect = (stationId) => {
    setSelectedStationId(stationId);
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      {/* Header */}
      <AppBar position="static" sx={{ backgroundColor: "#1565c0" }}>
        <Toolbar>
          <Typography variant="h6" sx={{ fontWeight: 600, flex: 1 }}>
            ⛽ São Paulo Gas Price Tracker
          </Typography>
          <Typography variant="caption" sx={{ color: "#e0e0e0" }}>
            Find the cheapest gas stations near you
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Box sx={{ flex: 1, overflow: "hidden" }}>
        {isMobile ? (
          // Mobile Layout: Stack vertically
          <Box sx={{ display: "flex", flexDirection: "column", height: "100%", p: 1, gap: 1 }}>
            <SearchBar onSearch={handleSearch} />
            <Box sx={{ flex: 1, overflow: "hidden", borderRadius: 2 }}>
              <MapComponent googleMapRef={googleMapRef} />
            </Box>
            <Box sx={{ height: "200px", overflow: "auto" }}>
              <StationList onStationSelect={handleStationSelect} />
            </Box>
          </Box>
        ) : (
          // Desktop Layout: Side-by-side with sidebar
          <Grid container sx={{ height: "100%", p: 2, gap: 2 }}>
            {/* Left Column: Search and Map */}
            <Grid item xs={12} md={8} sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
              <SearchBar onSearch={handleSearch} />
              <Box
                sx={{
                  flex: 1,
                  overflow: "hidden",
                  borderRadius: 2,
                  boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)",
                }}
              >
                <MapComponent googleMapRef={googleMapRef} />
              </Box>
            </Grid>

            {/* Right Column: Station List */}
            <Grid item xs={12} md={4} sx={{ overflow: "hidden" }}>
              <StationList onStationSelect={handleStationSelect} />
            </Grid>
          </Grid>
        )}
      </Box>
    </Box>
  );
};

/**
 * Main App Component
 * Wraps content with StationProvider context
 */
function App() {
  return (
    <StationProvider>
      <AppContent />
    </StationProvider>
  );
}

export default App;
