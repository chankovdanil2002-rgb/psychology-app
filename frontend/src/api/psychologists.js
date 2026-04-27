import api from './axios';

/**
 * Получение постраничного списка психологов с опциональными фильтрами.
 * @param {Object} params - { specialization, search, ordering, page }
 */
export function getPsychologists(params = {}) {
  return api.get('/psychologists/', { params });
}

/**
 * Получение детальной информации о конкретном психологе.
 * @param {number|string} id
 */
export function getPsychologistById(id) {
  return api.get(`/psychologists/${id}/`);
}

/**
 * Получение списка психологов для административного управления командой.
 */
export function getAdminPsychologists() {
  return api.get('/admin/psychologists/');
}

/**
 * Создание аккаунта психолога из административной панели.
 * @param {Object} data
 */
export function createAdminPsychologist(data) {
  return api.post('/admin/psychologists/', data);
}

/**
 * Удаление психолога администратором (каскадно удаляет записи и слоты).
 * @param {number|string} id
 */
export function deleteAdminPsychologist(id) {
  return api.delete(`/admin/psychologists/${id}/`);
}
