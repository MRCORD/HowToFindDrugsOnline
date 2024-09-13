import { useCallback } from 'react';
import {
  trackEvent,
  trackPageView,
  identifyUser,
  resetUser,
  setGroup,
  isFeatureEnabled,
  getFeatureFlagPayload,
  EVENT_TYPES,
  GROUP_TYPES,
  FEATURE_FLAGS
} from '../analytics';

export const useAnalytics = () => {
  return {
    trackPageView: useCallback(trackPageView, []),
    trackEvent: useCallback(trackEvent, []),
    identifyUser: useCallback(identifyUser, []),
    resetUser: useCallback(resetUser, []),
    isFeatureEnabled: useCallback(isFeatureEnabled, []),
    getFeatureFlagPayload: useCallback(getFeatureFlagPayload, []),
    setGroup: useCallback(setGroup, []),
    EVENT_TYPES,
    GROUP_TYPES,
    FEATURE_FLAGS
  };
};