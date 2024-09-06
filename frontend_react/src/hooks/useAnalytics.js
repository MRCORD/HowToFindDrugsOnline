// src/hooks/useAnalytics.js
import { useCallback } from 'react';
import { event, pageview } from '../services/ga4';

export const useAnalytics = () => {
  const trackPageView = useCallback((path) => {
    pageview(path);
  }, []);

  const trackEvent = useCallback((category, action, label, value) => {
    event(category, action, label, value);
  }, []);

  const trackSearch = useCallback((searchTerm, resultsCount) => {
    event('Search', 'Perform Search', searchTerm, resultsCount);
  }, []);

  const trackError = useCallback((errorType, errorMessage) => {
    event('Error', errorType, errorMessage);
  }, []);

  const trackFormInteraction = useCallback((interactionType, value) => {
    event('Form Interaction', interactionType, value);
  }, []);

  return {
    trackPageView,
    trackEvent,
    trackSearch,
    trackError,
    trackFormInteraction
  };
};