import React from 'react';
import { Paper, Typography, Box, Avatar, styled } from '@mui/material';
import { SmartToy } from '@mui/icons-material';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginTop: theme.spacing(2),
  backgroundColor: '#1e2130',
  borderRadius: theme.spacing(1),
  width: '100%',
  maxWidth: '600px',
}));

const StyledAvatar = styled(Avatar)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  marginRight: theme.spacing(2),
}));

const ResultItem = styled(Box)(({ theme }) => ({
  marginTop: theme.spacing(2),
  padding: theme.spacing(1),
  borderRadius: theme.spacing(1),
  backgroundColor: '#2a2d3e',
}));

const ChatResponse = ({ results }) => {
  return (
    <StyledPaper elevation={3}>
      <Box display="flex" alignItems="flex-start">
        <StyledAvatar>
          <SmartToy />
        </StyledAvatar>
        <Box flexGrow={1}>
          <Typography variant="body1" gutterBottom>
            He encontrado {results.length} resultados para tu búsqueda. Aquí están las opciones más económicas:
          </Typography>
          {results.map((result, index) => (
            <ResultItem key={index}>
              <Typography variant="subtitle1" gutterBottom>
                {result.nombreProducto} - S/. {result.precio.toFixed(2)}
              </Typography>
              <Typography variant="body2">
                {result.farmacia}
              </Typography>
              <Typography variant="body2">
                {result.direccion}
              </Typography>
            </ResultItem>
          ))}
        </Box>
      </Box>
    </StyledPaper>
  );
};

export default ChatResponse;