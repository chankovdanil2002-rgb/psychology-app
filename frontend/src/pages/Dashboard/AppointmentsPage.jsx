import { useEffect, useState } from 'react';
import { cancelAppointment, getAppointments, createReview } from '../../api';
import Alert from '../../components/ui/Alert';
import Button from '../../components/ui/Button';
import Loader from '../../components/ui/Loader';
import Modal from '../../components/ui/Modal';
import StarRating from '../../components/ui/StarRating';
import { APPOINTMENT_STATUS, APPOINTMENT_STATUS_COLOR } from '../../utils/constants';
import { extractList, formatDate, formatTime } from '../../utils/helpers';
import styles from './AppointmentsPage.module.css';

export default function AppointmentsPage() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Состояние модалки отзыва
  const [reviewModal, setReviewModal] = useState(null);
  const [reviewRating, setReviewRating] = useState(5);
  const [reviewText, setReviewText] = useState('');
  const [reviewLoading, setReviewLoading] = useState(false);

  const fetchAppointments = () => {
    setLoading(true);
    getAppointments()
      .then((res) => {
        const data = extractList(res);
        setAppointments(data);
      })
      .catch(() => setError('Не удалось загрузить записи'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const handleCancel = async (id) => {
    if (!confirm('Отменить запись?')) return;
    try {
      await cancelAppointment(id);
      setSuccess('Запись отменена');
      fetchAppointments();
    } catch {
      setError('Не удалось отменить запись');
    }
  };

  const handleReviewSubmit = async () => {
    setReviewLoading(true);
    try {
      await createReview({
        appointment_id: reviewModal.id,
        rating: reviewRating,
        text: reviewText,
      });
      setSuccess('Отзыв отправлен');
      setReviewModal(null);
      setReviewRating(5);
      setReviewText('');
      fetchAppointments();
    } catch {
      setError('Не удалось отправить отзыв');
    } finally {
      setReviewLoading(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className={styles.page}>
      <h1>Мои записи</h1>

      {error && <Alert variant="error" onClose={() => setError('')}>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')}>{success}</Alert>}

      {appointments.length === 0 ? (
        <p className={styles.empty}>У вас пока нет записей</p>
      ) : (
        <div className={styles.list}>
          {appointments.map((a) => (
            <div key={a.id} className={styles.card}>
              <div className={styles.cardHeader}>
                <span
                  className={styles.badge}
                  style={{ background: APPOINTMENT_STATUS_COLOR[a.status] }}
                >
                  {APPOINTMENT_STATUS[a.status]}
                </span>
                <span className={styles.date}>{formatDate(a.date)}</span>
              </div>
              <div className={styles.cardBody}>
                <div className={styles.info}>
                  <strong>{a.psychologist_name}</strong>
                  <span>{formatTime(a.start_time)} – {formatTime(a.end_time)}</span>
                </div>
                <div className={styles.actions}>
                  {(a.status === 'pending' || a.status === 'confirmed') && (
                    <Button variant="danger" size="sm" onClick={() => handleCancel(a.id)}>
                      Отменить
                    </Button>
                  )}
                  {a.status === 'completed' && !a.has_review && (
                    <Button size="sm" onClick={() => setReviewModal(a)}>
                      Оставить отзыв
                    </Button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Модалка отзыва */}
      {reviewModal && (
        <Modal title="Оставить отзыв" onClose={() => setReviewModal(null)}>
          <div className={styles.reviewForm}>
            <p>Психолог: <strong>{reviewModal.psychologist_name}</strong></p>
            <div className={styles.reviewField}>
              <label>Оценка:</label>
              <StarRating value={reviewRating} onChange={setReviewRating} size="lg" />
            </div>
            <div className={styles.reviewField}>
              <label>Комментарий:</label>
              <textarea
                className={styles.textarea}
                rows={4}
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                placeholder="Поделитесь впечатлениями..."
              />
            </div>
            <Button
              onClick={handleReviewSubmit}
              loading={reviewLoading}
              disabled={!reviewText.trim()}
              fullWidth
            >
              Отправить отзыв
            </Button>
          </div>
        </Modal>
      )}
    </div>
  );
}
