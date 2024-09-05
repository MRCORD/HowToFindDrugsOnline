import { styled } from '@mui/material/styles';
import { Container, Typography, Divider } from '@mui/material';

export const StyledContainer = styled(Container)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '100vh',
  padding: theme.spacing(2),
}));

export const ContentWrapper = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  width: '100%',
  maxWidth: '600px',
});

export const Title = styled(Typography)(({ theme }) => ({
  fontSize: '2.5rem',
  fontWeight: 'bold',
  marginBottom: theme.spacing(2),
  textAlign: 'center',
}));

export const Subtitle = styled(Typography)(({ theme }) => ({
  fontSize: '0.9rem',
  marginBottom: theme.spacing(4),
  maxWidth: '600px',
  textAlign: 'center',
}));

export const StyledDivider = styled(Divider)(({ theme }) => ({
  width: '100%',
  margin: theme.spacing(2, 0), // Reduced from 4 to 2
  border: `1px solid ${theme.palette.background.default}`,
}));

export const ResponseWrapper = styled('div')(({ theme }) => ({
  width: '100%',
  maxWidth: '600px',
  marginTop: theme.spacing(2), // Reduced from 4 to 2
}));