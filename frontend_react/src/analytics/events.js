import posthog from 'posthog-js';

export const EVENT_TYPES = {
  DRUG_SELECTED: 'Drug Selected',
  DISTRICT_SELECTED: 'District Selected',
  SEARCH_SUBMITTED: 'Search Submitted',
  RESET_SEARCH: 'Reset Search',
  LOCATION_CLICKED: 'Location Clicked',
  ERROR: 'Error'
};

export const trackEvent = (eventName, properties) => {
  posthog.capture(eventName, properties);
};

export const trackPageView = (path) => {
  posthog.capture('$pageview', { path });
};