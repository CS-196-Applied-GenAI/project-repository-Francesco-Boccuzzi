import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./SearchPage.css";

/**
 * Search Page Component
 * Displays horizontal search bar with address dropdown, range selector, and Go button
 * Shows "service not available" message when Go is clicked
 */
const SearchPage = () => {
  const navigate = useNavigate();
  const [selectedAddress, setSelectedAddress] = useState("");
  const [selectedRange, setSelectedRange] = useState("1km");
  const [showMessage, setShowMessage] = useState(false);

  const addressOptions = [
    "Parque do Ibirapuera",
    "MASP, Avenida Paulista",
    "Allianz Parque",
    "Universidade de São Paulo",
  ];

  const rangeOptions = ["1km", "2km", "3km"];

  const handleGoClick = () => {
    setShowMessage(true);
  };

  const handleBackClick = () => {
    navigate("/");
  };

  return (
    <div className="search-page">
      {/* Back Button */}
      <button className="back-button" onClick={handleBackClick}>
        ← Back
      </button>

      {/* Search Bar Container */}
      <div className="search-container">
        <div className="search-bar">
          {/* Address Dropdown */}
          <select
            className="search-input address-input"
            value={selectedAddress}
            onChange={(e) => setSelectedAddress(e.target.value)}
            placeholder="Select an address"
          >
            <option value="">Select an address</option>
            {addressOptions.map((address) => (
              <option key={address} value={address}>
                {address}
              </option>
            ))}
          </select>

          {/* Range Dropdown */}
          <select
            className="search-input range-input"
            value={selectedRange}
            onChange={(e) => setSelectedRange(e.target.value)}
          >
            {rangeOptions.map((range) => (
              <option key={range} value={range}>
                {range}
              </option>
            ))}
          </select>

          {/* Go Button */}
          <button className="go-button" onClick={handleGoClick}>
            Go
          </button>
        </div>

        {/* Service Not Available Message */}
        {showMessage && (
          <div className="message-container">
            <p className="service-message">Sorry, this service is not available yet</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
