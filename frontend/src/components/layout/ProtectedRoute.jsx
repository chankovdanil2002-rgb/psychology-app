import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

/**
 * ProtectedRoute защищает маршруты, требующие аутентификации,
 * опционально — конкретной роли или заполненного профиля.
 *
 * Props:
 *  - children: компонент страницы для рендеринга
 *  - role: (опционально) требуемая роль ('client' | 'psychologist' | 'admin')
 *  - profileComplete: (опционально) если true, user.is_profile_complete должен быть true
 */
export default function ProtectedRoute({ children, role, profileComplete }) {
  const { isAuthenticated, user, loading } = useAuth();
  const location = useLocation();

  // Состояние авторизации ещё загружается — пока ничего не показываем
  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '4rem' }}>
        <p>Загрузка...</p>
      </div>
    );
  }

  // Не аутентифицирован -> редирект на логин с сохранением исходного маршрута
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Несоответствие роли -> редирект на главную
  if (role && user?.role !== role) {
    return <Navigate to="/" replace />;
  }

  // Проверка заполненности профиля -> редирект на страницу профиля
  if (profileComplete && !user?.is_profile_complete) {
    return <Navigate to="/profile" replace />;
  }

  return children;
}
