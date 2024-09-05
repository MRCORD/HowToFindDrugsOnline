import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    background: {
      default: '#0E1117',
      paper: '#13151a', // Changed this to match the default background
    },
  },
});

export default theme;