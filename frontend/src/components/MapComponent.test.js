import React from 'react';
import { render, screen } from '@testing-library/react';
import MapComponent from './MapComponent';
import { StationContext } from '../context/StationContext';

test('renders the Google Maps iframe', () => {
  render(
    <StationContext.Provider value={{ searchCenter: { lat: -23.55, lng: -46.65 }, stations: [] }}>
      <MapComponent />
    </StationContext.Provider>
  );
  const iframe = screen.getByTitle(/map/i);
  expect(iframe).toBeInTheDocument();
});