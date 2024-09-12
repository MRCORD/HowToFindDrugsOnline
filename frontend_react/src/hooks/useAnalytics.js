import { useCallback } from 'react';
import { 
  trackPageView, 
  trackEvent, 
  identifyUser,
  resetUser,
  isFeatureEnabled,
  getFeatureFlagValue,
  setAnalyticsGroup,
  GROUP_TYPES,
  EVENT_TYPES,
  FEATURE_FLAGS
} from '../utils/analytics';

export const useAnalytics = () => {
  return {
    trackPageView: useCallback(trackPageView, []),
    trackEvent: useCallback(trackEvent, []),
    identifyUser: useCallback(identifyUser, []),
    resetUser: useCallback(resetUser, []),
    isFeatureEnabled: useCallback(isFeatureEnabled, []),
    getFeatureFlagValue: useCallback(getFeatureFlagValue, []),
    setAnalyticsGroup: useCallback(setAnalyticsGroup, []),
    GROUP_TYPES,
    EVENT_TYPES,
    FEATURE_FLAGS
  };
};