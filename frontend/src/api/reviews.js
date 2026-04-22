import api from './axios';

/**
 * Create a review for a completed appointment (client only).
 * @param {Object} data - { appointment, rating, text }
 */
export function createReview(data) {
  return api.post('/reviews/', data);
}

/**
 * Get reviews, optionally filtered by psychologist.
 * @param {Object} params - { psychologist, page }
 */
export function getReviews(params = {}) {
  return api.get('/reviews/', { params });
}
