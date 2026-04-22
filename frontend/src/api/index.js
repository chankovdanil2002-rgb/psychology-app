import api from './axios';

// --- Auth ---

export function registerClient(data) {
  return api.post('/auth/register/client/', data);
}

export function login(email, password) {
  return api.post('/auth/login/', { email, password });
}

export function refreshToken(refresh) {
  return api.post('/auth/token/refresh/', { refresh });
}

export function confirmEmail(token) {
  return api.get(`/auth/confirm-email/${token}/`);
}

export function getProfile() {
  return api.get('/profile/me/');
}

export function updateProfile(data) {
  const isFormData = data instanceof FormData;
  return api.put('/profile/me/', data, {
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
  });
}

export function patchProfile(data) {
  const isFormData = data instanceof FormData;
  return api.patch('/profile/me/', data, {
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
  });
}

export function requestPasswordReset(data) {
  return api.post('/auth/password-reset/', data);
}

// --- Appointments ---

export function createAppointment(data) {
  return api.post('/appointments/', data);
}

export function getAppointments(params = {}) {
  return api.get('/appointments/', { params });
}

export function confirmAppointment(id) {
  return api.patch(`/appointments/${id}/confirm/`);
}

export function rejectAppointment(id) {
  return api.patch(`/appointments/${id}/reject/`);
}

export function completeAppointment(id) {
  return api.patch(`/appointments/${id}/complete/`);
}

export function cancelAppointment(id) {
  return api.patch(`/appointments/${id}/cancel/`);
}

// --- Schedule ---

export function getSlots(params = {}) {
  return api.get('/schedule/slots/', { params });
}

export function createSlot(data) {
  return api.post('/schedule/slots/', data);
}

export function createBulkSlots(data) {
  return api.post('/schedule/slots/bulk/', data);
}

export function deleteSlot(id) {
  return api.delete(`/schedule/slots/${id}/`);
}

// --- Psychologists ---

export function getPsychologists(params = {}) {
  return api.get('/psychologists/', { params });
}

export function getPsychologistById(id) {
  return api.get(`/psychologists/${id}/`);
}

export function getAdminPsychologists() {
  return api.get('/admin/psychologists/');
}

export function createAdminPsychologist(data) {
  return api.post('/admin/psychologists/', data);
}

// --- Specializations ---

export function getSpecializations() {
  return api.get('/specializations/');
}

export function getSpecializationBySlug(slug) {
  return api.get(`/specializations/${slug}/`);
}

// --- Reviews ---

export function createReview(data) {
  return api.post('/reviews/', data);
}

export function getReviews(params = {}) {
  return api.get('/reviews/', { params });
}

