// src/pages/HomePage/HomePage.js

import React, { useState, useEffect } from 'react';
import SearchForm from '../../components/SearchForm';
import ChatResponse from '../../components/ChatResponse';
import { 
  StyledContainer, 
  ContentWrapper, 
  Title, 
  Subtitle, 
  StyledDivider
} from './HomePage.styles';
import { animationConfig } from '../../config/animationConfig';
import { searchDrugs } from '../../services/searchService';
import { styled } from '@mui/material/styles';

const FadeWrapper = styled('div')(({ theme }) => ({
  opacity: 0,
  transition: `opacity ${animationConfig.fadeInDuration}s ease-in-out`,
  '&.visible': {
    opacity: 1,
  },
}));

const HomePage = () => {
  const [state, setState] = useState({
    searchResults: null,
    isFormDisabled: false,
    isLoading: false,
    isVisible: false,
    showContent: true
  });

  const updateState = (newState) => {
    setState(prevState => ({ ...prevState, ...newState }));
  };

  useEffect(() => {
    // Trigger initial fade-in
    setTimeout(() => updateState({ isVisible: true }), 100);
  }, []);

  const handleSearch = async (drug, district) => {
    updateState({ isFormDisabled: true, isLoading: true, searchResults: null });
    try {
      const results = await searchDrugs(drug, district);
      updateState({ searchResults: results, isLoading: false });
    } catch (error) {
      console.error('Error searching drugs:', error);
      updateState({ isLoading: false });
    }
  };

  const handleRestart = () => {
    // Fade out
    updateState({ isVisible: false });

    // Wait for fade-out, then reset
    setTimeout(() => {
      updateState({
        searchResults: null,
        isFormDisabled: false,
        isLoading: false,
        showContent: false
      });

      // Trigger fade-in after a brief delay
      setTimeout(() => updateState({ isVisible: true, showContent: true }), 100);
    }, animationConfig.fadeInDuration * 1000);
  };

  const { searchResults, isFormDisabled, isLoading, isVisible, showContent } = state;

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
          <SearchForm onSearch={handleSearch} disabled={isFormDisabled} />
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