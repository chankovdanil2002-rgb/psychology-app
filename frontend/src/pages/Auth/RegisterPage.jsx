import { Link } from 'react-router-dom';
import styles from './RegisterPage.module.css';

/**
 * Register page for client accounts.
 * Psychologist accounts are created by the admin.
 */
export default function RegisterPage() {
  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <h1 className={styles.title}>Регистрация клиента</h1>
        <p className={styles.subtitle}>
          Создайте аккаунт, подтвердите email и записывайтесь к психологам
          команды
        </p>

        <div className={styles.cards}>
          <Link to="/register/client" className={styles.card}>
            <div className={styles.icon}>
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            </div>
            <h2 className={styles.cardTitle}>Создать аккаунт</h2>
            <p className={styles.cardDesc}>
              После входа в систему вы сможете выбрать специалиста и оформить
              запись на консультацию.
            </p>
          </Link>
        </div>

        <p className={styles.subtitle}>
          Аккаунты психологов создаёт администратор сайта.
        </p>

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
