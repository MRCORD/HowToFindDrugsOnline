import posthog from 'posthog-js';

export const FEATURE_FLAGS = {
  NEW_SEARCH_ALGORITHM: 'new-search-algorithm',
  BETA_FEATURES: 'beta-features',
};

export const isFeatureEnabled = (flagKey, defaultValue = false) => {
  return posthog.isFeatureEnabled(flagKey) ?? defaultValue;
};

export const getFeatureFlagPayload = (flagKey) => {
  return posthog.getFeatureFlagPayload(flagKey);
};