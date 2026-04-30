import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // CRITICAL IMPORT
import MapComponent from './MapComponent';
import { StationContext } from '../context/StationContext';

test('renders the Google Maps iframe', () => {
  const mockValue = { searchCenter: { latitude: -23.55, longitude: -46.65 }, stations: [] };
  render(
    <StationContext.Provider value={mockValue}>
      <MapComponent />
    </StationContext.Provider>
  );
  const iframe = screen.getByTitle(/map/i);
  expect(iframe).toBeInTheDocument();
});