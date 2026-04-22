import api from './axios';

/**
 * Get available time slots for a psychologist on a given date.
 * @param {Object} params - { psychologist, date }
 */
export function getSlots(params = {}) {
  return api.get('/schedule/slots/', { params });
}

/**
 * Create a single time slot (psychologist only).
 * @param {Object} data - { date, start_time, end_time }
 */
export function createSlot(data) {
  return api.post('/schedule/slots/', data);
}

/**
 * Bulk-create time slots (psychologist only).
 * @param {Object} data - { date, slots: [{ start_time, end_time }, ...] }
 */
export function createBulkSlots(data) {
  return api.post('/schedule/slots/bulk/', data);
}

/**
 * Delete a time slot (psychologist only, if no appointment linked).
 * @param {number|string} id
 */
export function deleteSlot(id) {
  return api.delete(`/schedule/slots/${id}/`);
}
