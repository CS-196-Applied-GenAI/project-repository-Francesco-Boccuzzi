import axios from 'axios';
import { searchStations } from './api';

jest.mock('axios');

test('searchStations fetches data from API', async () => {
  const stations = [{ id: 1, name: 'Shell', price: 5.50 }];
  axios.get.mockResolvedValue({ data: stations });

  const result = await searchStations(-23.55, -46.63, 2);
  
  expect(axios.get).toHaveBeenCalledWith(
    expect.stringContaining('/api/stations'),
    expect.any(Object)
  );
  expect(result).toEqual(stations);
});