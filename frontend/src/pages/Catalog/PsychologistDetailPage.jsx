import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getPsychologistById } from '../../api';
import { useAuth } from '../../context/AuthContext';
import Alert from '../../components/ui/Alert';
import Loader from '../../components/ui/Loader';
import StarRating from '../../components/ui/StarRating';
import { extractData, formatPrice } from '../../utils/helpers';
import styles from './PsychologistDetailPage.module.css';

export default function PsychologistDetailPage() {
  const { id } = useParams();
  const { isAuthenticated, isClient, user } = useAuth();
  const [psych, setPsych] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setLoading(true);
    getPsychologistById(id)
      .then((res) => {
        const data = extractData(res);
        setPsych(data);
      })
      .catch(() => setError('Не удалось загрузить профиль'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Loader />;
  if (error) return <Alert variant="error">{error}</Alert>;
  if (!psych) return <Alert variant="info">Психолог не найден</Alert>;

  const canBook = isAuthenticated && isClient && user?.is_profile_complete;

  return (
    <div className={styles.detail}>
      <div className={styles.header}>
        <div className={styles.photo}>
          {psych.photo ? (
            <img src={psych.photo} alt={psych.full_name} />
          ) : (
            <div className={styles.photoPlaceholder}>
              {(psych.full_name || '?')[0]}
            </div>
          )}
        </div>
        <div className={styles.headerInfo}>
          <h1>{psych.full_name}</h1>
          <div className={styles.rating}>
            <StarRating value={psych.average_rating || 0} showValue size="md" />
            <span>({psych.total_reviews || 0} отзывов)</span>
          </div>
          {psych.specializations && (
            <div className={styles.specs}>
              {(Array.isArray(psych.specializations) ? psych.specializations : []).map((s, i) => (
                <span key={i} className={styles.specBadge}>
                  {typeof s === 'string' ? s : s.name}
                </span>
              ))}
            </div>
          )}
          <div className={styles.priceRow}>
            <span className={styles.price}>{formatPrice(psych.price)}</span>
            <span className={styles.priceLabel}>за сессию</span>
          </div>
          {canBook && (
            <Link to={`/booking?psychologist=${psych.id}`} className={styles.bookBtn}>
              Записаться на консультацию
            </Link>
          )}
          {!isAuthenticated && (
            <p className={styles.hint}>
              <Link to="/login">Войдите</Link>, чтобы записаться
            </p>
          )}
        </div>
      </div>

      <div className={styles.body}>
        <div className={styles.infoSection}>
          {psych.experience_years && (
            <div className={styles.infoItem}>
              <strong>Опыт работы:</strong> {psych.experience_years} лет
            </div>
          )}
          {psych.education && (
            <div className={styles.infoItem}>
              <strong>Образование:</strong>
              <p>{psych.education}</p>
            </div>
          )}
          {psych.bio && (
            <div className={styles.infoItem}>
              <strong>О себе:</strong>
              <p>{psych.bio}</p>
            </div>
          )}
        </div>

        {/* Отзывы */}
        <div className={styles.reviewsSection}>
          <h2>Отзывы ({psych.total_reviews || 0})</h2>
          {psych.reviews && psych.reviews.length > 0 ? (
            <div className={styles.reviewsList}>
              {psych.reviews.map((r) => (
                <div key={r.id} className={styles.reviewCard}>
                  <div className={styles.reviewHeader}>
                    <StarRating value={r.rating} size="sm" />
                    <span className={styles.reviewAuthor}>{r.client_name}</span>
                  </div>
                  <p className={styles.reviewText}>{r.text}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className={styles.noReviews}>Отзывов пока нет</p>
          )}
        </div>
      </div>
    </div>
  );
}
