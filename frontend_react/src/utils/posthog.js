import posthog from 'posthog-js';

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

export const captureEvent = posthog.capture.bind(posthog);
export const capturePageView = (path) => posthog.capture('$pageview', { path });
export const identifyUser = posthog.identify.bind(posthog);
export const resetUser = posthog.reset.bind(posthog);
export const isFeatureEnabled = posthog.isFeatureEnabled.bind(posthog);
export const getFeatureFlagPayload = posthog.getFeatureFlagPayload.bind(posthog);
export const setGroup = posthog.group.bind(posthog);

export default posthog;