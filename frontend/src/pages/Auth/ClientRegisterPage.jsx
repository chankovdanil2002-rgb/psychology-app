import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';
import Alert from '../../components/ui/Alert';
import styles from './ClientRegisterPage.module.css';

/**
 * Страница регистрации клиента.
 * Собирает email, пароль и подтверждение пароля.
 * При успехе показывает сообщение с просьбой проверить почту.
 */
export default function ClientRegisterPage() {
  const { registerClient } = useAuth();

  const [form, setForm] = useState({
    email: '',
    password: '',
    password_confirm: '',
  });
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

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
    } else if (form.password.length < 8) {
      errs.password = 'Пароль должен содержать минимум 8 символов';
    }
    if (!form.password_confirm) {
      errs.password_confirm = 'Подтвердите пароль';
    } else if (form.password !== form.password_confirm) {
      errs.password_confirm = 'Пароли не совпадают';
    }
    return errs;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
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
      await registerClient({
        email: form.email,
        password: form.password,
        password_confirm: form.password_confirm,
      });
      setSuccess(true);
    } catch (err) {
      const resp = err.response?.data;
      // API возвращает { status: "error", message: "...", data: { field: [...] } }
      if (resp && typeof resp === 'object') {
        if (resp.message) {
          setServerError(resp.message);
        }
        // Разбираем ошибки по полям из resp.data
        const errData = resp.data || resp;
        const fieldErrors = {};
        for (const [key, val] of Object.entries(errData)) {
          if (key === 'status' || key === 'message') continue;
          if (Array.isArray(val)) {
            fieldErrors[key] = val.join(' ');
          } else if (typeof val === 'string') {
            fieldErrors[key] = val;
          }
        }
        if (Object.keys(fieldErrors).length) {
          setErrors(fieldErrors);
        }
      }
      if (!resp?.message) {
        setServerError('Произошла ошибка при регистрации. Попробуйте позже.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Состояние успеха
  if (success) {
    return (
      <div className={styles.page}>
        <div className={styles.card}>
          <div className={styles.successIcon}>
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--color-success)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 11.08V12a10 10 0 11-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          </div>
          <h2 className={styles.title}>Регистрация прошла успешно!</h2>
          <p className={styles.successText}>
            Мы отправили письмо на <strong>{form.email}</strong>.
            Пожалуйста, проверьте почту и перейдите по ссылке для подтверждения аккаунта.
          </p>
          <Link to="/login" className={styles.loginLink}>
            Перейти к входу
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>Регистрация клиента</h1>
        <p className={styles.subtitle}>
          Создайте аккаунт, чтобы записаться на консультацию
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
            placeholder="Минимум 8 символов"
            value={form.password}
            onChange={handleChange}
            error={errors.password}
            autoComplete="new-password"
          />

          <Input
            label="Подтверждение пароля"
            type="password"
            name="password_confirm"
            placeholder="Повторите пароль"
            value={form.password_confirm}
            onChange={handleChange}
            error={errors.password_confirm}
            autoComplete="new-password"
          />

          <Button type="submit" fullWidth loading={loading}>
            Зарегистрироваться
          </Button>
        </form>

        <p className={styles.footer}>
          Уже есть аккаунт?{' '}
          <Link to="/login" className={styles.link}>
            Войти
          </Link>
        </p>
      </div>
    </div>
  );
}
