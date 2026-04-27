import api from './axios';

/**
 * Создаёт новую запись на консультацию (только для клиента).
 * @param {Object} data - { time_slot_id, comment? }
 */
export function createAppointment(data) {
  return api.post('/appointments/create/', data);
}

/**
 * Получение списка записей текущего пользователя (клиента или психолога).
 */
export function getAppointments(params = {}) {
  return api.get('/appointments/', { params });
}

/**
 * Подтверждение ожидающей записи (только для психолога).
 * @param {number|string} id
 */
export function confirmAppointment(id) {
  return api.patch(`/appointments/${id}/confirm/`);
}

/**
 * Отклонение ожидающей записи (только для психолога).
 * @param {number|string} id
 */
export function rejectAppointment(id) {
  return api.patch(`/appointments/${id}/reject/`);
}

/**
 * Отметка записи как завершённой (только для психолога).
 * @param {number|string} id
 */
export function completeAppointment(id) {
  return api.patch(`/appointments/${id}/complete/`);
}

/**
 * Отмена записи клиентом (только если статус «ожидает» или «подтверждена»).
 * @param {number|string} id
 */
export function cancelAppointment(id) {
  return api.patch(`/appointments/${id}/cancel/`);
}
