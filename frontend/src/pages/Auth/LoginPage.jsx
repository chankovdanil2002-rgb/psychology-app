import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';
import Alert from '../../components/ui/Alert';
import styles from './LoginPage.module.css';

/**
 * Страница входа с формой email/пароль.
 * Использует AuthContext.login() и редиректит на /profile при успехе.
 */
export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [form, setForm] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [loading, setLoading] = useState(false);

  // Клиентская валидация
  const validate = () => {
    const errs = {};
    if (!form.email.trim()) {
      errs.email = 'Введите email';
    } else if (!/\S+@\S+\.\S+/.test(form.email)) {
      errs.email = 'Некорректный формат email';
    }
    if (!form.password) {
      errs.password = 'Введите пароль';
    }
    return errs;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    // Сбрасываем ошибку поля при изменении
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
    if (serverError) setServerError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) {
      setErrors(errs);
      return;
    }

    setLoading(true);
    setServerError('');

    try {
      await login(form.email, form.password);
      navigate('/profile');
    } catch (err) {
      const data = err.response?.data;
      if (data?.message) {
        setServerError(data.message);
      } else if (data?.detail) {
        setServerError(data.detail);
      } else {
        setServerError('Неверный email или пароль');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>Вход в аккаунт</h1>
        <p className={styles.subtitle}>
          Введите свои данные для входа
        </p>

        {serverError && (
          <Alert variant="error" onClose={() => setServerError('')}>
            {serverError}
          </Alert>
        )}

        <form onSubmit={handleSubmit} className={styles.form} noValidate>
          <Input
            label="Email"
            type="email"
            name="email"
            placeholder="your@email.com"
            value={form.email}
            onChange={handleChange}
            error={errors.email}
            autoComplete="email"
          />

          <Input
            label="Пароль"
            type="password"
            name="password"
            placeholder="Введите пароль"
            value={form.password}
            onChange={handleChange}
            error={errors.password}
            autoComplete="current-password"
          />

          <Button
            type="submit"
            fullWidth
            loading={loading}
          >
            Войти
          </Button>
        </form>

        <p className={styles.footer}>
          Нет аккаунта?{' '}
          <Link to="/register" className={styles.link}>
            Зарегистрироваться
          </Link>
        </p>
      </div>
    </div>
  );
}
