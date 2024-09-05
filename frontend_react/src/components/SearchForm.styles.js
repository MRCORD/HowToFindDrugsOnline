import { styled } from '@mui/material/styles';
import { Paper, TextField, Button } from '@mui/material';

export const FormWrapper = styled('div')({
  width: '100%',
  display: 'flex',
  justifyContent: 'center',
});

export const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  backgroundColor: '#1e2130',
  borderRadius: theme.spacing(1),
  width: '100%',
  maxWidth: '600px',
}));

export const StyledTextField = styled(TextField)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      borderColor: '#4a5568',
    },
    '&:hover fieldset': {
      borderColor: '#718096',
    },
    '&.Mui-focused fieldset': {
      borderColor: '#90caf9',
    },
  },
  '& .MuiInputLabel-root': {
    color: '#a0aec0',
    '&.Mui-focused': {
      color: '#90caf9',
    },
  },
  '& .MuiSelect-icon': {
    color: '#a0aec0',
  },
}));

export const StyledButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(2),
  backgroundColor: '#4a5568',
  '&:hover': {
    backgroundColor: '#718096',
  },
}));