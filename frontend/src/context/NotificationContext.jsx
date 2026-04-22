import { createContext, useContext, useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { useAuth } from './AuthContext';
import * as notificationsApi from '../api';
import { extractList } from '../utils/helpers';

const NotificationContext = createContext(null);

// Интервал опроса в миллисекундах (30 секунд)
const POLL_INTERVAL = 30000;

/**
 * Хук для доступа к контексту уведомлений.
 */
export function useNotifications() {
  const ctx = useContext(NotificationContext);
  if (!ctx) {
    throw new Error('useNotifications must be used within a NotificationProvider');
  }
  return ctx;
}

/**
 * NotificationProvider опрашивает сервер каждые 30 секунд,
 * пока пользователь аутентифицирован.
 */
export function NotificationProvider({ children }) {
  const { isAuthenticated } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const intervalRef = useRef(null);

  const fetchNotifications = useCallback(async () => {
    if (!isAuthenticated) return;
    try {
      setLoading(true);
      const res = await notificationsApi.getNotifications();
      const items = extractList(res);
      setNotifications(items);
    } catch {
      // Тихо игнорируем — уведомления не критичны
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  // Запуск/остановка опроса в зависимости от статуса аутентификации
  useEffect(() => {
    if (isAuthenticated) {
      fetchNotifications();
      intervalRef.current = setInterval(fetchNotifications, POLL_INTERVAL);
    } else {
      setNotifications([]);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [isAuthenticated, fetchNotifications]);

  const markAsRead = useCallback(async (id) => {
    try {
      await notificationsApi.markRead(id);
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch {
      // Игнорируем
    }
  }, []);

  const markAllAsRead = useCallback(async () => {
    try {
      await notificationsApi.markAllRead();
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
    } catch {
      // Игнорируем
    }
  }, []);

  const unreadCount = useMemo(
    () => notifications.filter((n) => !n.is_read).length,
    [notifications]
  );

  const value = useMemo(
    () => ({
      notifications,
      unreadCount,
      loading,
      fetchNotifications,
      markAsRead,
      markAllAsRead,
    }),
    [notifications, unreadCount, loading, fetchNotifications, markAsRead, markAllAsRead]
  );

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
}

export default NotificationContext;
