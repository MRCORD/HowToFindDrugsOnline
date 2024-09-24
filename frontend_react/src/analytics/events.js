import { captureEvent, capturePageView } from '../utils/posthog';

const EVENT_VERSION = 'v1';

export const EVENT_TYPES = {
  DRUG_SELECTED: `${EVENT_VERSION}:search_form:drug_select`,
  DISTRICT_SELECTED: `${EVENT_VERSION}:search_form:district_select`,
  SEARCH_SUBMITTED: `${EVENT_VERSION}:search_form:form_submit`,
  RESET_SEARCH: `${EVENT_VERSION}:search_form:reset_click`,
  LOCATION_CLICKED: `${EVENT_VERSION}:results:location_click`,
  ERROR: `${EVENT_VERSION}:app:error_occur`,
  RESULTS_DISPLAYED: `${EVENT_VERSION}:results:display`
};

export const trackEvent = (eventName, properties) => {
  captureEvent(eventName, properties);
};

export const trackPageView = (path) => {
  capturePageView(path);
};