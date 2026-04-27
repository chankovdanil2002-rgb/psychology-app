import { useState } from 'react';
import styles from './StarRating.module.css';

/**
 * Компонент звёздного рейтинга — интерактивный или только для отображения.
 * @param {number} value - Текущий рейтинг (1–5)
 * @param {function} onChange - При передаче включает интерактивный режим
 * @param {number} max - Максимальное число звёзд (по умолчанию 5)
 * @param {boolean} showValue - Показывать числовое значение рядом со звёздами
 * @param {string} size - Размер: 'sm' | 'md' | 'lg'
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
