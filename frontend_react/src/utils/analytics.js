import { initGA, pageview as ga4PageView, event as ga4Event } from './ga4';
import { 
  initPostHog, 
  capturePageView as posthogPageView, 
  captureEvent as posthogEvent,
  identifyUser as posthogIdentifyUser,
  resetUser as posthogResetUser,
  getFeatureFlag,
  getFeatureFlagPayload,
  setGroup
} from './posthog';
import { GROUP_TYPES, EVENT_TYPES, FEATURE_FLAGS } from '../config/analyticsConfig';

export const initAnalytics = () => {
  initGA();
  initPostHog();
};

export const trackPageView = (path) => {
  ga4PageView(path);
  posthogPageView(path);
};

export const trackEvent = (eventName, properties) => {
  const { category, action, label, value } = properties;
  
  const ga4Category = category || 'Uncategorized';
  const ga4Action = action || eventName;
  
  ga4Event(ga4Category, ga4Action, label, value);
  posthogEvent(eventName, properties);
};

export const identifyUser = (userId, traits = {}) => {
  posthogIdentifyUser(userId, traits);
};

export const resetUser = () => {
  posthogResetUser();
};

export const isFeatureEnabled = (flagKey, defaultValue = false) => {
  return getFeatureFlag(flagKey, defaultValue);
};

export const getFeatureFlagValue = (flagKey) => {
  return getFeatureFlagPayload(flagKey);
};

export const setAnalyticsGroup = (groupType, groupKey, groupProperties = {}) => {
  setGroup(groupType, groupKey, groupProperties);
};

export { GROUP_TYPES, EVENT_TYPES, FEATURE_FLAGS };