import React, { useEffect } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import HomePage from './pages/HomePage/HomePage';
import theme from './styles/theme';
import EnvDisplay from './components/EnvDisplay';
import { initAnalytics, trackPageView } from './analytics';

function App() {
  useEffect(() => {
    initAnalytics();
    trackPageView('/home');
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