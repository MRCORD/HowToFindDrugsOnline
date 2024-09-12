import React, { useEffect, useState } from 'react';
import { TextField } from '@mui/material';
import { useAnalytics } from '../hooks/useAnalytics';
import {
  FormWrapper,
  StyledButton,
  StyledPaper,
  StyledAutocomplete
} from './SearchForm.styles';

const SearchForm = ({ onSearch, disabled, reset, medicineOptions, districtOptions }) => {
  const { trackEvent, EVENT_TYPES } = useAnalytics();
  const [selectedDrug, setSelectedDrug] = useState(null);
  const [selectedDistrict, setSelectedDistrict] = useState(null);

  useEffect(() => {
    if (reset) {
      setSelectedDrug(null);
      setSelectedDistrict(null);
    }
  }, [reset]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedDrug && selectedDistrict) {
      onSearch(selectedDrug, selectedDistrict);
      trackEvent(EVENT_TYPES.FORM_INTERACTION, {
        category: 'Form Submission',
        action: 'Submit Search',
        label: `${selectedDrug.dropdown} in ${selectedDistrict.descripcion}`
      });
    }
  };

  return (
    <FormWrapper>
      <StyledPaper component="form" onSubmit={handleSubmit} elevation={3}>
        <StyledAutocomplete
          options={medicineOptions || []}
          getOptionLabel={(option) => option.dropdown}
          value={selectedDrug}
          onChange={(event, newValue) => {
            setSelectedDrug(newValue);
            if (newValue) {
              trackEvent(EVENT_TYPES.FORM_INTERACTION, {
                category: 'Form Interaction',
                action: 'Select Drug',
                label: newValue.dropdown
              });
            }
          }}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Medicina"
              fullWidth
              disabled={disabled}
              InputLabelProps={{
                shrink: true,
              }}
            />
          )}
          disabled={disabled || !medicineOptions}
        />
        <StyledAutocomplete
          options={districtOptions || []}
          getOptionLabel={(option) => option.descripcion}
          value={selectedDistrict}
          onChange={(event, newValue) => {
            setSelectedDistrict(newValue);
            if (newValue) {
              trackEvent(EVENT_TYPES.FORM_INTERACTION, {
                category: 'Form Interaction',
                action: 'Select District',
                label: newValue.descripcion
              });
            }
          }}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Distrito"
              fullWidth
              disabled={disabled}
              InputLabelProps={{
                shrink: true,
              }}
            />
          )}
          disabled={disabled || !districtOptions}
        />
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