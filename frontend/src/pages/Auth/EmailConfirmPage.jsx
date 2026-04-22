import { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { confirmEmail } from '../../api';
import Loader from '../../components/ui/Loader';
import Alert from '../../components/ui/Alert';
import styles from './EmailConfirmPage.module.css';

/**
 * Страница подтверждения email.
 * Читает токен из параметров URL и вызывает API подтверждения.
 * Показывает сообщение об успехе/ошибке и ссылку на логин.
 *
 * Использует ref-защиту, чтобы React StrictMode не вызвал
 * запрос подтверждения дважды в режиме разработки.
 */
export default function EmailConfirmPage() {
  const { token } = useParams();
  const [status, setStatus] = useState('loading'); // loading | success | error
  const [message, setMessage] = useState('');
  const calledRef = useRef(false);

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setMessage('Ссылка подтверждения недействительна. Токен отсутствует.');
      return;
    }

    // Защита от двойного вызова в React StrictMode в dev-режиме.
    if (calledRef.current) return;
    calledRef.current = true;

    const confirm = async () => {
      try {
        const { data } = await confirmEmail(token);
        setStatus('success');
        setMessage(
          data?.message || 'Ваш email успешно подтверждён!'
        );
      } catch (err) {
        const errData = err.response?.data;
        setStatus('error');
        setMessage(
          errData?.message ||
          errData?.detail ||
          'Ссылка подтверждения недействительна или истекла.'
        );
      }
    };

    confirm();
  }, [token]);

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>Подтверждение email</h1>

        {status === 'loading' && (
          <>
            <Loader size="medium" />
            <p className={styles.loadingText}>Подтверждаем ваш email...</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className={styles.iconWrapper}>
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--color-success)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 11.08V12a10 10 0 11-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
            </div>
            <Alert variant="success">{message}</Alert>
            <Link to="/login" className={styles.loginLink}>
              Перейти к входу
            </Link>
          </>
        )}

        {status === 'error' && (
          <>
            <div className={styles.iconWrapper}>
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--color-danger)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <line x1="15" y1="9" x2="9" y2="15" />
                <line x1="9" y1="9" x2="15" y2="15" />
              </svg>
            </div>
            <Alert variant="error">{message}</Alert>
            <Link to="/login" className={styles.loginLink}>
              Перейти к входу
            </Link>
          </>
        )}
      </div>
    </div>
  );
}
