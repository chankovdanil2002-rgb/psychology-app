import api from './axios';

/**
 * Получение доступных тайм-слотов психолога с опциональной фильтрацией по дате.
 * @param {Object} params - { psychologist, date }
 */
export function getSlots(params = {}) {
  return api.get('/schedule/slots/', { params });
}

/**
 * Создание одного тайм-слота (только для психолога).
 * @param {Object} data - { date, start_time, end_time }
 */
export function createSlot(data) {
  return api.post('/schedule/slots/', data);
}

/**
 * Массовое создание тайм-слотов (только для психолога).
 * @param {Object} data - { date_from, date_to, start_time, end_time, weekdays }
 */
export function createBulkSlots(data) {
  return api.post('/schedule/slots/bulk/', data);
}

/**
 * Удаление тайм-слота (только для психолога, если нет привязанной записи).
 * @param {number|string} id
 */
export function deleteSlot(id) {
  return api.delete(`/schedule/slots/${id}/`);
}
