import { Container, Divider, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

export const StyledContainer = styled(Container)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '100vh',
  padding: theme.spacing(4),
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
  color: theme.palette.text.primary,
}));

export const Subtitle = styled(Typography)(({ theme }) => ({
  fontSize: '1rem',
  marginBottom: theme.spacing(4),
  maxWidth: '600px',
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

export const StyledDivider = styled(Divider)(({ theme }) => ({
  width: '100%',
  margin: theme.spacing(1, 0),
  backgroundColor: theme.palette.background.default,
  border: theme.palette.background.default,
}));

export const FadeWrapper = styled('div')(({ theme }) => ({
  opacity: 0,
  transition: `opacity ${theme.transitions.duration.standard}ms ${theme.transitions.easing.easeInOut}`,
  '&.visible': {
    opacity: 1,
  },
}));

export const ErrorMessage = styled('div')(({ theme }) => ({
  color: theme.palette.error.main,
  marginBottom: theme.spacing(2),
}));

export const LoadingWrapper = styled('div')(({ theme }) => ({
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'flex-start',
  width: '100%',
  padding: theme.spacing(2),
}));

export const LoadingText = styled(Typography)(({ theme }) => ({
  marginLeft: theme.spacing(2),
}));