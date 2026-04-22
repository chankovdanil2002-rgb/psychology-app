// Подписи статусов записей (русский интерфейс)
export const APPOINTMENT_STATUS = {
  pending: 'Ожидает подтверждения',
  confirmed: 'Подтверждена',
  completed: 'Завершена',
  rejected: 'Отклонена',
  cancelled: 'Отменена',
};

// Цвета статусов записей для UI-бейджей
export const APPOINTMENT_STATUS_COLOR = {
  pending: '#ffc107',
  confirmed: '#28a745',
  completed: '#17a2b8',
  rejected: '#dc3545',
  cancelled: '#6c757d',
};

// Подписи ролей пользователей (русский интерфейс)
export const ROLE_LABELS = {
  client: 'Клиент',
  psychologist: 'Психолог',
  admin: 'Администратор',
};

// Варианты оценки для формы отзыва
export const RATING_OPTIONS = [
  { value: 1, label: 'Ужасно' },
  { value: 2, label: 'Плохо' },
  { value: 3, label: 'Нормально' },
  { value: 4, label: 'Хорошо' },
  { value: 5, label: 'Отлично' },
];

// Типы уведомлений
export const NOTIFICATION_TYPES = {
  appointment_created: 'Новая запись',
  appointment_confirmed: 'Запись подтверждена',
  appointment_rejected: 'Запись отклонена',
  appointment_cancelled: 'Запись отменена',
  appointment_completed: 'Приём завершён',
  review_requested: 'Оставьте отзыв',
  verification_approved: 'Верификация одобрена',
};

// Пагинация
export const PAGE_SIZE = 12;

// Шаги wizard записи на приём
export const BOOKING_STEPS = [
  { key: 'specialization', label: 'Специализация' },
  { key: 'psychologist', label: 'Психолог' },
  { key: 'time', label: 'Время' },
  { key: 'confirm', label: 'Подтверждение' },
];
