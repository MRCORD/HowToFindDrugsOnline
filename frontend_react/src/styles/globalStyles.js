// import { styled, keyframes } from '@mui/material/styles';
// import { Paper, Avatar, CircularProgress } from '@mui/material';

// export const MessageBubble = styled(Paper)(({ theme }) => ({
//   padding: theme.spacing(1.5), // Reduced padding
//   marginBottom: theme.spacing(1.5), // Reduced margin
//   backgroundColor: theme.palette.background.default,
//   borderRadius: theme.spacing(2),
//   width: '100%',
//   // maxWidth: '600px', // Reduced max-width
//   display: 'flex',
//   alignItems: 'flex-start',
//   border: `1px solid ${theme.palette.background.default}`,
// }));


import { styled, keyframes } from '@mui/material/styles';
import { Paper, Avatar, CircularProgress } from '@mui/material';

export const MessageBubble = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  backgroundColor: theme.palette.background.default,
  borderRadius: theme.spacing(3), // Increased border radius
  width: '100%',
  border: `1px solid ${theme.palette.background.default}`,
}));

export const StyledAvatar = styled(Avatar)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  marginRight: theme.spacing(1), // Reduced margin
  width: theme.spacing(4), // Smaller avatar
  height: theme.spacing(4), // Smaller avatar
}));

export const ResponseBubble = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(1.5), // Reduced padding
  marginBottom: theme.spacing(1.5), // Reduced margin
  backgroundColor: theme.palette.background.default,
  borderRadius: theme.spacing(2),
  width: '100%',
  // maxWidth: '450px', // Reduced max-width
  border: `1px solid ${theme.palette.divider}`,
}));

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

export const LoadingBubble = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  backgroundColor: theme.palette.background.default,
  borderRadius: theme.spacing(2),
  width: '100%',
  maxWidth: '500px', // Reduced from 600px
  display: 'flex',
  alignItems: 'center',
  border: `1px solid ${theme.palette.background.default}`,
}));

export const StyledCircularProgress = styled(CircularProgress)(({ theme }) => ({
  marginRight: theme.spacing(2),
  animation: `${spin} 1s linear infinite`,
}));

export const ResponseWrapper = styled('div')(({ theme }) => ({
  width: '100%',
  maxWidth: '600px', // This should match the maxWidth of your form wrapper
}));