import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
// console.log('API_URL:', API_URL); // This log will be visible during build time

const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

const getCachedData = (key) => {
  const cachedData = localStorage.getItem(key);
  if (cachedData) {
    const { data, timestamp } = JSON.parse(cachedData);
    if (Date.now() - timestamp < CACHE_DURATION) {
      console.log(`Returning cached ${key}:`, data);
      return data;
    }
  }
  return null;
};

const setCachedData = (key, data) => {
  const cacheObject = { data, timestamp: Date.now() };
  localStorage.setItem(key, JSON.stringify(cacheObject));
  console.log(`Cached ${key}:`, data);
};

export const fetchMedicineOptions = async () => {
  console.log('Fetching medicine options...');
  const cachedMedicines = getCachedData('medicineOptions');
  if (cachedMedicines) {
    return cachedMedicines;
  }

  try {
    const response = await axios.get(`${API_URL}/v1/unique_drugs`);
    console.log('Medicine options response:', response.data);
    const medicines = response.data;
    setCachedData('medicineOptions', medicines);
    return medicines;
  } catch (error) {
    console.error('Error fetching medicine options:', error);
    throw error;
  }
};

export const fetchDistrictOptions = async () => {
  console.log('Fetching district options...');
  const cachedDistricts = getCachedData('districtOptions');
  if (cachedDistricts) {
    return cachedDistricts;
  }

  try {
    const response = await axios.get(`${API_URL}/v1/unique_districts`);
    console.log('District options response:', response.data);
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
    console.log('Searching drugs with:', { selectedDrug, selectedDistrict });

    if (!selectedDrug || !selectedDistrict) {
      throw new Error('Selected drug or district is missing');
    }

    let drugName, concent, nombreFormaFarmaceutica;

    const parts = selectedDrug.split(' [');
    if (parts.length === 2) {
      [drugName, nombreFormaFarmaceutica] = parts;
      nombreFormaFarmaceutica = nombreFormaFarmaceutica.replace(']', '').trim();

      const concentParts = drugName.match(/(\d+(\.\d+)?\s*[a-zA-Z]+)$/);
      if (concentParts) {
        concent = concentParts[0].trim();
        drugName = drugName.replace(concent, '').trim();
      } else {
        throw new Error('Unable to parse drug concentration');
      }
    } else {
      throw new Error('Invalid drug format');
    }

    console.log('Parsed drug info:', { drugName, concent, nombreFormaFarmaceutica });

    const response = await axios.post(`${API_URL}/v1/filtered_drugs`, {
      selected_drug: drugName,
      concent,
      nombreFormaFarmaceutica,
      selected_distrito: selectedDistrict
    });

    console.log('Search drugs response:', response.data);
    return response.data; // This now includes both totalCount and drugs
  } catch (error) {
    console.error('Error searching drugs:', error);
    throw error;
  }
};