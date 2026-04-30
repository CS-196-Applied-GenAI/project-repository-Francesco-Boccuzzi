import axios from 'axios';
import { searchStations, updateStationPrice } from './api';

// 1. Mock axios. This factory is hoisted to the top.
jest.mock('axios', () => {
  const mockAxiosInstance = {
    get: jest.fn(),
    patch: jest.fn(),
    headers: { 'Content-Type': 'application/json' }
  };
  return {
    create: jest.fn(() => mockAxiosInstance),
    // Export the instance methods so we can access them in tests
    mockInstance: mockAxiosInstance 
  };
});

describe('API Service', () => {
  // 2. Get a reference to the mocked instance to control its behavior
  const mockClient = require('axios').mockInstance;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('searchStations fetches data successfully', async () => {
    const mockData = { stations: [], count: 0 };
    mockClient.get.mockResolvedValue({ data: mockData });

    const result = await searchStations(-23.55, -46.63, 2.0);
    
    expect(result).toEqual(mockData);
    expect(mockClient.get).toHaveBeenCalledWith("/api/stations", expect.any(Object));
  });

  test('updateStationPrice updates data successfully', async () => {
    const mockUpdate = { id: '1', gasolina_comum_price: 6.50 };
    mockClient.patch.mockResolvedValue({ data: mockUpdate });

    const result = await updateStationPrice('1', { gasolina_comum_price: 6.50 });
    
    expect(result).toEqual(mockUpdate);
    expect(mockClient.patch).toHaveBeenCalledWith("/api/stations/1", { gasolina_comum_price: 6.50 });
  });
});