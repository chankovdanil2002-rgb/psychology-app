import styles from './Footer.module.css';

/**
 * Simple application footer.
 */
export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <p className={styles.text}>
          &copy; {currentYear} Психолог Онлайн. Все права защищены.
        </p>
      </div>
    </footer>
  );
}
