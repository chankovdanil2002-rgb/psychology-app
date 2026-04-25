import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { getSpecializations, getPsychologists, getSlots, createAppointment } from '../../api';
import Alert from '../../components/ui/Alert';
import Button from '../../components/ui/Button';
import Loader from '../../components/ui/Loader';
import StarRating from '../../components/ui/StarRating';
import { BOOKING_STEPS } from '../../utils/constants';
import { extractList, formatDate, formatPrice, formatTime } from '../../utils/helpers';
import styles from './BookingWizard.module.css';

export default function BookingWizard() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const preselectedPsych = searchParams.get('psychologist');

  const [step, setStep] = useState(preselectedPsych ? 2 : 0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  // Данные
  const [specializations, setSpecializations] = useState([]);
  const [psychologists, setPsychologists] = useState([]);

  // Выбранные значения
  const [selectedSpec, setSelectedSpec] = useState('');
  const [selectedPsych, setSelectedPsych] = useState(preselectedPsych || null);
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [comment, setComment] = useState('');

  // Шаг 0: загрузка специализаций
  useEffect(() => {
    if (step === 0) {
      setLoading(true);
      getSpecializations()
        .then((res) => {
          const data = extractList(res);
          setSpecializations(data);
        })
        .catch(() => {})
        .finally(() => setLoading(false));
    }
  }, [step]);

  // Шаг 1: загрузка психологов по выбранной специализации
  useEffect(() => {
    if (step === 1 || (step === 2 && preselectedPsych)) {
      setLoading(true);
      const params = {};
      if (selectedSpec) params.specialization = selectedSpec;
      getPsychologists(params)
        .then((res) => {
          const list = extractList(res);
          setPsychologists(list);
        })
        .catch(() => {})
        .finally(() => setLoading(false));
    }
  }, [step, selectedSpec, preselectedPsych]);

  // Все доступные слоты выбранного психолога (без фильтра по дате)
  const [allSlots, setAllSlots] = useState([]);

  // Уникальные даты, на которых есть свободные слоты
  const availableDates = [...new Set(allSlots.map((s) => s.date))].sort();

  // Шаг 2: загружаем ВСЕ доступные слоты психолога одним запросом
  useEffect(() => {
    if (step === 2 && selectedPsych) {
      setLoading(true);
      setAllSlots([]);
      setSelectedDate('');
      setSelectedSlot(null);
      getSlots({ psychologist: selectedPsych })
        .then((res) => {
          const data = extractList(res);
          setAllSlots(data);
        })
        .catch(() => setAllSlots([]))
        .finally(() => setLoading(false));
    }
  }, [step, selectedPsych]);

  // Слоты для выбранной даты
  const slots = selectedDate
    ? allSlots.filter((s) => s.date === selectedDate)
    : [];

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      await createAppointment({
        time_slot_id: selectedSlot.id,
        comment,
      });
      setSuccess(true);
      setTimeout(() => navigate('/appointments'), 2000);
    } catch (err) {
      setError(err.response?.data?.message || 'Ошибка при создании записи');
    } finally {
      setLoading(false);
    }
  };

  const selectedPsychData = psychologists.find((p) => String(p.id) === String(selectedPsych));

  if (success) {
    return (
      <div className={styles.wizard}>
        <Alert variant="success">
          Запись успешно создана! Ожидайте подтверждения от психолога. Перенаправление...
        </Alert>
      </div>
    );
  }

  return (
    <div className={styles.wizard}>
      <h1>Запись на консультацию</h1>

      {/* Индикатор шагов */}
      <div className={styles.steps}>
        {BOOKING_STEPS.map((s, i) => (
          <div key={s.key} className={`${styles.stepItem} ${i === step ? styles.stepActive : ''} ${i < step ? styles.stepDone : ''}`}>
            <div className={styles.stepNum}>{i < step ? '✓' : i + 1}</div>
            <span>{s.label}</span>
          </div>
        ))}
      </div>

      {error && <Alert variant="error" onClose={() => setError('')}>{error}</Alert>}

      <div className={styles.stepContent}>
        {/* Шаг 0: специализация */}
        {step === 0 && (
          <>
            <h2>Выберите специализацию</h2>
            {loading ? <Loader /> : (
              <div className={styles.cardGrid}>
                {specializations.map((s) => (
                  <button
                    key={s.id}
                    className={`${styles.selCard} ${selectedSpec === s.slug ? styles.selCardActive : ''}`}
                    onClick={() => setSelectedSpec(s.slug)}
                  >
                    <h3>{s.name}</h3>
                    {s.description && <p>{s.description}</p>}
                  </button>
                ))}
              </div>
            )}
            <div className={styles.nav}>
              <div />
              <Button onClick={() => setStep(1)} disabled={!selectedSpec}>
                Далее
              </Button>
            </div>
          </>
        )}

        {/* Шаг 1: психолог */}
        {step === 1 && (
          <>
            <h2>Выберите психолога</h2>
            {loading ? <Loader /> : (
              <div className={styles.cardGrid}>
                {psychologists.map((p) => (
                  <button
                    key={p.id}
                    className={`${styles.selCard} ${String(selectedPsych) === String(p.id) ? styles.selCardActive : ''}`}
                    onClick={() => setSelectedPsych(p.id)}
                  >
                    <h3>{p.full_name}</h3>
                    <StarRating value={p.average_rating || 0} size="sm" showValue />
                    <p>{formatPrice(p.price)}</p>
                  </button>
                ))}
                {psychologists.length === 0 && <p>Психологи не найдены</p>}
              </div>
            )}
            <div className={styles.nav}>
              <Button variant="outline" onClick={() => setStep(0)}>Назад</Button>
              <Button onClick={() => setStep(2)} disabled={!selectedPsych}>Далее</Button>
            </div>
          </>
        )}

        {/* Шаг 2: дата и время */}
        {step === 2 && (
          <>
            <h2>Выберите дату и время</h2>
            {loading ? <Loader /> : availableDates.length === 0 ? (
              <p className={styles.noSlots}>У этого психолога нет свободных слотов</p>
            ) : (
              <>
                <div className={styles.dateGrid}>
                  {availableDates.map((d) => {
                    const count = allSlots.filter((s) => s.date === d).length;
                    return (
                      <button
                        key={d}
                        className={`${styles.dateBtn} ${selectedDate === d ? styles.dateBtnActive : ''}`}
                        onClick={() => { setSelectedDate(d); setSelectedSlot(null); }}
                      >
                        <span>{formatDate(d)}</span>
                        <small>{count} сл.</small>
                      </button>
                    );
                  })}
                </div>
                {selectedDate && (
                  <div className={styles.slotGrid}>
                    {slots.map((s) => (
                      <button
                        key={s.id}
                        className={`${styles.slotBtn} ${selectedSlot?.id === s.id ? styles.slotBtnActive : ''}`}
                        onClick={() => setSelectedSlot(s)}
                      >
                        {formatTime(s.start_time)} – {formatTime(s.end_time)}
                      </button>
                    ))}
                  </div>
                )}
              </>
            )}
            <div className={styles.nav}>
              <Button variant="outline" onClick={() => setStep(preselectedPsych ? 0 : 1)}>Назад</Button>
              <Button onClick={() => setStep(3)} disabled={!selectedSlot}>Далее</Button>
            </div>
          </>
        )}

        {/* Шаг 3: подтверждение */}
        {step === 3 && (
          <>
            <h2>Подтверждение записи</h2>
            <div className={styles.summary}>
              <div className={styles.summaryRow}>
                <strong>Психолог:</strong>
                <span>{selectedPsychData?.full_name || `#${selectedPsych}`}</span>
              </div>
              <div className={styles.summaryRow}>
                <strong>Дата:</strong>
                <span>{formatDate(selectedDate)}</span>
              </div>
              <div className={styles.summaryRow}>
                <strong>Время:</strong>
                <span>{formatTime(selectedSlot?.start_time)} – {formatTime(selectedSlot?.end_time)}</span>
              </div>
              {selectedPsychData?.price && (
                <div className={styles.summaryRow}>
                  <strong>Стоимость:</strong>
                  <span>{formatPrice(selectedPsychData.price)}</span>
                </div>
              )}
            </div>
            <div className={styles.commentBlock}>
              <label>Комментарий (необязательно):</label>
              <textarea
                className={styles.textarea}
                rows={3}
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Опишите вашу ситуацию или задайте вопрос..."
              />
            </div>
            <div className={styles.nav}>
              <Button variant="outline" onClick={() => setStep(2)}>Назад</Button>
              <Button onClick={handleSubmit} loading={loading}>
                Подтвердить запись
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
