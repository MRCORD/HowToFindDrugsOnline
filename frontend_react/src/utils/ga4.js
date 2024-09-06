import ReactGA from 'react-ga4';

// Initialize GA with the ID from environment variable
export const initGA = () => {
    const GOOGLE_ANALYTICS_ID = process.env.REACT_APP_GOOGLE_ANALYTICS_ID;
    if (GOOGLE_ANALYTICS_ID) {
      ReactGA.initialize(GOOGLE_ANALYTICS_ID);
      console.log('Google Analytics initialized');
    } else {
      console.warn('Google Analytics ID not found in environment variables');
    }
  };

// Log pageviews
export const pageview = (path) => {
  ReactGA.send({ hitType: "pageview", page: path });
  console.log(`Pageview logged: ${path}`);
};

// Log events
export const event = (category, action, label, value) => {
  ReactGA.event({ category, action, label, value });
  console.log(`Event logged - Category: ${category}, Action: ${action}, Label: ${label}, Value: ${value}`);
};

// Log search events
export const logSearch = (searchTerm, resultsCount) => {
  ReactGA.event({
    category: 'Search',
    action: 'Perform Search',
    label: searchTerm,
    value: resultsCount
  });
  console.log(`Search logged - Term: ${searchTerm}, Results: ${resultsCount}`);
};