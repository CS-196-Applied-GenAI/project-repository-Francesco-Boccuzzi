import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchBar from './SearchBar';
import { StationContext } from '../context/StationContext';

// Mock function for the onSearch prop
const mockOnSearch = jest.fn();

describe('SearchBar Component', () => {
  test('calls onSearch with correct coordinates and radius', () => {
    render(
      <StationContext.Provider value={{ loading: false, error: null }}>
        <SearchBar onSearch={mockOnSearch} />
      </StationContext.Provider>
    );

    const latInput = screen.getByLabelText(/latitude/i);
    const lngInput = screen.getByLabelText(/longitude/i);
    
    // Use valid São Paulo coordinates to pass geofencing validation
    fireEvent.change(latInput, { target: { value: '-23.5505' } });
    fireEvent.change(lngInput, { target: { value: '-46.6561' } });

    const searchButton = screen.getByRole('button', { name: /search/i });
    fireEvent.click(searchButton);

    expect(mockOnSearch).toHaveBeenCalledWith(-23.5505, -46.6561, 2.0);
  });
});