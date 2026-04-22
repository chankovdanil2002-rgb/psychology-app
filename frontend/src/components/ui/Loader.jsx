import styles from './Loader.module.css';

/**
 * Spinning loader component.
 * Supports small, medium, and large sizes.
 */
export default function Loader({ size = 'medium', className = '' }) {
  return (
    <div className={`${styles.wrapper} ${className}`}>
      <div className={`${styles.spinner} ${styles[size]}`} role="status">
        <span className={styles.srOnly}>Loading...</span>
      </div>
    </div>
  );
}
