import { forwardRef } from 'react';
import styles from './Input.module.css';

/**
 * Reusable input component with label and error display.
 * Supports text, email, password, number, date, tel, and textarea types.
 */
const Input = forwardRef(function Input(
  {
    label,
    error,
    id,
    type = 'text',
    className = '',
    fullWidth = true,
    ...props
  },
  ref
) {
  const inputId = id || props.name;
  const isTextarea = type === 'textarea';
  const Component = isTextarea ? 'textarea' : 'input';

  return (
    <div className={`${styles.wrapper} ${fullWidth ? styles.fullWidth : ''} ${className}`}>
      {label && (
        <label htmlFor={inputId} className={styles.label}>
          {label}
        </label>
      )}
      <Component
        ref={ref}
        id={inputId}
        type={isTextarea ? undefined : type}
        className={`${styles.input} ${isTextarea ? styles.textarea : ''} ${error ? styles.inputError : ''}`}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : undefined}
        {...props}
      />
      {error && (
        <span id={`${inputId}-error`} className={styles.error} role="alert">
          {error}
        </span>
      )}
    </div>
  );
});

export default Input;
