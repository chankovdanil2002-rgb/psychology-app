import api from './axios';

/**
 * Get all available specializations.
 */
export function getSpecializations() {
  return api.get('/specializations/');
}

/**
 * Get details of a specific specialization by slug.
 * @param {string} slug
 */
export function getSpecializationBySlug(slug) {
  return api.get(`/specializations/${slug}/`);
}
