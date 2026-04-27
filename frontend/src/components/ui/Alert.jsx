import styles from './Alert.module.css';

/**
 * Компонент уведомления / сообщения.
 * Варианты: success, error, info, warning.
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
          aria-label="Закрыть"
        >
          &times;
        </button>
      )}
    </div>
  );
}
