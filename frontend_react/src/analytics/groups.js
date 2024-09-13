import posthog from 'posthog-js';

export const GROUP_TYPES = {
  DISTRICT: 'district',
};

export const setGroup = (groupType, groupKey, groupProperties = {}) => {
  posthog.group(groupType, groupKey, groupProperties);
};