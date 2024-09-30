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
  const [isFormDisabled, setIsFormDisabled] = useState(disabled);

  useEffect(() => {
    if (reset) {
      setSelectedDrug(null);
      setSelectedDistrict(null);
      setIsFormDisabled(false);
    }
  }, [reset]);

  useEffect(() => {
    setIsFormDisabled(disabled);
  }, [disabled]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedDrug && selectedDistrict && !isFormDisabled) {
      setIsFormDisabled(true);
      onSearch(selectedDrug, selectedDistrict);
      trackEvent(EVENT_TYPES.SEARCH_SUBMITTED, {
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
            if (!isFormDisabled) {
              setSelectedDrug(newValue);
              if (newValue) {
                trackEvent(EVENT_TYPES.DRUG_SELECTED, {
                  category: 'Form Interaction',
                  action: 'Select Drug',
                  label: newValue.dropdown,
                  properties: {
                    drugName: newValue.searchTerm,
                    concentration: newValue.concent,
                    formType: newValue.nombreFormaFarmaceutica
                  }
                });
              }
            }
          }}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Medicina"
              fullWidth
              disabled={isFormDisabled}
              InputLabelProps={{
                shrink: true,
              }}
            />
          )}
          disabled={isFormDisabled}
        />
        <StyledAutocomplete
          options={districtOptions || []}
          getOptionLabel={(option) => option.descripcion}
          value={selectedDistrict}
          onChange={(event, newValue) => {
            if (!isFormDisabled) {
              setSelectedDistrict(newValue);
              if (newValue) {
                trackEvent(EVENT_TYPES.DISTRICT_SELECTED, {
                  category: 'Form Interaction',
                  action: 'Select District',
                  label: newValue.descripcion,
                  properties: {
                    districtName: newValue.descripcion
                  }
                });
              }
            }
          }}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Distrito"
              fullWidth
              disabled={isFormDisabled}
              InputLabelProps={{
                shrink: true,
              }}
            />
          )}
          disabled={isFormDisabled}
        />
        <StyledButton
          type="submit"
          variant="contained"
          fullWidth
          disabled={isFormDisabled || !selectedDrug || !selectedDistrict}
        >
          Consultar
        </StyledButton>
      </StyledPaper>
    </FormWrapper>
  );
};

export default SearchForm;