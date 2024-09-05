import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

const getCachedData = (key) => {
  const cachedData = localStorage.getItem(key);
  if (cachedData) {
    const { data, timestamp } = JSON.parse(cachedData);
    if (Date.now() - timestamp < CACHE_DURATION) {
      return data;
    }
  }
  return null;
};

const setCachedData = (key, data) => {
  const cacheObject = { data, timestamp: Date.now() };
  localStorage.setItem(key, JSON.stringify(cacheObject));
};

export const fetchMedicineOptions = async () => {
  const cachedMedicines = getCachedData('medicineOptions');
  if (cachedMedicines) {
    return cachedMedicines;
  }

  // Simulating API call
  await new Promise(resolve => setTimeout(resolve, 1000));
  const medicines = {
    drugs: [
      {
        searchTerm: "AMITRIPTILINA CLORHIDRATO",
        concent: "25 mg",
        nombreFormaFarmaceutica: "Tableta",
        dropdown: "AMITRIPTILINA CLORHIDRATO 25 mg [Tableta]"
      },
      {
        searchTerm: "AMITRIPTILINA CLORHIDRATO",
        concent: "25 mg",
        nombreFormaFarmaceutica: "Tableta Recubierta",
        dropdown: "AMITRIPTILINA CLORHIDRATO 25 mg [Tableta Recubierta]"
      },
      // Add more simulated medicines as needed
    ]
  };
  setCachedData('medicineOptions', medicines);
  return medicines;
};

export const fetchDistrictOptions = async () => {
  const cachedDistricts = getCachedData('districtOptions');
  if (cachedDistricts) {
    return cachedDistricts;
  }

  // Simulating API call
  await new Promise(resolve => setTimeout(resolve, 1000));
  const districts = {
    districts: [
      { descripcion: "ANCON" },
      { descripcion: "ATE" },
      { descripcion: "BARRANCO" },
      { descripcion: "BREÑA" },
      { descripcion: "CARABAYLLO" },
      { descripcion: "MIRAFLORES" },
      { descripcion: "SURCO" },
      // Add more simulated districts as needed
    ]
  };
  setCachedData('districtOptions', districts);
  return districts;
};

export const searchDrugs = async (selectedDrug, selectedDistrict) => {
  // Simulating API call
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  return {
    drugs: [
      {
        _id: "664924cca96f7a2b14846c6b",
        nombreProducto: selectedDrug.searchTerm,
        concent: selectedDrug.concent,
        nombreFormaFarmaceutica: selectedDrug.nombreFormaFarmaceutica,
        precio2: 0.12,
        nombreComercial: "FARMACIA DEL HOSPITAL DE EMERGENCIAS JOSE CASIMIRO ULLOA",
        direccion: "AV. REPUBLICA DE PANAMA  6355",
        googleMaps_search_url: "https://www.google.com/maps/place/Av.+República+de+Panamá+6355-6375%2C+Miraflores+15047%2C+Peru/@-12.1281188,-77.0177211,17z",
        googleMapsUri: "https://maps.google.com/?cid=6407837351487944386"
      },
      {
        _id: "664924cca96f7a2b14847afe",
        nombreProducto: selectedDrug.searchTerm,
        concent: selectedDrug.concent,
        nombreFormaFarmaceutica: selectedDrug.nombreFormaFarmaceutica,
        precio2: 0.12,
        nombreComercial: "BOTICA ALEMANA S.A.C.",
        direccion: "AV. LARCO N° 1150 INTERIOR 24 - MEZANINE DEL \"EDIFICIO COMERCIAL LARCO 1150\"  ",
        googleMaps_search_url: "https://www.google.com/maps/place/interior+24%2C+Av.+José+Larco+1150%2C+Miraflores+15074%2C+Peru/@-12.1291951,-77.02992379999999,17z",
        googleMapsUri: "https://maps.google.com/?cid=17301418492810050510"
      },
      {
        _id: "664924cca96f7a2b14847ba2",
        nombreProducto: selectedDrug.searchTerm,
        concent: selectedDrug.concent,
        nombreFormaFarmaceutica: selectedDrug.nombreFormaFarmaceutica,
        precio2: 0.13,
        nombreComercial: "BOTICA NEOSALUD",
        direccion: "CALLE JORGE BUCKLEY Nº 140, SAN ANTONIO ",
        googleMaps_search_url: "https://www.google.com/maps/place/C.+Jorge+Buckley+140%2C+Miraflores+15048%2C+Peru/@-12.1262053,-77.01629009999999,17z",
        googleMapsUri: "https://maps.google.com/?cid=16472674239638043924"
      }
      // Add more simulated results as needed
    ]
  };
};