import posthog from 'posthog-js';
import { GROUP_TYPES } from '../config/analyticsConfig';

export const initPostHog = () => {
  posthog.init(process.env.REACT_APP_POSTHOG_API_KEY, {
    api_host: process.env.REACT_APP_POSTHOG_HOST || 'https://app.posthog.com',
    capture_pageview: false,
    autocapture: true,
    session_recording: {
      enabled: true,
      consent_cookie_name: 'posthog_session_recording_consent'
    }
  });
};

export const capturePageView = (path) => {
  posthog.capture('$pageview', { path });
};

export const captureEvent = (eventName, properties) => {
  posthog.capture(eventName, properties);
};

export const identifyUser = (userId, traits = {}) => {
  posthog.identify(userId, traits);
};

export const resetUser = () => {
  posthog.reset();
};

export const getFeatureFlag = (flagKey, defaultValue) => {
  return posthog.isFeatureEnabled(flagKey) ?? defaultValue;
};

export const getFeatureFlagPayload = (flagKey) => {
  return posthog.getFeatureFlagPayload(flagKey);
};

export const setGroup = (groupType, groupKey, groupProperties = {}) => {
  if (!Object.values(GROUP_TYPES).includes(groupType)) {
    console.warn(`Invalid group type: ${groupType}`);
    return;
  }
  posthog.group(groupType, groupKey, groupProperties);
};

export default posthog;