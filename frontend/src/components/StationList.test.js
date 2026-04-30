import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import StationList from './StationList';
import { StationContext } from '../context/StationContext';

const mockStations = [
  { 
    station_id: 'station-123', // Ensure this field exists and is unique
    name: 'Posto Paulista', 
    bandeira: 'Shell', 
    gasolina_comum_price: 5.89, 
    distance_km: 0.5,
    last_verified_at: '2023-10-27T10:00:00'
  }
];

test('renders stations and highlights the cheapest one', () => {
  render(
    <StationContext.Provider value={{ 
      stations: mockStations, 
      loading: false, 
      cheapestStationId: '1',
      selectedStationId: null 
    }}>
      <StationList />
    </StationContext.Provider>
  );

  expect(screen.getByText('Posto Paulista')).toBeInTheDocument();
  expect(screen.getByText(/Cheapest/i)).toBeInTheDocument(); // Badge verification
});