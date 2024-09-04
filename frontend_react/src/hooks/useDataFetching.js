import { useState, useEffect } from 'react';
import { fetchDrugsAndDistricts, searchDrugs } from '../services/api';

const useDataFetching = () => {
  const [drugs, setDrugs] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const { drugs, districts } = await fetchDrugsAndDistricts();
        setDrugs(drugs);
        setDistricts(districts);
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const handleSearch = async (drug, district) => {
    setIsLoading(true);
    try {
      const results = await searchDrugs(drug, district);
      setSearchResults(results);
    } catch (error) {
      console.error('Error searching drugs:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return { drugs, districts, isLoading, searchResults, handleSearch };
};

export default useDataFetching;