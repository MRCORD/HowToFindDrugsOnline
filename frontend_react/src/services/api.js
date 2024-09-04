import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

// export const fetchDrugsAndDistricts = async () => {
//   try {
//     const response = await axios.get(`${API_URL}/drugs-and-districts`);
//     return response.data;
//   } catch (error) {
//     console.error('Error fetching drugs and districts:', error);
//     throw error;
//   }
// };

// export const searchDrugs = async (drug, district) => {
//   try {
//     const response = await axios.post(`${API_URL}/search`, { drug, district });
//     return response.data;
//   } catch (error) {
//     console.error('Error searching drugs:', error);
//     throw error;
//   }
// };

// Test data for drugs and districts
const testDrugs = [
  { value: 'paracetamol', label: 'Paracetamol' },
  { value: 'ibuprofeno', label: 'Ibuprofeno' },
  { value: 'amoxicilina', label: 'Amoxicilina' },
  { value: 'omeprazol', label: 'Omeprazol' },
  { value: 'loratadina', label: 'Loratadina' },
];

const testDistricts = [
  { value: 'lima', label: 'Lima' },
  { value: 'miraflores', label: 'Miraflores' },
  { value: 'sanisidro', label: 'San Isidro' },
  { value: 'barranco', label: 'Barranco' },
  { value: 'surco', label: 'Surco' },
];

export const fetchDrugsAndDistricts = async () => {
  // Simulating API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  return { drugs: testDrugs, districts: testDistricts };
};

export const searchDrugs = async (drug, district) => {
  // Simulating API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Generate some mock results
  return [
    {
      nombreProducto: drug,
      precio: Math.random() * 50 + 1, // Random price between 1 and 51
      farmacia: 'Farmacia Test',
      direccion: `Av. Principal 123, ${district}`,
    },
    {
      nombreProducto: drug,
      precio: Math.random() * 50 + 1,
      farmacia: 'Botica Test',
      direccion: `Jr. Secundario 456, ${district}`,
    },
  ];
};