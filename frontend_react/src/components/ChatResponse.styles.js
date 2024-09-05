import { styled } from '@mui/material/styles';
import { Paper, Avatar, CircularProgress, Button } from '@mui/material';

export const MessageBubble = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  backgroundColor: theme.palette.background.default,
  borderRadius: theme.shape.borderRadius,
  width: '100%',
  border: `1px solid ${theme.palette.background.default}`,
}));

export const StyledAvatar = styled(Avatar)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  marginRight: theme.spacing(2),
}));

export const LoadingBubble = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  backgroundColor: theme.palette.background.default,
  borderRadius: theme.shape.borderRadius,
  width: '100%',
  display: 'flex',
  alignItems: 'center',
  border: `1px solid ${theme.palette.background.default}`,
}));

export const StyledCircularProgress = styled(CircularProgress)(({ theme }) => ({
  marginRight: theme.spacing(2),
}));

export const ResponseWrapper = styled('div')(({ theme }) => ({
  width: '100%',
  maxWidth: '600px',
  marginTop: theme.spacing(4),
}));

export const ResultItem = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginTop: theme.spacing(2),
  backgroundColor: theme.palette.background.default,
  borderRadius: theme.shape.borderRadius,
  transition: 'transform 0.2s, box-shadow 0.2s',
  border: `1px solid ${theme.palette.divider}`,
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
  },
}));

export const RestartButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(2),
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.primary.contrastText,
  '&:hover': {
    backgroundColor: theme.palette.primary.dark,
  },
}));