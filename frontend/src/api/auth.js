import api from './axios';

/**
 * Register a new client account.
 * @param {Object} data - { email, password, password_confirm }
 */
export function registerClient(data) {
  return api.post('/auth/register/client/', data);
}

/**
 * Login with email and password. Returns JWT token pair.
 * @param {string} email
 * @param {string} password
 */
export function login(email, password) {
  return api.post('/auth/login/', { email, password });
}

/**
 * Refresh the JWT access token.
 * @param {string} refresh - Refresh token
 */
export function refreshToken(refresh) {
  return api.post('/auth/token/refresh/', { refresh });
}

/**
 * Confirm email address using the token from the confirmation link.
 * @param {string} token
 */
export function confirmEmail(token) {
  return api.get(`/auth/confirm-email/${token}/`);
}

/**
 * Get the current authenticated user's profile.
 */
export function getProfile() {
  return api.get('/profile/me/');
}

/**
 * Update the current user's profile.
 * @param {Object|FormData} data - Profile fields (may include files like avatar/photo)
 */
export function updateProfile(data) {
  const isFormData = data instanceof FormData;
  return api.put('/profile/me/', data, {
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
  });
}

/**
 * Partially update the current user's profile.
 * @param {Object|FormData} data - Partial profile fields
 */
export function patchProfile(data) {
  const isFormData = data instanceof FormData;
  return api.patch('/profile/me/', data, {
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
  });
}

/**
 * Request a password reset email.
 * @param {Object} data - { email }
 */
export function requestPasswordReset(data) {
  return api.post('/auth/password-reset/', data);
}
