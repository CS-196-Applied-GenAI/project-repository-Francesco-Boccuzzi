import React from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css";

/**
 * Landing Page Component
 * Displays welcome message and CTA button to start searching
 */
const LandingPage = () => {
  const navigate = useNavigate();

  const handleStartSearching = () => {
    navigate("/search");
  };

  return (
    <div className="landing-page">
      <div className="landing-content">
        <h1 className="landing-title">Welcome to GasPriceTracker.com!</h1>
        <p className="landing-description">
          Input your address, choose a range and find the gas stations with the cheapest prices near you!
        </p>
        <p className="landing-description">
          Don't hesitate. Experiment and start saving!
        </p>
        <button className="cta-button" onClick={handleStartSearching}>
          Start Searching
        </button>
      </div>
    </div>
  );
};

export default LandingPage;
