import { styled } from '@mui/material/styles';
import { Paper, TextField, Button, Autocomplete } from '@mui/material';

export const FormWrapper = styled('div')({
  width: '100%',
  display: 'flex',
  justifyContent: 'center',
});

export const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  backgroundColor: theme.palette.background.paper,
  borderRadius: theme.shape.borderRadius,
  width: '100%',
  maxWidth: '600px',
}));

export const StyledAutocomplete = styled(Autocomplete)(({ theme }) => ({
  marginBottom: theme.spacing(2), // Add more vertical space between components
  '& .MuiTextField-root': {
    '& .MuiOutlinedInput-root': {
      '& fieldset': {
        borderColor: theme.palette.divider,
      },
      '&:hover fieldset': {
        borderColor: theme.palette.primary.main,
      },
      '&.Mui-focused fieldset': {
        borderColor: theme.palette.primary.main,
      },
    },
    '& .MuiInputLabel-root': {
      color: theme.palette.text.secondary,
      '&.Mui-focused': {
        color: theme.palette.primary.main,
      },
    },
    '& .MuiSelect-icon': {
      color: theme.palette.text.secondary,
    },
  },
}));

export const StyledButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(0.5),
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.primary.contrastText,
  '&:hover': {
    backgroundColor: theme.palette.primary.dark,
  },
}));