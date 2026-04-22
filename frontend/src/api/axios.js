import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request-интерцептор: прикрепляет JWT access-токен из localStorage
api.interceptors.request.use(
  (config) => {
    const tokens = localStorage.getItem('tokens');
    if (tokens) {
      try {
        const { access } = JSON.parse(tokens);
        if (access) {
          config.headers.Authorization = `Bearer ${access}`;
        }
      } catch {
        // Некорректные данные токена — игнорируем
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response-интерцептор: обрабатывает 401, пытаясь обновить токен
let isRefreshing = false;
let failedQueue = [];

function processQueue(error, token = null) {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error);
    } else {
      resolve(token);
    }
  });
  failedQueue = [];
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Пропускаем логику обновления для самого refresh-эндпоинта и логина
    if (
      originalRequest.url === '/auth/token/refresh/' ||
      originalRequest.url === '/auth/login/'
    ) {
      return Promise.reject(error);
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Откладываем запрос в очередь до завершения обновления токена
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return api(originalRequest);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const tokens = localStorage.getItem('tokens');
        if (!tokens) throw new Error('No tokens stored');

        const { refresh } = JSON.parse(tokens);
        if (!refresh) throw new Error('No refresh token');

        const { data } = await axios.post('/api/auth/token/refresh/', {
          refresh,
        });

        const newTokens = { access: data.access, refresh };
        localStorage.setItem('tokens', JSON.stringify(newTokens));

        processQueue(null, data.access);

        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        // Чистим состояние авторизации и редиректим на логин
        localStorage.removeItem('tokens');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;
