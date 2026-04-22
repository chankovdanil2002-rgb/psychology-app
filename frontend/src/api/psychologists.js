import api from './axios';

/**
 * Get a paginated list of psychologists with optional filters.
 * @param {Object} params - { specialization, search, ordering, page }
 */
export function getPsychologists(params = {}) {
  return api.get('/psychologists/', { params });
}

/**
 * Get detailed info about a specific psychologist.
 * @param {number|string} id
 */
export function getPsychologistById(id) {
  return api.get(`/psychologists/${id}/`);
}

/**
 * Get the psychologist team list for admin management.
 */
export function getAdminPsychologists() {
  return api.get('/admin/psychologists/');
}

/**
 * Create a psychologist account from the admin panel.
 * @param {Object} data
 */
export function createAdminPsychologist(data) {
  return api.post('/admin/psychologists/', data);
}
