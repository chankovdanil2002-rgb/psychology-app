import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import ProtectedRoute from './components/layout/ProtectedRoute';

// Компоненты страниц
import HomePage from './pages/Home/HomePage';
import LoginPage from './pages/Auth/LoginPage';
import ClientRegisterPage from './pages/Auth/ClientRegisterPage';
import EmailConfirmPage from './pages/Auth/EmailConfirmPage';
import CatalogPage from './pages/Catalog/CatalogPage';
import PsychologistDetailPage from './pages/Catalog/PsychologistDetailPage';
import ProfilePage from './pages/Profile/ProfilePage';
import BookingWizard from './pages/Booking/BookingWizard';
import AppointmentsPage from './pages/Dashboard/AppointmentsPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import AdminVerificationPage from './pages/Admin/AdminVerificationPage';

export default function App() {
  return (
    <AuthProvider>
        <Header />
        <main style={{ flex: 1 }}>
          <Routes>
            {/* Публичные маршруты */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<ClientRegisterPage />} />
            <Route path="/confirm-email/:token" element={<EmailConfirmPage />} />
            <Route path="/catalog" element={<CatalogPage />} />
            <Route path="/psychologists/:id" element={<PsychologistDetailPage />} />

            {/* Защищённые: любой авторизованный пользователь */}
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />

            {/* Защищённые: клиент с заполненным профилем */}
            <Route
              path="/booking"
              element={
                <ProtectedRoute role="client" profileComplete>
                  <BookingWizard />
                </ProtectedRoute>
              }
            />

            {/* Защищённые: любой авторизованный (показывает разные данные для клиента/психолога) */}
            <Route
              path="/appointments"
              element={
                <ProtectedRoute>
                  <AppointmentsPage />
                </ProtectedRoute>
              }
            />

            {/* Защищённые: только для психолога */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute role="psychologist">
                  <DashboardPage />
                </ProtectedRoute>
              }
            />

            {/* Защищённые: только для администратора */}
            <Route
              path="/admin/psychologists"
              element={
                <ProtectedRoute role="admin">
                  <AdminVerificationPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/verification"
              element={
                <ProtectedRoute role="admin">
                  <AdminVerificationPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </main>
        <Footer />
    </AuthProvider>
  );
}
