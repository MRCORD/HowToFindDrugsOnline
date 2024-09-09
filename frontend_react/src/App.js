import React, { useEffect } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import HomePage from './pages/HomePage/HomePage';
import theme from './styles/theme';
import { initGA, pageview } from './utils/ga4';
import EnvDisplay from './components/EnvDisplay';

function App() {
  useEffect(() => {
    initGA();
    pageview('/home');
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <HomePage />
      {process.env.NODE_ENV !== 'production' && <EnvDisplay />}
    </ThemeProvider>
  );
}

export default App;