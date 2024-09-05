import React, { useEffect, useState } from 'react';
import ChatResponse from '../../components/ChatResponse';
import SearchForm from '../../components/SearchForm';
import { animationConfig } from '../../config/animationConfig';
import { fetchDistrictOptions, fetchMedicineOptions, searchDrugs } from '../../services/api';
import {
  ContentWrapper,
  FadeWrapper,
  StyledContainer,
  StyledDivider,
  Subtitle,
  Title
} from './HomePage.styles';

const HomePage = () => {
  const [state, setState] = useState({
    searchResults: null,
    isFormDisabled: false,
    isLoading: false,
    isVisible: false,
    showContent: true,
    resetForm: false,
    medicineOptions: null,
    districtOptions: null,
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
          medicineOptions: medicines.drugs,
          districtOptions: districts.districts,
        });
      } catch (error) {
        console.error('Error loading options:', error);
      }
    };

    loadOptions();
    setTimeout(() => updateState({ isVisible: true }), 100);
  }, []);

  const handleSearch = async (selectedDrug, selectedDistrict) => {
    updateState({ isFormDisabled: true, isLoading: true, searchResults: null, resetForm: false });
    try {
      const results = await searchDrugs(selectedDrug, selectedDistrict);
      updateState({ searchResults: results.drugs, isLoading: false });
    } catch (error) {
      console.error('Error searching drugs:', error);
      updateState({ isLoading: false });
    }
  };

  const handleRestart = () => {
    updateState({ isVisible: false });
    setTimeout(() => {
      updateState({
        searchResults: null,
        isFormDisabled: false,
        isLoading: false,
        showContent: false,
        resetForm: true
      });
      setTimeout(() => updateState({ isVisible: true, showContent: true }), 100);
    }, animationConfig.fadeInDuration * 1000);
  };

  const { searchResults, isFormDisabled, isLoading, isVisible, showContent, resetForm, medicineOptions, districtOptions } = state;

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