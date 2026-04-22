import styles from './Alert.module.css';

/**
 * Alert/message component.
 * Variants: success, error, info, warning.
 */
export default function Alert({
  children,
  variant = 'info',
  onClose,
  className = '',
}) {
  const variantClass = styles[variant] || styles.info;

  return (
    <div className={`${styles.alert} ${variantClass} ${className}`} role="alert">
      <div className={styles.content}>{children}</div>
      {onClose && (
        <button
          className={styles.closeBtn}
          onClick={onClose}
          aria-label="Close"
        >
          &times;
        </button>
      )}
    </div>
  );
}
