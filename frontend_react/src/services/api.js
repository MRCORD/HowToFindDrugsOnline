import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

const isDevelopment = process.env.NODE_ENV === 'development';

const devLog = (...args) => {
  if (isDevelopment) {
    console.log(...args);
  }
};

const getCachedData = (key) => {
  const cachedData = localStorage.getItem(key);
  if (cachedData) {
    const { data, timestamp } = JSON.parse(cachedData);
    if (Date.now() - timestamp < CACHE_DURATION) {
      devLog(`Returning cached ${key}:`, data);
      return data;
    }
  }
  return null;
};

const setCachedData = (key, data) => {
  const cacheObject = { data, timestamp: Date.now() };
  localStorage.setItem(key, JSON.stringify(cacheObject));
  devLog(`Cached ${key}:`, data);
};

export const fetchMedicineOptions = async () => {
  devLog('Fetching medicine options...');
  const cachedMedicines = getCachedData('medicineOptions');
  if (cachedMedicines) {
    return cachedMedicines;
  }

  try {
    const response = await axios.get(`${API_URL}/v1/drugs/unique_drugs`);
    devLog('Medicine options response:', response.data);
    const medicines = response.data;
    setCachedData('medicineOptions', medicines);
    return medicines;
  } catch (error) {
    console.error('Error fetching medicine options:', error);
    throw error;
  }
};

export const fetchDistrictOptions = async () => {
  devLog('Fetching district options...');
  const cachedDistricts = getCachedData('districtOptions');
  if (cachedDistricts) {
    return cachedDistricts;
  }

  try {
    const response = await axios.get(`${API_URL}/v1/drugs/unique_districts`);
    devLog('District options response:', response.data);
    const districts = response.data;
    setCachedData('districtOptions', districts);
    return districts;
  } catch (error) {
    console.error('Error fetching district options:', error);
    throw error;
  }
};

export const searchDrugs = async (selectedDrug, selectedDistrict) => {
  try {
    devLog('Searching drugs with:', { selectedDrug, selectedDistrict });

    if (!selectedDrug || !selectedDistrict) {
      throw new Error('Selected drug or district is missing');
    }

    const { searchTerm, concent, nombreFormaFarmaceutica } = selectedDrug;

    devLog('Parsed drug info:', { searchTerm, concent, nombreFormaFarmaceutica });

    const response = await axios.post(`${API_URL}/v1/drugs/filtered_drugs`, {
      selected_drug: searchTerm,
      concent,
      nombreFormaFarmaceutica,
      selected_distrito: selectedDistrict
    });

    devLog('Search drugs response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error searching drugs:', error);
    throw error;
  }
};