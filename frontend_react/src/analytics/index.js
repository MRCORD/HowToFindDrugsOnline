import { initGA, pageview as ga4PageView, event as ga4Event } from '../utils/ga4';
import { initPostHog, identifyUser, resetUser } from '../utils/posthog';
import { trackEvent as posthogTrackEvent, trackPageView as posthogTrackPageView, EVENT_TYPES } from './events';
import { isFeatureEnabled, getFeatureFlagPayload, FEATURE_FLAGS } from './featureFlags';
import { setGroup, GROUP_TYPES } from './groups';

export const initAnalytics = () => {
  initGA();
  initPostHog();
};

export const trackPageView = (path) => {
  ga4PageView(path);
  posthogTrackPageView(path);
};

export const trackEvent = (eventName, properties) => {
  const { category, action, label, value } = properties;
  
  // Google Analytics
  const ga4Category = category || 'User Interaction';
  const ga4Action = action || eventName.split(':').pop();
  ga4Event(ga4Category, ga4Action, label, value);

  // PostHog
  posthogTrackEvent(eventName, properties);
};

export const setAnalyticsGroup = (groupType, groupKey, groupProperties = {}) => {
  setGroup(groupType, groupKey, groupProperties);
};

export const getFeatureFlagValue = getFeatureFlagPayload;

export {
  identifyUser,
  resetUser,
  isFeatureEnabled,
  EVENT_TYPES,
  GROUP_TYPES,
  FEATURE_FLAGS
};