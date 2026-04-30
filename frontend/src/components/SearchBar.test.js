import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SearchBar from './SearchBar';
import { StationContext } from '../context/StationContext';

const mockSearchStations = jest.fn();

const renderWithContext = (component) => {
  return render(
    <StationContext.Provider value={{ searchStations: mockSearchStations, loading: false }}>
      {component}
    </StationContext.Provider>
  );
};

test('updates latitude and longitude inputs', () => {
  renderWithContext(<SearchBar />);
  
  const latInput = screen.getByLabelText(/latitude/i);
  const lngInput = screen.getByLabelText(/longitude/i);

  fireEvent.change(latInput, { target: { value: '-23.55' } });
  fireEvent.change(lngInput, { target: { value: '-46.63' } });

  expect(latInput.value).toBe('-23.55');
  expect(lngInput.value).toBe('-46.63');
});

test('calls searchStations on button click', () => {
  renderWithContext(<SearchBar />);
  const searchButton = screen.getByRole('button', { name: /search/i });
  
  fireEvent.click(searchButton);
  expect(mockSearchStations).toHaveBeenCalled();
});