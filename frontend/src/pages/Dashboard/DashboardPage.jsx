import { useEffect, useState } from 'react';
import {
  confirmAppointment,
  completeAppointment,
  getAppointments,
  rejectAppointment,
  createSlot,
  createBulkSlots,
  deleteSlot,
  getSlots,
  getReviews,
} from '../../api';
import { useAuth } from '../../context/AuthContext';
import Alert from '../../components/ui/Alert';
import Button from '../../components/ui/Button';
import Loader from '../../components/ui/Loader';
import StarRating from '../../components/ui/StarRating';
import { APPOINTMENT_STATUS, APPOINTMENT_STATUS_COLOR } from '../../utils/constants';
import { extractList, formatDate, formatTime } from '../../utils/helpers';
import styles from './DashboardPage.module.css';

const TABS = [
  { key: 'appointments', label: 'Записи' },
  { key: 'schedule', label: 'Расписание' },
  { key: 'reviews', label: 'Отзывы' },
];

const WEEKDAYS = [
  { value: 0, label: 'Пн' },
  { value: 1, label: 'Вт' },
  { value: 2, label: 'Ср' },
  { value: 3, label: 'Чт' },
  { value: 4, label: 'Пт' },
  { value: 5, label: 'Сб' },
  { value: 6, label: 'Вс' },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const [tab, setTab] = useState('appointments');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  return (
    <div className={styles.dashboard}>
      <h1>Панель управления</h1>

      <div className={styles.tabs}>
        {TABS.map((t) => (
          <button
            key={t.key}
            className={`${styles.tab} ${tab === t.key ? styles.tabActive : ''}`}
            onClick={() => setTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {error && <Alert variant="error" onClose={() => setError('')}>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')}>{success}</Alert>}

      {tab === 'appointments' && (
        <AppointmentsTab
          onError={setError}
          onSuccess={setSuccess}
        />
      )}
      {tab === 'schedule' && (
        <ScheduleTab
          psychologistId={user?.id}
          onError={setError}
          onSuccess={setSuccess}
        />
      )}
      {tab === 'reviews' && (
        <ReviewsTab psychologistId={user?.id} />
      )}
    </div>
  );
}

function AppointmentsTab({ onError, onSuccess }) {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetch = () => {
    setLoading(true);
    getAppointments()
      .then((res) => {
        const data = extractList(res);
        setAppointments(data);
      })
      .catch(() => onError('Не удалось загрузить записи'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetch(); }, []);

  const handleAction = async (id, action, label) => {
    try {
      if (action === 'confirm') await confirmAppointment(id);
      else if (action === 'reject') await rejectAppointment(id);
      else if (action === 'complete') await completeAppointment(id);
      onSuccess(`Запись ${label}`);
      fetch();
    } catch (err) {
      onError(err.response?.data?.message || 'Ошибка при обработке записи');
    }
  };

  /** Возвращает true, если время окончания приёма ещё не наступило. */
  const isAppointmentOngoing = (a) => {
    if (!a.date || !a.end_time) return false;
    const endAt = new Date(`${a.date}T${a.end_time}`);
    return new Date() < endAt;
  };

  if (loading) return <Loader />;

  const pending = appointments.filter((a) => a.status === 'pending');
  const confirmed = appointments.filter((a) => a.status === 'confirmed');
  const history = appointments.filter((a) =>
    ['completed', 'rejected', 'cancelled'].includes(a.status)
  );

  return (
    <div className={styles.tabContent}>
      <Section title={`Ожидают подтверждения (${pending.length})`}>
        {pending.length === 0 ? (
          <p className={styles.empty}>Нет новых записей</p>
        ) : (
          pending.map((a) => (
            <AppointmentCard key={a.id} appointment={a}>
              <Button size="sm" onClick={() => handleAction(a.id, 'confirm', 'подтверждена')}>
                Подтвердить
              </Button>
              <Button size="sm" variant="danger" onClick={() => handleAction(a.id, 'reject', 'отклонена')}>
                Отклонить
              </Button>
            </AppointmentCard>
          ))
        )}
      </Section>

      <Section title={`Подтверждённые (${confirmed.length})`}>
        {confirmed.length === 0 ? (
          <p className={styles.empty}>Нет подтверждённых записей</p>
        ) : (
          confirmed.map((a) => (
            <AppointmentCard key={a.id} appointment={a}>
              <Button
                size="sm"
                disabled={isAppointmentOngoing(a)}
                title={isAppointmentOngoing(a) ? 'Приём ещё не завершён' : ''}
                onClick={() => handleAction(a.id, 'complete', 'завершена')}
              >
                Завершить приём
              </Button>
            </AppointmentCard>
          ))
        )}
      </Section>

      <Section title={`История (${history.length})`}>
        {history.length === 0 ? (
          <p className={styles.empty}>Нет записей в истории</p>
        ) : (
          history.map((a) => <AppointmentCard key={a.id} appointment={a} />)
        )}
      </Section>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className={styles.section}>
      <h3>{title}</h3>
      <div className={styles.sectionBody}>{children}</div>
    </div>
  );
}

function AppointmentCard({ appointment: a, children }) {
  return (
    <div className={styles.apptCard}>
      <div className={styles.apptInfo}>
        <span
          className={styles.badge}
          style={{ background: APPOINTMENT_STATUS_COLOR[a.status] }}
        >
          {APPOINTMENT_STATUS[a.status]}
        </span>
        <strong>{a.client_name}</strong>
        <span>{formatDate(a.date)}, {formatTime(a.start_time)} – {formatTime(a.end_time)}</span>
        {a.comment && <p className={styles.comment}>"{a.comment}"</p>}
      </div>
      {children && <div className={styles.apptActions}>{children}</div>}
    </div>
  );
}

/** Возвращает сегодняшнюю дату в локальном часовом поясе как YYYY-MM-DD. */
function getLocalToday() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

function ScheduleTab({ psychologistId, onError, onSuccess }) {
  const today = getLocalToday();

  const [slots, setSlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewDate, setViewDate] = useState(today);

  // Форма одного слота
  const [slotDate, setSlotDate] = useState(today);
  const [slotStart, setSlotStart] = useState('');
  const [slotEnd, setSlotEnd] = useState('');

  // Форма массового создания
  const [bulkDateFrom, setBulkDateFrom] = useState(today);
  const [bulkDateTo, setBulkDateTo] = useState(today);
  const [bulkStart, setBulkStart] = useState('09:00');
  const [bulkEnd, setBulkEnd] = useState('10:00');
  const [bulkWeekdays, setBulkWeekdays] = useState([0, 1, 2, 3, 4]);

  const fetchSlots = () => {
    if (!psychologistId) return;
    setLoading(true);
    getSlots({ psychologist: psychologistId, date: viewDate, all: 1 })
      .then((res) => {
        const data = extractList(res);
        setSlots(data);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchSlots(); }, [viewDate]);

  const handleAddSlot = async (e) => {
    e.preventDefault();
    if (slotDate < today) {
      onError('Нельзя создать слот на прошедшую дату');
      return;
    }
    if (slotEnd <= slotStart) {
      onError('Время окончания должно быть позже времени начала');
      return;
    }
    try {
      await createSlot({ date: slotDate, start_time: slotStart, end_time: slotEnd });
      onSuccess('Слот создан');
      setSlotDate(today);
      setSlotStart('');
      setSlotEnd('');
      fetchSlots();
    } catch (err) {
      onError(err.response?.data?.message || 'Не удалось создать слот');
    }
  };

  const handleBulkAdd = async (e) => {
    e.preventDefault();
    if (bulkDateFrom < today) {
      onError('Нельзя создать слоты на прошедшие даты');
      return;
    }
    if (bulkDateTo < bulkDateFrom) {
      onError('Дата окончания не может быть раньше даты начала');
      return;
    }
    if (bulkEnd <= bulkStart) {
      onError('Время окончания должно быть позже времени начала');
      return;
    }
    try {
      await createBulkSlots({
        date_from: bulkDateFrom,
        date_to: bulkDateTo,
        start_time: bulkStart,
        end_time: bulkEnd,
        weekdays: bulkWeekdays,
      });
      onSuccess('Слоты созданы');
      fetchSlots();
    } catch (err) {
      onError(err.response?.data?.message || 'Не удалось создать слоты');
    }
  };

  const handleDeleteSlot = async (id) => {
    try {
      await deleteSlot(id);
      onSuccess('Слот удалён');
      fetchSlots();
    } catch {
      onError('Не удалось удалить слот (возможно, привязана запись)');
    }
  };

  const toggleWeekday = (day) => {
    setBulkWeekdays((prev) =>
      prev.includes(day) ? prev.filter((d) => d !== day) : [...prev, day]
    );
  };

  return (
    <div className={styles.tabContent}>
      {/* Просмотр слотов */}
      <Section title="Расписание">
        <div className={styles.dateNav}>
          <label>Дата:</label>
          <input
            type="date"
            value={viewDate}
            onChange={(e) => setViewDate(e.target.value)}
            className={styles.dateInput}
          />
        </div>
        {loading ? <Loader /> : slots.length === 0 ? (
          <p className={styles.empty}>Нет слотов на выбранную дату</p>
        ) : (
          <div className={styles.slotList}>
            {slots.map((s) => (
              <div key={s.id} className={`${styles.slotItem} ${!s.is_available ? styles.slotTaken : ''}`}>
                <span>{formatTime(s.start_time)} – {formatTime(s.end_time)}</span>
                <span className={styles.slotStatus}>
                  {s.is_available ? 'Свободен' : 'Занят'}
                </span>
                {s.is_available && (
                  <button className={styles.deleteBtn} onClick={() => handleDeleteSlot(s.id)}>✕</button>
                )}
              </div>
            ))}
          </div>
        )}
      </Section>

      {/* Добавить один слот */}
      <Section title="Добавить слот">
        <form onSubmit={handleAddSlot} className={styles.slotForm}>
          <input type="date" value={slotDate} min={today} onChange={(e) => setSlotDate(e.target.value)} required className={styles.dateInput} />
          <input type="time" value={slotStart} onChange={(e) => setSlotStart(e.target.value)} required className={styles.dateInput} />
          <input type="time" value={slotEnd} onChange={(e) => setSlotEnd(e.target.value)} required className={styles.dateInput} />
          <Button type="submit">Добавить</Button>
        </form>
      </Section>

      {/* Массовое добавление */}
      <Section title="Массовое создание слотов">
        <form onSubmit={handleBulkAdd} className={styles.bulkForm}>
          <div className={styles.formRow}>
            <div>
              <label>С:</label>
              <input type="date" value={bulkDateFrom} min={today} onChange={(e) => setBulkDateFrom(e.target.value)} required className={styles.dateInput} />
            </div>
            <div>
              <label>По:</label>
              <input type="date" value={bulkDateTo} min={today} onChange={(e) => setBulkDateTo(e.target.value)} required className={styles.dateInput} />
            </div>
          </div>
          <div className={styles.formRow}>
            <div>
              <label>Начало:</label>
              <input type="time" value={bulkStart} onChange={(e) => setBulkStart(e.target.value)} required className={styles.dateInput} />
            </div>
            <div>
              <label>Конец:</label>
              <input type="time" value={bulkEnd} onChange={(e) => setBulkEnd(e.target.value)} required className={styles.dateInput} />
            </div>
          </div>
          <div className={styles.weekdays}>
            {WEEKDAYS.map((w) => (
              <label key={w.value} className={styles.weekday}>
                <input
                  type="checkbox"
                  checked={bulkWeekdays.includes(w.value)}
                  onChange={() => toggleWeekday(w.value)}
                />
                {w.label}
              </label>
            ))}
          </div>
          <Button type="submit">Создать слоты</Button>
        </form>
      </Section>
    </div>
  );
}

function ReviewsTab({ psychologistId }) {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getReviews({ psychologist: psychologistId })
      .then((res) => {
        const data = extractList(res);
        setReviews(data);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [psychologistId]);

  if (loading) return <Loader />;

  return (
    <div className={styles.tabContent}>
      <h3>Мои отзывы ({reviews.length})</h3>
      {reviews.length === 0 ? (
        <p className={styles.empty}>Отзывов пока нет</p>
      ) : (
        <div className={styles.reviewsList}>
          {reviews.map((r) => (
            <div key={r.id} className={styles.reviewCard}>
              <div className={styles.reviewHeader}>
                <StarRating value={r.rating} size="sm" />
                <strong>{r.client_name}</strong>
              </div>
              <p>{r.text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
