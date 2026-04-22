/**
 * Форматирует дату (YYYY-MM-DD) в русскую локаль для отображения.
 * @param {string} dateStr - Дата в ISO-формате (например, "2026-04-12")
 * @returns {string} Отформатированная дата (например, "12 апреля 2026")
 */
export function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

/**
 * Форматирует строку времени (HH:MM:SS или HH:MM) для отображения.
 * @param {string} timeStr - Строка времени (например, "14:30:00" или "14:30")
 * @returns {string} Отформатированное время (например, "14:30")
 */
export function formatTime(timeStr) {
  if (!timeStr) return '';
  // Берём только часть HH:MM
  return timeStr.slice(0, 5);
}

/**
 * Форматирует цену в рублях.
 * @param {number|string} price - Значение цены
 * @returns {string} Отформатированная цена (например, "3 500 ₽")
 */
export function formatPrice(price) {
  if (price == null) return '';
  const num = Number(price);
  return num.toLocaleString('ru-RU') + ' \u20BD';
}

/**
 * Обрезает текст до заданной длины, добавляя многоточие.
 * @param {string} text - Исходный текст
 * @param {number} maxLength - Максимальная длина
 * @returns {string} Обрезанный текст
 */
export function truncateText(text, maxLength = 100) {
  if (!text || text.length <= maxLength) return text || '';
  return text.slice(0, maxLength).trimEnd() + '...';
}

/**
 * Получает инициалы из полного имени.
 * @param {string} firstName
 * @param {string} lastName
 * @returns {string} Инициалы (например, "ИФ")
 */
export function getInitials(firstName, lastName) {
  const first = firstName ? firstName.charAt(0).toUpperCase() : '';
  const last = lastName ? lastName.charAt(0).toUpperCase() : '';
  return first + last || '?';
}

/**
 * Формирует query string из объекта параметров (пропускает null/undefined/пустые).
 * @param {Object} params
 * @returns {string} Query string без ведущего "?"
 */
export function buildQueryString(params) {
  const entries = Object.entries(params).filter(
    ([, v]) => v != null && v !== ''
  );
  return new URLSearchParams(entries).toString();
}

/**
 * Извлекает массив из стандартной обёртки API-ответа.
 *
 * Backend оборачивает всё в:
 *   { status, message, data: { count, next, previous, results: [...] } }
 * или иногда:
 *   { status, message, data: [...] }
 *
 * Эта функция надёжно возвращает массив в обоих случаях.
 *
 * @param {Object} res - Axios response
 * @returns {Array} Массив элементов
 */
export function extractList(res) {
  const payload = res.data?.data ?? res.data ?? {};
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload.results)) return payload.results;
  return [];
}

/**
 * Извлекает один объект из стандартной обёртки API-ответа.
 *
 * @param {Object} res - Axios response
 * @returns {Object} Объект данных
 */
export function extractData(res) {
  return res.data?.data ?? res.data ?? {};
}
