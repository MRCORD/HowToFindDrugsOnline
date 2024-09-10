import React, { useEffect, useState } from 'react';
import ChatResponse from '../../components/ChatResponse';
import SearchForm from '../../components/SearchForm';
import { animationConfig } from '../../config/animationConfig';
import { fetchDistrictOptions, fetchMedicineOptions, searchDrugs } from '../../services/api';
import { useAnalytics } from '../../hooks/useAnalytics';
import {
  ContentWrapper,
  FadeWrapper,
  StyledContainer,
  StyledDivider,
  Subtitle,
  Title,
  ErrorMessage
} from './HomePage.styles';

const HomePage = () => {
  const { trackSearch, trackError, trackEvent } = useAnalytics();
  const [state, setState] = useState({
    searchResults: null,
    totalCount: 0,
    isFormDisabled: false,
    isLoading: false,
    isVisible: false,
    showContent: true,
    resetForm: false,
    medicineOptions: null,
    districtOptions: null,
    error: null,
  });

  const updateState = (newState) => {
    setState(prevState => ({ ...prevState, ...newState }));
  };

  useEffect(() => {
    const loadOptions = async () => {
      console.log('Loading options...');
      try {
        const [medicines, districts] = await Promise.all([
          fetchMedicineOptions(),
          fetchDistrictOptions()
        ]);
        console.log('Medicines:', medicines);
        console.log('Districts:', districts);
        updateState({ 
          medicineOptions: medicines.drugs,
          districtOptions: districts.districts,
        });
        console.log('State updated with options');
      } catch (error) {
        console.error('Error loading options:', error);
        updateState({ 
          medicineOptions: [],
          districtOptions: [],
          error: 'Failed to load options. Please try again later.',
        });
        trackError('Options Loading Error', error.message || 'Unknown error loading options');
      }
    };

    loadOptions();
    setTimeout(() => updateState({ isVisible: true }), 100);
  }, [trackError]);

  const handleSearch = async (selectedDrug, selectedDistrict) => {
    updateState({ isFormDisabled: true, isLoading: true, searchResults: null, totalCount: 0, resetForm: false, error: null });
    try {
      const results = await searchDrugs(selectedDrug, selectedDistrict.descripcion);
      updateState({ searchResults: results.drugs, totalCount: results.totalCount, isLoading: false });
      
      trackSearch(`${selectedDrug.dropdown} in ${selectedDistrict.descripcion}`, results.totalCount);
    } catch (error) {
      console.error('Error searching drugs:', error);
      updateState({ 
        isLoading: false, 
        searchResults: [], 
        totalCount: 0,
        error: error.message || 'Failed to search drugs. Please try again.',
      });
      trackError('Search Error', error.message || 'Unknown search error');
    } finally {
      updateState({ isFormDisabled: false });
    }
  };

  const handleRestart = () => {
    updateState({ isVisible: false });
    setTimeout(() => {
      updateState({
        searchResults: null,
        totalCount: 0,
        isFormDisabled: false,
        isLoading: false,
        showContent: false,
        resetForm: true,
        error: null,
      });
      setTimeout(() => updateState({ isVisible: true, showContent: true }), 100);
    }, animationConfig.fadeInDuration * 1000);
    trackEvent('User Action', 'Restart Search', 'User initiated new search');
  };

  const { searchResults, totalCount, isFormDisabled, isLoading, isVisible, showContent, resetForm, medicineOptions, districtOptions, error } = state;

  return (
    <StyledContainer maxWidth="md">
      <FadeWrapper className={isVisible ? 'visible' : ''}>
        <ContentWrapper>
          <Title variant="h1">
            Busca tu Pepa 💊
          </Title>
          <Subtitle variant="body1">
            ¡Hola! Soy tu asistente virtual de búsqueda de medicinas en Lima. Estoy aquí para ayudarte a encontrar las medicinas que necesitas. ¿En qué puedo ayudarte hoy?
          </Subtitle>
          {error && <ErrorMessage>{error}</ErrorMessage>}
          <SearchForm 
            onSearch={handleSearch} 
            disabled={isFormDisabled} 
            reset={resetForm}
            medicineOptions={medicineOptions}
            districtOptions={districtOptions}
          />
          {showContent && (isLoading || searchResults) && (
            <>
              <StyledDivider />
              <ChatResponse
                results={searchResults || []}
                totalCount={totalCount}
                isLoading={isLoading}
                onRestart={handleRestart}
              />
            </>
          )}
        </ContentWrapper>
      </FadeWrapper>
    </StyledContainer>
  );
};

export default HomePage;