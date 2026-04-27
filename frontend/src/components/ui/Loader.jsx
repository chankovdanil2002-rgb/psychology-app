import styles from './Loader.module.css';

/**
 * Компонент индикатора загрузки (спиннер).
 * Поддерживает размеры: small, medium, large.
 */
export default function Loader({ size = 'medium', className = '' }) {
  return (
    <div className={`${styles.wrapper} ${className}`}>
      <div className={`${styles.spinner} ${styles[size]}`} role="status">
        <span className={styles.srOnly}>Загрузка...</span>
      </div>
    </div>
  );
}
