import React, { useEffect, useState } from 'react';
import { useAnalytics } from '../hooks/useAnalytics';
import {
  FormWrapper,
  StyledButton,
  StyledPaper,
  StyledTextField
} from './SearchForm.styles';

const SearchForm = ({ onSearch, disabled, reset, medicineOptions, districtOptions }) => {
  const { trackEvent, trackFormInteraction } = useAnalytics();
  const [selectedDrug, setSelectedDrug] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('');

  useEffect(() => {
    if (reset) {
      setSelectedDrug('');
      setSelectedDistrict('');
    }
  }, [reset]);

  useEffect(() => {
    console.log('Medicine options in SearchForm:', medicineOptions);
    console.log('District options in SearchForm:', districtOptions);
  }, [medicineOptions, districtOptions]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(selectedDrug, selectedDistrict);
    trackEvent('Form Submission', 'Search Form', `${selectedDrug} in ${selectedDistrict}`);
  };

  const handleDrugChange = (e) => {
    const newDrug = e.target.value;
    setSelectedDrug(newDrug);
    if (newDrug) {
      trackFormInteraction('Select Drug', newDrug);
    }
  };

  const handleDistrictChange = (e) => {
    const newDistrict = e.target.value;
    setSelectedDistrict(newDistrict);
    if (newDistrict) {
      trackFormInteraction('Select District', newDistrict);
    }
  };

  return (
    <FormWrapper>
      <StyledPaper component="form" onSubmit={handleSubmit} elevation={3}>
        <StyledTextField
          select
          fullWidth
          label="Medicina"
          value={selectedDrug}
          onChange={handleDrugChange}
          disabled={disabled || !medicineOptions}
          SelectProps={{
            native: true,
          }}
          InputLabelProps={{
            shrink: true,
          }}
        >
          <option value="">Selecciona la medicina...</option>
          {medicineOptions && medicineOptions.map((drug) => (
            <option key={drug.dropdown} value={drug.dropdown}>{drug.dropdown}</option>
          ))}
        </StyledTextField>
        <StyledTextField
          select
          fullWidth
          label="Distrito"
          value={selectedDistrict}
          onChange={handleDistrictChange}
          disabled={disabled || !districtOptions}
          SelectProps={{
            native: true,
          }}
          InputLabelProps={{
            shrink: true,
          }}
        >
          <option value="">Selecciona el distrito...</option>
          {districtOptions && districtOptions.map((district) => (
            <option key={district.descripcion} value={district.descripcion}>{district.descripcion}</option>
          ))}
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