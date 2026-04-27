import { useEffect, useState } from 'react';
import { createAdminPsychologist, deleteAdminPsychologist, getAdminPsychologists } from '../../api';
import Alert from '../../components/ui/Alert';
import Button from '../../components/ui/Button';
import Input from '../../components/ui/Input';
import Loader from '../../components/ui/Loader';
import { formatDate } from '../../utils/helpers';
import styles from './AdminVerificationPage.module.css';

export default function AdminVerificationPage() {
  const [psychologists, setPsychologists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [creating, setCreating] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});
  const [form, setForm] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    patronymic: '',
  });

  const fetchPsychologists = () => {
    setLoading(true);
    getAdminPsychologists()
      .then((res) => {
        const payload = res.data?.data || res.data || {};
        const list = payload.results || (Array.isArray(payload) ? payload : []);
        setPsychologists(list);
      })
      .catch(() => setError('Не удалось загрузить список психологов'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchPsychologists();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (fieldErrors[name]) {
      setFieldErrors((prev) => ({ ...prev, [name]: '' }));
    }
    if (error) setError('');
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setCreating(true);
    setError('');
    setSuccess('');
    setFieldErrors({});

    try {
      await createAdminPsychologist(form);
      setSuccess(
        `Аккаунт психолога ${form.last_name} ${form.first_name} успешно создан`
      );
      setForm({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        patronymic: '',
      });
      fetchPsychologists();
    } catch (err) {
      const resp = err.response?.data;
      const nextErrors = {};

      if (resp?.data && typeof resp.data === 'object') {
        for (const [key, value] of Object.entries(resp.data)) {
          if (Array.isArray(value)) {
            nextErrors[key] = value.join(' ');
          } else if (typeof value === 'string') {
            nextErrors[key] = value;
          }
        }
      }

      setFieldErrors(nextErrors);
      setError(resp?.message || 'Не удалось создать аккаунт психолога');
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (p) => {
    if (!confirm(`Удалить психолога «${p.full_name}»? Это действие необратимо.`)) return;
    setDeletingId(p.id);
    setError('');
    setSuccess('');
    try {
      await deleteAdminPsychologist(p.id);
      setSuccess(`Психолог «${p.full_name}» удалён.`);
      fetchPsychologists();
    } catch (err) {
      setError(err.response?.data?.message || 'Не удалось удалить психолога');
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className={styles.page}>
      <h1>Управление командой психологов</h1>

      {error && <Alert variant="error" onClose={() => setError('')}>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')}>{success}</Alert>}

      <section className={styles.createSection}>
        <h2>Добавить психолога</h2>
        <p className={styles.sectionText}>
          Администратор создаёт учётную запись специалиста. После входа
          психолог сможет заполнить профиль и начать принимать записи клиентов.
        </p>

        <form className={styles.form} onSubmit={handleCreate}>
          <div className={styles.formGrid}>
            <Input
              label="Фамилия"
              name="last_name"
              value={form.last_name}
              onChange={handleChange}
              error={fieldErrors.last_name}
            />
            <Input
              label="Имя"
              name="first_name"
              value={form.first_name}
              onChange={handleChange}
              error={fieldErrors.first_name}
            />
            <Input
              label="Отчество"
              name="patronymic"
              value={form.patronymic}
              onChange={handleChange}
              error={fieldErrors.patronymic}
            />
            <Input
              label="Email"
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              error={fieldErrors.email}
            />
            <Input
              label="Пароль"
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              error={fieldErrors.password}
            />
          </div>

          <div className={styles.formActions}>
            <Button type="submit" loading={creating}>
              Создать аккаунт
            </Button>
          </div>
        </form>
      </section>

      {psychologists.length === 0 ? (
        <div className={styles.emptyState}>
          <p>Пока нет добавленных психологов</p>
        </div>
      ) : (
        <>
          <div className={styles.table}>
            <div className={styles.tableHeader}>
              <span>ФИО</span>
              <span>Email</span>
              <span>Добавлен</span>
              <span>Профиль</span>
              <span>Статус</span>
              <span></span>
            </div>
            {psychologists.map((p) => (
              <div key={p.id} className={styles.tableRow}>
                <span className={styles.name}>{p.full_name}</span>
                <span>{p.email}</span>
                <span>{formatDate(p.date_joined)}</span>
                <span>{p.is_profile_complete ? 'Заполнен' : 'Нужно заполнить'}</span>
                <span>{p.is_active ? 'Активен' : 'Неактивен'}</span>
                <span>
                  <Button
                    variant="danger"
                    size="sm"
                    loading={deletingId === p.id}
                    onClick={() => handleDelete(p)}
                  >
                    Удалить
                  </Button>
                </span>
              </div>
            ))}
          </div>

          <div className={styles.cards}>
            {psychologists.map((p) => (
              <div key={p.id} className={styles.card}>
                <h3>{p.full_name}</h3>
                <p>{p.email}</p>
                <p className={styles.meta}>Добавлен: {formatDate(p.date_joined)}</p>
                <p className={styles.meta}>
                  Профиль: {p.is_profile_complete ? 'заполнен' : 'нужно заполнить'}
                </p>
                <p className={styles.meta}>
                  Статус: {p.is_active ? 'активен' : 'неактивен'}
                </p>
                <Button
                  variant="danger"
                  size="sm"
                  loading={deletingId === p.id}
                  onClick={() => handleDelete(p)}
                  fullWidth
                >
                  Удалить
                </Button>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
