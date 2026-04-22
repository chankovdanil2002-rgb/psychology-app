import api from './axios';

/**
 * Create a new appointment (client only).
 * @param {Object} data - { psychologist, time_slot, comment? }
 */
export function createAppointment(data) {
  return api.post('/appointments/', data);
}

/**
 * Get list of appointments for the current user (client or psychologist).
 */
export function getAppointments(params = {}) {
  return api.get('/appointments/', { params });
}

/**
 * Confirm a pending appointment (psychologist only).
 * @param {number|string} id
 */
export function confirmAppointment(id) {
  return api.patch(`/appointments/${id}/confirm/`);
}

/**
 * Reject a pending appointment (psychologist only).
 * @param {number|string} id
 */
export function rejectAppointment(id) {
  return api.patch(`/appointments/${id}/reject/`);
}

/**
 * Mark an appointment as completed (psychologist only).
 * @param {number|string} id
 */
export function completeAppointment(id) {
  return api.patch(`/appointments/${id}/complete/`);
}

/**
 * Cancel an appointment (client only, when pending or confirmed).
 * @param {number|string} id
 */
export function cancelAppointment(id) {
  return api.patch(`/appointments/${id}/cancel/`);
}
