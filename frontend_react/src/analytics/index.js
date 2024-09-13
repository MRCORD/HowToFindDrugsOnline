import posthog from 'posthog-js';
import { trackEvent, trackPageView, EVENT_TYPES } from './events';
import { setGroup, GROUP_TYPES } from './groups';
import { isFeatureEnabled, getFeatureFlagPayload, FEATURE_FLAGS } from './featureFlags';

export const initAnalytics = () => {
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

export const identifyUser = (userId, traits = {}) => {
  posthog.identify(userId, traits);
};

export const resetUser = () => {
  posthog.reset();
};

export {
  trackEvent,
  trackPageView,
  EVENT_TYPES,
  setGroup,
  GROUP_TYPES,
  isFeatureEnabled,
  getFeatureFlagPayload,
  FEATURE_FLAGS
};