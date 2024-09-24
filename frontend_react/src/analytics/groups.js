import { setGroup as posthogSetGroup } from '../utils/posthog';

export const GROUP_TYPES = {
  DISTRICT: 'district',
};

export const setGroup = (groupType, groupKey, groupProperties = {}) => {
  if (!Object.values(GROUP_TYPES).includes(groupType)) {
    console.warn(`Invalid group type: ${groupType}`);
    return;
  }
  posthogSetGroup(groupType, groupKey, groupProperties);
};