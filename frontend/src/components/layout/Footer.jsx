import { Link } from 'react-router-dom';
import styles from './Footer.module.css';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.top}>
          <div className={styles.brand}>
            <span className={styles.brandIcon}>🧠</span>
            <span className={styles.brandName}>Психологи ИППС СФУ</span>
          </div>
          <div className={styles.links}>
            <Link to="/catalog">Психологи</Link>
            <Link to="/booking">Записаться</Link>
            <Link to="/register">Регистрация</Link>
          </div>
        </div>
        <div className={styles.bottom}>
          <p>&copy; {currentYear} ИППС СФУ, кафедра ПРиК. Учебный проект.</p>
        </div>
      </div>
    </footer>
  );
}
