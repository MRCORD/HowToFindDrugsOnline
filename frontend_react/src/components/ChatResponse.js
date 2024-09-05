import React, { useState, useEffect } from 'react';
import { Typography, Box, ListItemIcon, Link, Fade, Paper } from '@mui/material';
import { LocalPharmacy, LocationOn } from '@mui/icons-material';
import { MessageBubble, StyledAvatar, LoadingBubble, StyledCircularProgress, ResponseWrapper } from '../styles/globalStyles';
import { animationConfig } from '../config/animationConfig';
import { styled } from '@mui/material/styles';
import { TypeAnimation } from 'react-type-animation';

const ResultItem = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(1.5),
  marginTop: theme.spacing(2),
  backgroundColor: theme.palette.background.paper,
  borderRadius: theme.spacing(2),
  transition: 'transform 0.2s, box-shadow 0.2s',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
  },
}));

const ChatResponse = ({ results, isLoading }) => {
  const [showLoadingMessage, setShowLoadingMessage] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [typewriterComplete, setTypewriterComplete] = useState(false);
  const [visibleResults, setVisibleResults] = useState([]);

  useEffect(() => {
    if (isLoading) {
      setShowLoadingMessage(true);
      setShowResults(false);
      setTypewriterComplete(false);
      setVisibleResults([]);
    } else if (results.length > 0) {
      setShowLoadingMessage(false);
      setShowResults(true);
    }
  }, [isLoading, results]);

  useEffect(() => {
    if (typewriterComplete && results.length > 0) {
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
  }, [typewriterComplete, results]);

  const introText = `Hay ${results.length} resultados en total.\nAquí están las opciones más económicas:`;

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
                    () => setTypewriterComplete(true)
                  ]}
                  wrapper="div"
                  cursor={true}
                  speed={animationConfig.typewriterSpeed}
                  style={{ whiteSpace: 'pre-line', marginBottom: '16px' }}
                />
                {visibleResults.map((result, index) => (
                  <Fade key={index} in={true} timeout={500}>
                    <ResultItem elevation={1}>
                      <Box display="flex" alignItems="flex-start">
                        <ListItemIcon style={{ minWidth: 'auto', marginRight: '8px', marginTop: '4px' }}>
                          <LocalPharmacy color="primary" fontSize="small" />
                        </ListItemIcon>
                        <Box flexGrow={1}>
                          <Typography variant="body2" component="div">
                            <strong>{result.nombreProducto}</strong>
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            Precio: S/. {result.precio.toFixed(2)}
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            {result.farmacia}
                          </Typography>
                          <Link 
                            href="#" 
                            color="secondary" 
                            sx={{ 
                              display: 'flex', 
                              alignItems: 'center', 
                              mt: 0.5,
                              fontSize: '0.875rem'
                            }}
                          >
                            <LocationOn sx={{ mr: 0.5 }} fontSize="small" />
                            {result.direccion}
                          </Link>
                        </Box>
                      </Box>
                    </ResultItem>
                  </Fade>
                ))}
              </Box>
            </Box>
          </MessageBubble>
        </Fade>
      )}
    </ResponseWrapper>
  );
};

export default ChatResponse;