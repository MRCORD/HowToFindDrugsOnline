import { animationConfig } from '../config/animationConfig';

// Simulated API call
const searchDrugs = async (drug, district) => {
  // Simulate API delay using the loadingMessageDuration
  await new Promise(resolve => setTimeout(resolve, animationConfig.loadingMessageDuration * 1000));
  
  return [
    {
      nombreProducto: drug,
      precio: 10.50,
      farmacia: 'Farmacia Universal',
      direccion: 'Av. Example 123, ' + district,
    },
    {
      nombreProducto: drug,
      precio: 9.75,
      farmacia: 'Inkafarma',
      direccion: 'Jr. Sample 456, ' + district,
    },
    {
      nombreProducto: drug,
      precio: 11.25,
      farmacia: 'Mifarma',
      direccion: 'Calle Test 789, ' + district,
    },
  ];
};

export { searchDrugs };