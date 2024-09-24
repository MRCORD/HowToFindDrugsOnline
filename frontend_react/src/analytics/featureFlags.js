import { isFeatureEnabled, getFeatureFlagPayload } from '../utils/posthog';

export const FEATURE_FLAGS = {
  NEW_SEARCH_ALGORITHM: 'new-search-algorithm',
  BETA_FEATURES: 'beta-features',
};

export { isFeatureEnabled, getFeatureFlagPayload };