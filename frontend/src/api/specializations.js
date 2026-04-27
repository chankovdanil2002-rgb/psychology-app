import api from './axios';

/**
 * Получение всех доступных специализаций.
 */
export function getSpecializations() {
  return api.get('/specializations/');
}

/**
 * Получение детальной информации о специализации по slug.
 * @param {string} slug
 */
export function getSpecializationBySlug(slug) {
  return api.get(`/specializations/${slug}/`);
}
