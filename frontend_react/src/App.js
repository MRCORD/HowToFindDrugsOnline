import React, { useState } from 'react';
import { ThemeProvider, CssBaseline, Container, Typography, styled } from '@mui/material';
import darkTheme from './theme/darkTheme';
import SearchForm from './components/SearchForm';
import ChatResponse from './components/ChatResponse';

const StyledContainer = styled(Container)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '100vh',
  padding: theme.spacing(2),
}));

const Title = styled(Typography)(({ theme }) => ({
  fontSize: '2.5rem',
  fontWeight: 'bold',
  marginBottom: theme.spacing(2),
}));

const Subtitle = styled(Typography)(({ theme }) => ({
  fontSize: '0.9rem',
  marginBottom: theme.spacing(4),
  maxWidth: '600px',
  textAlign: 'center',
}));

function App() {
  const [searchResults, setSearchResults] = useState(null);
  const [isFormDisabled, setIsFormDisabled] = useState(false);

  const handleSearch = async (drug, district) => {
    setIsFormDisabled(true);
    // Simulating API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    const mockResults = [
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
    setSearchResults(mockResults);
    // Form remains disabled after search
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <StyledContainer maxWidth="md">
        <Title variant="h1">
          Busca tu Pepa 💊
        </Title>
        <Subtitle variant="body1">
          ¡Hola! Soy tu asistente virtual de búsqueda de medicinas en Lima. Estoy aquí para ayudarte a encontrar las medicinas que necesitas. ¿En qué puedo ayudarte hoy?
        </Subtitle>
        <SearchForm onSearch={handleSearch} disabled={isFormDisabled} />
        {searchResults && searchResults.length > 0 && (
          <ChatResponse results={searchResults} />
        )}
      </StyledContainer>
    </ThemeProvider>
  );
}

export default App;