import api from './axios';

/**
 * Get notifications for the current user.
 */
export function getNotifications() {
  return api.get('/notifications/');
}

/**
 * Mark a single notification as read.
 * @param {number|string} id
 */
export function markRead(id) {
  return api.patch(`/notifications/${id}/read/`);
}

/**
 * Mark all notifications as read.
 */
export function markAllRead() {
  return api.patch('/notifications/read-all/');
}
