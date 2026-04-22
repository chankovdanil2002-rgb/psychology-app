import { useState } from 'react';
import styles from './StarRating.module.css';

/**
 * Interactive/display star rating component.
 * @param {number} value - Current rating (1-5)
 * @param {function} onChange - If provided, enables interactive mode
 * @param {number} max - Maximum stars (default 5)
 * @param {boolean} showValue - Show numeric value next to stars
 * @param {string} size - 'sm' | 'md' | 'lg'
 */
export default function StarRating({
  value = 0,
  onChange,
  max = 5,
  showValue = false,
  size = 'md',
}) {
  const [hoverValue, setHoverValue] = useState(0);
  const interactive = typeof onChange === 'function';
  const displayValue = hoverValue || value;

  return (
    <div className={`${styles.wrapper} ${styles[size]}`}>
      <div className={styles.stars}>
        {Array.from({ length: max }, (_, i) => {
          const starValue = i + 1;
          const filled = starValue <= displayValue;
          return (
            <span
              key={starValue}
              className={`${styles.star} ${filled ? styles.filled : ''} ${interactive ? styles.interactive : ''}`}
              onClick={() => interactive && onChange(starValue)}
              onMouseEnter={() => interactive && setHoverValue(starValue)}
              onMouseLeave={() => interactive && setHoverValue(0)}
              role={interactive ? 'button' : 'presentation'}
              tabIndex={interactive ? 0 : undefined}
              onKeyDown={(e) => {
                if (interactive && (e.key === 'Enter' || e.key === ' ')) {
                  e.preventDefault();
                  onChange(starValue);
                }
              }}
            >
              ★
            </span>
          );
        })}
      </div>
      {showValue && value > 0 && (
        <span className={styles.value}>{value.toFixed(1)}</span>
      )}
    </div>
  );
}
