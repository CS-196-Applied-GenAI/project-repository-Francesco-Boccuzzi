import React from 'react';
import { render, act } from '@testing-library/react';
import { StationProvider, useStations } from './StationContext';
import * as api from '../services/api';

jest.mock('../services/api');

const TestComponent = () => {
  const { performSearch, stations } = useStations();
  return (
    <div>
      <div data-testid="count">{stations.length}</div>
      <button onClick={() => performSearch(-23.55, -46.63, 2.0)}>Search</button>
    </div>
  );
};

test('performSearch updates stations in state', async () => {
  api.searchStations.mockResolvedValue({ stations: [{ station_id: '1', name: 'Posto' }] });

  const { getByTestId, getByText } = render(
    <StationProvider>
      <TestComponent />
    </StationProvider>
  );

  await act(async () => {
    getByText('Search').click();
  });

  expect(getByTestId('count').textContent).toBe('1');
});