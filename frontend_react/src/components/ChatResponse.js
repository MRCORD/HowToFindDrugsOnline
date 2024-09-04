import React from 'react';
import { Typography, Box, List, ListItem, ListItemText, ListItemIcon, Link, Paper, Avatar } from '@mui/material';
import { styled } from '@mui/system';
import { LocalPharmacy, LocationOn, SmartToy } from '@mui/icons-material';

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

const StyledListItem = styled(ListItem)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.background.paper,
  transition: 'transform 0.2s',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
  },
}));

const ChatResponse = ({ results }) => {
  return (
    <StyledPaper elevation={3}>
      <Box display="flex" alignItems="flex-start">
        <StyledAvatar>
          <SmartToy />
        </StyledAvatar>
        <Box flexGrow={1}>
          <Typography variant="h6" gutterBottom>
            Hay {results.length} resultados en total
          </Typography>
          <Typography variant="subtitle1" gutterBottom>
            Dejame mostrarte las opciones más económicas:
          </Typography>
          <List>
            {results.map((result, index) => (
              <StyledListItem key={index}>
                <ListItemIcon>
                  <LocalPharmacy color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary={`${result.nombreProducto} - Precio: S/. ${result.precio.toFixed(2)}`}
                  secondary={
                    <React.Fragment>
                      <Typography component="span" variant="body2" color="text.primary">
                        {result.farmacia}
                      </Typography>
                      <br />
                      <Link href="#" color="secondary" sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <LocationOn sx={{ mr: 0.5 }} fontSize="small" />
                        {result.direccion}
                      </Link>
                    </React.Fragment>
                  }
                />
              </StyledListItem>
            ))}
          </List>
        </Box>
      </Box>
    </StyledPaper>
  );
};

export default ChatResponse;