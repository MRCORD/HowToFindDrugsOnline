import React, { useState } from 'react';
import { TextField, Button, Paper, styled } from '@mui/material';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  backgroundColor: '#1e2130',
  borderRadius: theme.spacing(1),
  width: '100%',
  maxWidth: '600px',
}));

const StyledTextField = styled(TextField)(({ theme }) => ({
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

const StyledButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(2),
  backgroundColor: '#4a5568',
  '&:hover': {
    backgroundColor: '#718096',
  },
}));

const SearchForm = ({ onSearch, disabled }) => {
  const [selectedDrug, setSelectedDrug] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(selectedDrug, selectedDistrict);
  };

  return (
    <StyledPaper component="form" onSubmit={handleSubmit} elevation={3}>
      <StyledTextField
        select
        fullWidth
        label="Medicina"
        value={selectedDrug}
        onChange={(e) => setSelectedDrug(e.target.value)}
        disabled={disabled}
        SelectProps={{
          native: true,
        }}
        InputLabelProps={{
          shrink: true,
        }}
      >
        <option value="">Selecciona la medicina...</option>
        <option value="AMLODIPINO 10 mg [Comprimido]">AMLODIPINO 10 mg [Comprimido]</option>
        <option value="PARACETAMOL 500 mg [Tableta]">PARACETAMOL 500 mg [Tableta]</option>
      </StyledTextField>
      <StyledTextField
        select
        fullWidth
        label="Distrito"
        value={selectedDistrict}
        onChange={(e) => setSelectedDistrict(e.target.value)}
        disabled={disabled}
        SelectProps={{
          native: true,
        }}
        InputLabelProps={{
          shrink: true,
        }}
      >
        <option value="">Selecciona el distrito...</option>
        <option value="BREÑA">BREÑA</option>
        <option value="MIRAFLORES">MIRAFLORES</option>
      </StyledTextField>
      <StyledButton
        type="submit"
        variant="contained"
        fullWidth
        disabled={disabled || !selectedDrug || !selectedDistrict}
      >
        Consultar
      </StyledButton>
    </StyledPaper>
  );
};

export default SearchForm;