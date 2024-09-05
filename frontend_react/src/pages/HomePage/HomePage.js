import { Fade } from '@mui/material';
import React, { useState } from 'react';
import ChatResponse from '../../components/ChatResponse';
import SearchForm from '../../components/SearchForm';
import { animationConfig } from '../../config/animationConfig';
import { searchDrugs } from '../../services/searchService';
import {
  ContentWrapper,
  StyledContainer,
  StyledDivider,
  Subtitle,
  Title
} from './HomePage.styles';

const HomePage = () => {
  const [searchResults, setSearchResults] = useState(null);
  const [isFormDisabled, setIsFormDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (drug, district) => {
    setIsFormDisabled(true);
    setIsLoading(true);
    setSearchResults(null);
    try {
      const results = await searchDrugs(drug, district);
      setSearchResults(results);
    } catch (error) {
      console.error('Error searching drugs:', error);
      // Here you might want to set an error state and display it to the user
    } finally {
      setIsLoading(false);
      // We're not re-enabling the form here
    }
  };

  return (
    <StyledContainer maxWidth="md">
      <Fade in={true} timeout={animationConfig.fadeInDuration * 1000}>
        <ContentWrapper>
          <Title variant="h1">
            Busca tu Pepa 💊
          </Title>
          <Subtitle variant="body1">
            ¡Hola! Soy tu asistente virtual de búsqueda de medicinas en Lima. Estoy aquí para ayudarte a encontrar las medicinas que necesitas. ¿En qué puedo ayudarte hoy?
          </Subtitle>
          <SearchForm onSearch={handleSearch} disabled={isFormDisabled} />
        </ContentWrapper>
      </Fade>
      {(isLoading || searchResults) && (
        <>
          <StyledDivider />
          <ChatResponse results={searchResults || []} isLoading={isLoading} />
        </>
      )}
    </StyledContainer>
  );
};

export default HomePage;