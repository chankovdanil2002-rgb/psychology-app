import { Link } from 'react-router-dom';
import styles from './PsychologistRegisterPage.module.css';

/**
 * Informational page for psychologists.
 * Psychologist accounts are created by the admin.
 */
export default function PsychologistRegisterPage() {
  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>Для психологов</h1>
        <p className={styles.subtitle}>
          Учётные записи специалистов создаёт администратор сайта. После
          получения логина и пароля вы сможете войти в систему, заполнить
          профиль и работать с клиентскими записями.
        </p>

        <div className={styles.form}>
          <Link to="/login" className={styles.loginLink}>
            Перейти ко входу
          </Link>
          <Link to="/" className={styles.link}>
            На главную
          </Link>
        </div>

        <p className={styles.footer}>
          Если вы входите в команду молодых психологов при институте, обратитесь
          к администратору для создания аккаунта.
        </p>
      </div>
    </div>
  );
}
