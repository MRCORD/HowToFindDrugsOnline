import ReactGA from 'react-ga4';

export const initGA = () => {
  const GOOGLE_ANALYTICS_ID = process.env.REACT_APP_GOOGLE_ANALYTICS_ID;
  if (GOOGLE_ANALYTICS_ID) {
    ReactGA.initialize(GOOGLE_ANALYTICS_ID);
  } else {
    console.warn('Google Analytics ID not found in environment variables');
  }
};

export const pageview = (path) => {
  ReactGA.send({ hitType: "pageview", page: path });
};

export const event = (category, action, label, value) => {
  ReactGA.event({ category, action, label, value });
};

export default ReactGA;