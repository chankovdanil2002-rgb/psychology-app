import api from './axios';

/**
 * Регистрация нового аккаунта клиента.
 * @param {Object} data - { email, password, password_confirm }
 */
export function registerClient(data) {
  return api.post('/auth/register/client/', data);
}

/**
 * Вход по email и паролю. Возвращает пару JWT-токенов.
 * @param {string} email
 * @param {string} password
 */
export function login(email, password) {
  return api.post('/auth/login/', { email, password });
}

/**
 * Обновление JWT access-токена.
 * @param {string} refresh - Refresh-токен
 */
export function refreshToken(refresh) {
  return api.post('/auth/token/refresh/', { refresh });
}

/**
 * Подтверждение email по токену из письма.
 * @param {string} token
 */
export function confirmEmail(token) {
  return api.get(`/auth/confirm-email/${token}/`);
}

export function confirmEmailCode(email, code) {
  return api.post('/auth/confirm-email/code/', { email, code });
}

/**
 * Получение профиля текущего авторизованного пользователя.
 */
export function getProfile() {
  return api.get('/profile/me/');
}

/**
 * Полное обновление профиля текущего пользователя.
 * @param {Object|FormData} data - Поля профиля (могут включать файлы: аватар, фото)
 */
export function updateProfile(data) {
  const isFormData = data instanceof FormData;
  return api.put('/profile/me/', data, {
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
  });
}

/**
 * Частичное обновление профиля текущего пользователя.
 * @param {Object|FormData} data - Частичные поля профиля
 */
export function patchProfile(data) {
  const isFormData = data instanceof FormData;
  return api.patch('/profile/me/', data, {
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
  });
}

/**
 * Запрос письма для сброса пароля.
 * @param {Object} data - { email }
 */
export function requestPasswordReset(data) {
  return api.post('/auth/password-reset/', data);
}
