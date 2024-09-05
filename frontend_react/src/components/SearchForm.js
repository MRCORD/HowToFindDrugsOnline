// src/components/SearchForm/SearchForm.js

import React, { useState, useEffect } from 'react';
// import { Typography } from '@mui/material';
import {
  FormWrapper,
  StyledPaper,
  StyledTextField,
  StyledButton
} from './SearchForm.styles';

const SearchForm = ({ onSearch, disabled, reset }) => {
  const [selectedDrug, setSelectedDrug] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('');

  useEffect(() => {
    if (reset) {
      setSelectedDrug('');
      setSelectedDistrict('');
    }
  }, [reset]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(selectedDrug, selectedDistrict);
  };

  return (
    <FormWrapper>
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
    </FormWrapper>
  );
};

export default SearchForm;