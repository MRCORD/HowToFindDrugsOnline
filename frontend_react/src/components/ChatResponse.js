import React, { useState, useEffect } from 'react';
import { Typography, Box, ListItemIcon, Link, Fade, Paper } from '@mui/material';
import { LocalPharmacy, LocationOn } from '@mui/icons-material';
import { MessageBubble, StyledAvatar, LoadingBubble, StyledCircularProgress, ResponseWrapper } from '../styles/globalStyles';
import { animationConfig } from '../config/animationConfig';
import { styled } from '@mui/material/styles';

const ResultItem = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(1.5),
  marginTop: theme.spacing(2),
  backgroundColor: theme.palette.background.paper,
  borderRadius: theme.spacing(2), // Increased border radius
  transition: 'transform 0.2s, box-shadow 0.2s',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
  },
}));

const ChatResponse = ({ results, isLoading }) => {
  const [showLoadingMessage, setShowLoadingMessage] = useState(false);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    if (isLoading) {
      setShowLoadingMessage(true);
      setShowResults(false);
    } else if (results.length > 0) {
      setShowLoadingMessage(false);
      setShowResults(true);
    }
  }, [isLoading, results]);

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
                <Typography variant="body2" gutterBottom>
                  Hay {results.length} resultados en total.
                  <br />
                  Aquí están las opciones más económicas:
                </Typography>
                {results.slice(0, 3).map((result, index) => (
                  <ResultItem key={index} elevation={1}>
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