import React, { useEffect, useState } from 'react';
import { TypeAnimation } from 'react-type-animation';
import { animationConfig } from '../config/animationConfig';
import { useAnalytics } from '../hooks/useAnalytics';
import {
  LoadingBubble,
  MessageBubble,
  ResponseWrapper,
  RestartButton,
  ResultItem,
  StyledAvatar,
  StyledCircularProgress
} from './ChatResponse.styles';
import { Box, Fade, Link, Typography, useTheme } from '@mui/material';
import { LocationOn } from '@mui/icons-material';

const ChatResponse = ({ results, totalCount, isLoading, onRestart }) => {
  const theme = useTheme();
  const { trackEvent, EVENT_TYPES } = useAnalytics();
  const [showLoadingMessage, setShowLoadingMessage] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [typewriterComplete, setTypewriterComplete] = useState(false);
  const [visibleResults, setVisibleResults] = useState([]);
  const [showRestartMessage, setShowRestartMessage] = useState(false);
  const [restartTypewriterComplete, setRestartTypewriterComplete] = useState(false);

  // Handle loading state
  useEffect(() => {
    if (isLoading) {
      setShowLoadingMessage(true);
      setShowResults(false);
      setTypewriterComplete(false);
      setVisibleResults([]);
      setShowRestartMessage(false);
    } else {
      setShowLoadingMessage(false);
      setTimeout(() => setShowResults(true), animationConfig.chatBubbleAppear * 1000);
    }
  }, [isLoading]);

  // Handle results display
  useEffect(() => {
    if (showResults) {
      trackEvent(EVENT_TYPES.RESULTS_DISPLAYED, {
        category: 'Results',
        action: 'Display Results',
        label: 'Search Results Shown',
        value: results.length
      });
      if (totalCount > 0 && typewriterComplete) {
        const timer = setInterval(() => {
          setVisibleResults((prev) => {
            if (prev.length < results.length) {
              return [...prev, results[prev.length]];
            }
            clearInterval(timer);
            return prev;
          });
        }, animationConfig.resultItemDelay * 1000);
        return () => clearInterval(timer);
      }
    }
  }, [showResults, typewriterComplete, results, totalCount, trackEvent, EVENT_TYPES]);

  // Handle restart message display
  useEffect(() => {
    if (showResults && typewriterComplete) {
      if (totalCount === 0 || (visibleResults.length === results.length && results.length > 0)) {
        setTimeout(() => {
          setShowRestartMessage(true);
        }, animationConfig.showRestartMessageDelay * 1000);
      }
    }
  }, [showResults, typewriterComplete, visibleResults, results, totalCount]);

  const handleRestartClick = () => {
    trackEvent(EVENT_TYPES.RESET_SEARCH, {
      category: 'User Action',
      action: 'Restart Search',
      label: 'User clicked restart button'
    });
    onRestart();
  };

  const handleLocationClick = (result) => {
    trackEvent(EVENT_TYPES.LOCATION_CLICKED, {
      category: 'User Action',
      action: 'View Location',
      label: result.nombreComercial,
      properties: {
        drugName: result.nombreProducto,
        pharmacy: result.nombreComercial,
        address: result.direccion,
        price: result.precio2
      }
    });
  };

  const introText = totalCount === 0
    ? "Lo siento, no se han podido encontrar opciones en tu distrito para la medicina que buscas."
    : `Hay ${totalCount} resultados en total.\nAquí están las opciones más económicas:`;
  const restartText = "¿Deseas realizar otra consulta? Presiona el botón de abajo para realizar otra consulta ⬇️";

  return (
    <ResponseWrapper>
      <Fade in={showLoadingMessage} timeout={animationConfig.chatBubbleAppear * 1000}>
        <LoadingBubble elevation={0} style={{ display: showLoadingMessage ? 'flex' : 'none' }}>
          <StyledCircularProgress size={24} />
          <Typography variant="body2">
            Déjame buscar la información que necesitas...
          </Typography>
        </LoadingBubble>
      </Fade>

      {showResults && (
        <Fade in={showResults} timeout={animationConfig.chatBubbleAppear * 1000}>
          <MessageBubble elevation={0}>
            <Box display="flex">
              <StyledAvatar>🤖</StyledAvatar>
              <Box flexGrow={1} ml={2}>
                <TypeAnimation
                  sequence={[
                    introText,
                    () => setTypewriterComplete(true),
                    1
                  ]}
                  wrapper="div"
                  cursor={false}
                  speed={animationConfig.typewriterSpeed}
                  style={{ whiteSpace: 'pre-line', marginBottom: '16px', color: theme.palette.text.primary }}
                />
                {totalCount > 0 && visibleResults.map((result, index) => (
                  <Fade key={index} in={true} timeout={500}>
                    <ResultItem elevation={1}>
                      <Typography variant="body1" component="div" gutterBottom>
                        <strong>{result.nombreProducto}</strong>
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Precio: S/. {result.precio2 ? result.precio2.toFixed(2) : 'N/A'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {result.nombreComercial}
                      </Typography>
                      <Link
                        href={result.googleMapsUri}
                        target="_blank"
                        rel="noopener noreferrer"
                        color="secondary"
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          mt: 1,
                          fontSize: '0.875rem'
                        }}
                        onClick={() => handleLocationClick(result)}
                      >
                        <LocationOn sx={{ mr: 0.5 }} fontSize="small" />
                        {result.direccion}
                      </Link>
                    </ResultItem>
                  </Fade>
                ))}
              </Box>
            </Box>
          </MessageBubble>
        </Fade>
      )}

      {showRestartMessage && (
        <Fade in={showRestartMessage} timeout={animationConfig.restartAnimationDuration * 1000}>
          <MessageBubble elevation={0}>
            <Box display="flex">
              <StyledAvatar>🤖</StyledAvatar>
              <Box flexGrow={1} ml={2}>
                <TypeAnimation
                  sequence={[
                    restartText,
                    () => setRestartTypewriterComplete(true),
                    1
                  ]}
                  wrapper="div"
                  cursor={false}
                  speed={animationConfig.typewriterSpeed}
                  style={{ whiteSpace: 'pre-line', marginBottom: '16px' }}
                />
                {restartTypewriterComplete && (
                  <Fade 
                    in={restartTypewriterComplete} 
                    timeout={animationConfig.restartAnimationDuration * 1000}
                  >
                    <RestartButton
                      variant="contained"
                      fullWidth
                      onClick={handleRestartClick}
                      startIcon={<span role="img" aria-label="pill">💊</span>}
                      style={{ marginTop: `${animationConfig.restartButtonDelay}s` }}
                    >
                      Realizar otra consulta
                    </RestartButton>
                  </Fade>
                )}
              </Box>
            </Box>
          </MessageBubble>
        </Fade>
      )}
    </ResponseWrapper>
  );
};

export default ChatResponse;