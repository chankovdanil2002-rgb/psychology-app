import api from './axios';

/**
 * Создание отзыва к завершённой записи (только для клиента).
 * @param {Object} data - { appointment_id, rating, text }
 */
export function createReview(data) {
  return api.post('/reviews/', data);
}

/**
 * Получение отзывов с опциональной фильтрацией по психологу.
 * @param {Object} params - { psychologist, page }
 */
export function getReviews(params = {}) {
  return api.get('/reviews/', { params });
}
