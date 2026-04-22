import { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import * as authApi from '../api';

const AuthContext = createContext(null);

/**
 * Хук для доступа к контексту авторизации.
 */
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return ctx;
}

/**
 * AuthProvider управляет состоянием авторизации, JWT-токенами
 * и предоставляет функции login/logout/register.
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState(() => {
    try {
      const stored = localStorage.getItem('tokens');
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Сохраняем токены в localStorage при каждом изменении
  useEffect(() => {
    if (tokens) {
      localStorage.setItem('tokens', JSON.stringify(tokens));
    } else {
      localStorage.removeItem('tokens');
    }
  }, [tokens]);

  // On mount (or when tokens change), fetch the user profile
  const fetchProfile = useCallback(async () => {
    if (!tokens?.access) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const { data } = await authApi.getProfile();
      // Поддерживаем и обёрнутый ({ data: { ... } }), и обычный формат
      setUser(data.data || data);
    } catch {
      // Токен недействителен или истёк — очищаем состояние
      setUser(null);
      setTokens(null);
    } finally {
      setLoading(false);
    }
  }, [tokens?.access]);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  // Логин: получаем токены, сохраняем, затем загружаем профиль,
  // чтобы вызывающий мог дождаться полного цикла авторизации.
  const login = useCallback(async (email, password) => {
    const { data } = await authApi.login(email, password);
    // Ответ: { status, data: { user, tokens: { access, refresh } }, message }
    const inner = data.data || data;
    const tkns = inner.tokens || inner;
    const newTokens = { access: tkns.access, refresh: tkns.refresh };

    // Сохраняем сразу, чтобы интерцептор их подхватил.
    setTokens(newTokens);
    localStorage.setItem('tokens', JSON.stringify(newTokens));

    // Загружаем профиль сразу (не ждём useEffect).
    try {
      const profileRes = await authApi.getProfile();
      setUser(profileRes.data?.data || profileRes.data);
    } catch {
      // Не удалось загрузить профиль — токены сохранены,
      // useEffect повторит попытку при следующем рендере.
    }
  }, []);

  // Logout: очищаем всё
  const logout = useCallback(() => {
    setTokens(null);
    setUser(null);
    localStorage.removeItem('tokens');
    localStorage.removeItem('user');
    navigate('/login');
  }, [navigate]);

  // Регистрация клиента
  const registerClient = useCallback(async (formData) => {
    const { data } = await authApi.registerClient(formData);
    return data;
  }, []);

  // Вычисляемые значения
  const isAuthenticated = !!user;
  const isClient = user?.role === 'client';
  const isPsychologist = user?.role === 'psychologist';
  const isAdmin = user?.role === 'admin';
  const isProfileComplete = !!user?.is_profile_complete;
  const isVerified = !!user?.is_verified;

  const value = useMemo(
    () => ({
      user,
      tokens,
      loading,
      login,
      logout,
      registerClient,
      fetchProfile,
      isAuthenticated,
      isClient,
      isPsychologist,
      isAdmin,
      isProfileComplete,
      isVerified,
    }),
    [
      user,
      tokens,
      loading,
      login,
      logout,
      registerClient,
      fetchProfile,
      isAuthenticated,
      isClient,
      isPsychologist,
      isAdmin,
      isProfileComplete,
      isVerified,
    ]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default AuthContext;
