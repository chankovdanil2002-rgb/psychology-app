import styles from './Button.module.css';

/**
 * Reusable button with variant support.
 * Variants: primary, secondary, danger, outline.
 */
export default function Button({
  children,
  variant = 'primary',
  type = 'button',
  disabled = false,
  loading = false,
  fullWidth = false,
  className = '',
  ...props
}) {
  const variantClass = styles[variant] || styles.primary;

  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`${styles.button} ${variantClass} ${fullWidth ? styles.fullWidth : ''} ${className}`}
      {...props}
    >
      {loading ? (
        <span className={styles.spinner} aria-hidden="true" />
      ) : null}
      <span className={loading ? styles.labelLoading : ''}>{children}</span>
    </button>
  );
}
