import { createTheme } from '@mui/material/styles';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    background: {
      default: '#13151a',
      paper: '#1e2130',
    },
    primary: {
      main: '#90caf9',
    },
    text: {
      primary: '#ffffff',
      secondary: '#a0aec0',
    },
  },
});

export default darkTheme;