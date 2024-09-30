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
  ErrorMessage,
  LoadingWrapper,
  LoadingText
} from './HomePage.styles';
import { CircularProgress } from '@mui/material';

const HomePage = () => {
  const { trackEvent, setGroup, GROUP_TYPES, EVENT_TYPES } = useAnalytics();
  const [state, setState] = useState({
    searchResults: null,
    totalCount: 0,
    isFormDisabled: true,
    isLoading: true,
    isVisible: false,
    showContent: false,
    resetForm: false,
    medicineOptions: null,
    districtOptions: null,
    error: null,
    isSearching: false,
  });

  const updateState = (newState) => {
    setState(prevState => ({ ...prevState, ...newState }));
  };

  useEffect(() => {
    const loadOptions = async () => {
      try {
        const [medicines, districts] = await Promise.all([
          fetchMedicineOptions(),
          fetchDistrictOptions()
        ]);
        updateState({ 
          medicineOptions: medicines, // API now returns the array directly
          districtOptions: districts, // API now returns the array directly
          isFormDisabled: false,
          isLoading: false
        });
      } catch (error) {
        updateState({ 
          medicineOptions: [],
          districtOptions: [],
          error: 'Failed to load options. Please try again later.',
          isLoading: false
        });
        trackEvent(EVENT_TYPES.ERROR, {
          category: 'Data Loading',
          action: 'Options Loading Error',
          label: error.message || 'Unknown error loading options'
        });
      }
    };

    loadOptions();
    setTimeout(() => updateState({ isVisible: true }), 100);
  }, [trackEvent, EVENT_TYPES]);

  const handleSearch = async (selectedDrug, selectedDistrict) => {
    updateState({ isFormDisabled: true, isSearching: true, searchResults: null, totalCount: 0, resetForm: false, error: null, showContent: true });
    try {
      const results = await searchDrugs(selectedDrug, selectedDistrict.descripcion);
      updateState({ searchResults: results.drugs, totalCount: results.totalCount, isSearching: false });
      
      setGroup(GROUP_TYPES.DISTRICT, selectedDistrict.descripcion, {
        name: selectedDistrict.descripcion,
      });
      
      trackEvent(EVENT_TYPES.SEARCH_SUBMITTED, {
        category: 'Drug Search',
        action: 'Perform Search',
        label: `${selectedDrug.dropdown} in ${selectedDistrict.descripcion}`,
        value: results.totalCount
      });
    } catch (error) {
      updateState({ 
        isSearching: false, 
        searchResults: [], 
        totalCount: 0,
        error: error.message || 'Failed to search drugs. Please try again.',
      });
      trackEvent(EVENT_TYPES.ERROR, {
        category: 'Drug Search',
        action: 'Search Error',
        label: error.message || 'Unknown search error'
      });
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
        isSearching: false,
      });
      setTimeout(() => updateState({ isVisible: true }), 100);
    }, animationConfig.fadeInDuration * 1000);
    trackEvent(EVENT_TYPES.RESET_SEARCH, {
      category: 'User Action',
      action: 'Restart Search',
      label: 'User initiated new search'
    });
  };

  const { searchResults, totalCount, isFormDisabled, isLoading, isVisible, showContent, resetForm, medicineOptions, districtOptions, error, isSearching } = state;

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
          {isLoading ? (
            <LoadingWrapper>
              <CircularProgress size={24} />
              <LoadingText variant="body1">
                🤖 Iniciando Inteligencia Artificial...
              </LoadingText>
            </LoadingWrapper>
          ) : (
            <SearchForm 
              onSearch={handleSearch} 
              disabled={isFormDisabled}
              reset={resetForm}
              medicineOptions={medicineOptions}
              districtOptions={districtOptions}
            />
          )}
          {showContent && (
            <>
              <StyledDivider />
              {isSearching ? (
                <LoadingWrapper>
                  <CircularProgress size={24} />
                  <LoadingText variant="body1">
                    Déjame buscar la información que necesitas...
                  </LoadingText>
                </LoadingWrapper>
              ) : (
                <ChatResponse
                  results={searchResults || []}
                  totalCount={totalCount}
                  onRestart={handleRestart}
                />
              )}
            </>
          )}
        </ContentWrapper>
      </FadeWrapper>
    </StyledContainer>
  );
};

export default HomePage;