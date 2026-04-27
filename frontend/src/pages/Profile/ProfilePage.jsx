import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { patchProfile, getSpecializations } from '../../api';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';
import Alert from '../../components/ui/Alert';
import Loader from '../../components/ui/Loader';
import StarRating from '../../components/ui/StarRating';
import FileUpload from '../../components/forms/FileUpload';
import { extractList, formatPrice } from '../../utils/helpers';
import styles from './ProfilePage.module.css';

/** Оставляет только буквы (кириллица + латиница), пробелы и дефисы. */
function onlyLetters(value) {
  return value.replace(/[^a-zA-Zа-яА-ЯёЁ\s-]/g, '');
}

/**
 * Приводит ввод к формату +7XXXXXXXXXX.
 * Всегда сохраняет +7 в начале, принимает только цифры.
 */
function normalizePhone(raw) {
  const digits = raw.replace(/\D/g, '');
  let d = digits;
  if (d.startsWith('8') || d.startsWith('7')) {
    d = '7' + d.slice(1);
  } else {
    d = '7' + d;
  }
  return '+' + d.slice(0, 11);
}

function toDateInputValue(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function getLatestAllowedBirthDate() {
  const date = new Date();
  date.setFullYear(date.getFullYear() - 14);
  return toDateInputValue(date);
}

function formatDate(dateValue) {
  if (!dateValue) return 'Не указана';
  const [year, month, day] = dateValue.split('-');
  return `${day}.${month}.${year}`;
}

function getInitials(user) {
  const first = user.first_name?.trim()?.[0] || '';
  const last = user.last_name?.trim()?.[0] || '';
  return `${first}${last}`.toUpperCase() || 'К';
}

/**
 * Страница профиля — определяет роль пользователя из AuthContext
 * и отрисовывает соответствующую форму (клиент, психолог или
 * экран ожидания верификации).
 */
export default function ProfilePage() {
  const {
    user,
    loading: authLoading,
    isClient,
    isPsychologist,
    isVerified,
    isProfileComplete,
    fetchProfile,
  } = useAuth();

  if (authLoading) return <Loader size="large" />;
  if (!user) return null;

  // Психолог, ещё не прошедший верификацию
  if (isPsychologist && !isVerified) {
    return <PendingVerification user={user} />;
  }

  if (isClient) {
    return (
      <ClientProfileForm
        user={user}
        isProfileComplete={isProfileComplete}
        fetchProfile={fetchProfile}
      />
    );
  }

  if (isPsychologist) {
    return (
      <PsychologistProfileForm
        user={user}
        isProfileComplete={isProfileComplete}
        fetchProfile={fetchProfile}
      />
    );
  }

  // Админ или неизвестная роль
  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>Личный кабинет</h1>
        <p className={styles.infoText}>
          Роль: {user.role}. Email: {user.email}
        </p>
      </div>
    </div>
  );
}

/**
 * Сообщение об ожидании верификации для психологов.
 */
function PendingVerification({ user }) {
  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.pendingIcon}>
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--color-warning)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
        </div>
        <h1 className={styles.title}>Ваша заявка на рассмотрении</h1>
        <p className={styles.infoText}>
          Администратор проверяет ваши документы. Вы получите уведомление,
          когда верификация будет завершена.
        </p>

        {user.diploma_scan && (
          <div className={styles.diplomaPreview}>
            <h3 className={styles.sectionTitle}>Загруженный документ</h3>
            {user.diploma_scan.match(/\.(jpg|jpeg|png|gif|webp)$/i) ? (
              <img
                src={user.diploma_scan}
                alt="Diploma scan"
                className={styles.diplomaImage}
              />
            ) : (
              <a
                href={user.diploma_scan}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.diplomaLink}
              >
                Просмотреть документ
              </a>
            )}
          </div>
        )}

        <Alert variant="info">
          Ваш email: <strong>{user.email}</strong>
        </Alert>
      </div>
    </div>
  );
}

/**
 * Форма профиля клиента.
 */
function ClientProfileView({ user, onEdit }) {
  const fullName = `${user.last_name || ''} ${user.first_name || ''}`.trim();

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>Личный кабинет</h1>

        <div className={styles.profileHeader}>
          {user.avatar ? (
            <img
              src={user.avatar}
              alt="Аватар профиля"
              className={styles.profileAvatar}
            />
          ) : (
            <div className={styles.profileAvatarPlaceholder}>
              {getInitials(user)}
            </div>
          )}
          <div>
            <h2 className={styles.profileName}>{fullName}</h2>
            <p className={styles.profileEmail}>{user.email}</p>
          </div>
        </div>

        <div className={styles.profileDetails}>
          <div className={styles.profileDetail}>
            <span>Телефон</span>
            <strong>{user.phone || 'Не указан'}</strong>
          </div>
          <div className={styles.profileDetail}>
            <span>Дата рождения</span>
            <strong>{formatDate(user.date_of_birth)}</strong>
          </div>
          <div className={styles.profileDetail}>
            <span>Статус профиля</span>
            <strong>Заполнен</strong>
          </div>
        </div>

        <div className={styles.profileActions}>
          <Link to="/catalog" className={styles.catalogLink}>
            Выбрать психолога
          </Link>
          <Button type="button" variant="outline" fullWidth onClick={onEdit}>
            Редактировать профиль
          </Button>
        </div>
      </div>
    </div>
  );
}

function ClientProfileForm({ user, isProfileComplete, fetchProfile }) {
  const latestAllowedBirthDate = getLatestAllowedBirthDate();
  const [isEditing, setIsEditing] = useState(!isProfileComplete);
  const [form, setForm] = useState({
    first_name: user.first_name || '',
    last_name: user.last_name || '',
    phone: user.phone || '+7',
    date_of_birth: user.date_of_birth || '',
  });
  const [avatarFile, setAvatarFile] = useState(null);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isProfileComplete) {
      setIsEditing(false);
    }
  }, [isProfileComplete]);

  if (isProfileComplete && !isEditing) {
    return (
      <ClientProfileView
        user={user}
        onEdit={() => {
          setSuccessMsg('');
          setIsEditing(true);
        }}
      />
    );
  }

  const validate = () => {
    const errs = {};
    if (!form.first_name.trim()) errs.first_name = 'Введите имя';
    if (!form.last_name.trim()) errs.last_name = 'Введите фамилию';
    if (!form.phone || form.phone === '+7') {
      errs.phone = 'Введите номер телефона';
    } else if (!/^\+7\d{10}$/.test(form.phone)) {
      errs.phone = 'Номер должен начинаться с +7 и содержать 11 цифр';
    }
    if (!form.date_of_birth) errs.date_of_birth = 'Укажите дату рождения';
    if (form.date_of_birth && form.date_of_birth > latestAllowedBirthDate) {
      errs.date_of_birth = 'Запись доступна клиентам от 14 лет';
    }
    return errs;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: '' }));
    if (serverError) setServerError('');
    if (successMsg) setSuccessMsg('');
  };

  const handleNameChange = (e) => {
    const { name, value } = e.target;
    const filtered = onlyLetters(value);
    setForm((prev) => ({ ...prev, [name]: filtered }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: '' }));
    if (serverError) setServerError('');
  };

  const handlePhoneChange = (e) => {
    const normalized = normalizePhone(e.target.value);
    setForm((prev) => ({ ...prev, phone: normalized }));
    if (errors.phone) setErrors((prev) => ({ ...prev, phone: '' }));
    if (serverError) setServerError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) {
      setErrors(errs);
      return;
    }

    setLoading(true);
    setServerError('');
    setSuccessMsg('');

    try {
      const formData = new FormData();
      formData.append('first_name', form.first_name);
      formData.append('last_name', form.last_name);
      formData.append('phone', form.phone);
      formData.append('date_of_birth', form.date_of_birth);
      if (avatarFile) {
        formData.append('avatar', avatarFile);
      }

      await patchProfile(formData);
      await fetchProfile();
      setIsEditing(false);
      setSuccessMsg('Профиль успешно сохранён!');
    } catch (err) {
      const data = err.response?.data;
      if (data && typeof data === 'object') {
        const fieldErrors = {};
        for (const [key, val] of Object.entries(data)) {
          if (key === 'message' || key === 'detail') {
            setServerError(Array.isArray(val) ? val.join(' ') : val);
          } else if (Array.isArray(val)) {
            fieldErrors[key] = val.join(' ');
          } else if (typeof val === 'string') {
            fieldErrors[key] = val;
          }
        }
        if (Object.keys(fieldErrors).length) setErrors(fieldErrors);
      }
      if (!serverError) {
        setServerError('Не удалось сохранить профиль. Попробуйте позже.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>Личный кабинет</h1>

        <div className={styles.statusBadge}>
          {isProfileComplete ? (
            <span className={styles.badgeComplete}>Профиль заполнен</span>
          ) : (
            <span className={styles.badgeIncomplete}>Заполните профиль для записи</span>
          )}
        </div>

        {serverError && (
          <Alert variant="error" onClose={() => setServerError('')}>
            {serverError}
          </Alert>
        )}
        {successMsg && (
          <Alert variant="success" onClose={() => setSuccessMsg('')}>
            {successMsg}
          </Alert>
        )}

        <form onSubmit={handleSubmit} className={styles.form} noValidate>
          <div className={styles.row}>
            <Input
              label="Фамилия"
              name="last_name"
              placeholder="Иванов"
              value={form.last_name}
              onChange={handleNameChange}
              error={errors.last_name}
            />
            <Input
              label="Имя"
              name="first_name"
              placeholder="Иван"
              value={form.first_name}
              onChange={handleNameChange}
              error={errors.first_name}
            />
          </div>

          <Input
            label="Телефон"
            type="tel"
            name="phone"
            placeholder="+7XXXXXXXXXX"
            value={form.phone}
            onChange={handlePhoneChange}
            error={errors.phone}
          />

          <Input
            label="Дата рождения"
            type="date"
            name="date_of_birth"
            value={form.date_of_birth}
            onChange={handleChange}
            error={errors.date_of_birth}
            max={latestAllowedBirthDate}
          />

          <FileUpload
            label="Аватар"
            name="avatar"
            accept="image/*"
            onChange={(file) => setAvatarFile(file)}
            currentFile={user.avatar}
            error={errors.avatar}
          />

          <Button type="submit" fullWidth loading={loading}>
            Сохранить профиль
          </Button>
        </form>
      </div>
    </div>
  );
}

/**
 * Режим просмотра профиля психолога.
 */
function PsychologistProfileView({ user, onEdit }) {
  const fullName = [user.last_name, user.first_name, user.patronymic]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={styles.page}>
      <div className={styles.cardWide}>
        <h1 className={styles.title}>Личный кабинет психолога</h1>

        <div className={styles.profileHeader}>
          {user.photo ? (
            <img src={user.photo} alt="Фото профиля" className={styles.profileAvatar} />
          ) : (
            <div className={styles.profileAvatarPlaceholder}>
              {getInitials(user)}
            </div>
          )}
          <div>
            <h2 className={styles.profileName}>{fullName || 'Имя не указано'}</h2>
            <p className={styles.profileEmail}>{user.email}</p>
            {user.average_rating > 0 && (
              <StarRating value={user.average_rating} size="sm" showValue />
            )}
          </div>
        </div>

        <div className={styles.profileDetails}>
          <div className={styles.profileDetail}>
            <span>Телефон</span>
            <strong>{user.phone || 'Не указан'}</strong>
          </div>
          <div className={styles.profileDetail}>
            <span>Стаж работы</span>
            <strong>
              {user.experience_years != null
                ? `${user.experience_years} ${pluralYears(user.experience_years)}`
                : 'Не указан'}
            </strong>
          </div>
          <div className={styles.profileDetail}>
            <span>Стоимость консультации</span>
            <strong>{user.price ? formatPrice(user.price) : 'Не указана'}</strong>
          </div>
          {user.education && (
            <div className={styles.profileDetail}>
              <span>Образование</span>
              <strong>{user.education}</strong>
            </div>
          )}
        </div>

        {user.bio && (
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>О себе</h2>
            <p className={styles.bioText}>{user.bio}</p>
          </div>
        )}

        {user.specializations?.length > 0 && (
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Специализации</h2>
            <div className={styles.specTags}>
              {user.specializations.map((s) => (
                <span
                  key={typeof s === 'object' ? s.id : s}
                  className={styles.specTag}
                >
                  {typeof s === 'object' ? s.name : s}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className={styles.profileActions}>
          <Link to="/dashboard" className={styles.catalogLink}>
            Перейти в панель управления
          </Link>
          <Button type="button" variant="outline" fullWidth onClick={onEdit}>
            Редактировать профиль
          </Button>
        </div>
      </div>
    </div>
  );
}

function pluralYears(n) {
  const abs = Math.abs(n) % 100;
  const mod = abs % 10;
  if (abs > 10 && abs < 20) return 'лет';
  if (mod === 1) return 'год';
  if (mod >= 2 && mod <= 4) return 'года';
  return 'лет';
}

/**
 * Форма профиля психолога (для верифицированных психологов).
 */
function PsychologistProfileForm({ user, isProfileComplete, fetchProfile }) {
  const [isEditing, setIsEditing] = useState(!isProfileComplete);
  const [specializations, setSpecializations] = useState([]);
  const [specLoading, setSpecLoading] = useState(true);

  const [form, setForm] = useState({
    first_name: user.first_name || '',
    last_name: user.last_name || '',
    patronymic: user.patronymic || '',
    phone: user.phone || '+7',
    experience_years: user.experience_years || '',
    education: user.education || '',
    bio: user.bio || '',
    price: user.price || '',
  });
  const [selectedSpecs, setSelectedSpecs] = useState(
    user.specializations?.map((s) => (typeof s === 'object' ? s.id : s)) || []
  );
  const [photoFile, setPhotoFile] = useState(null);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isProfileComplete) setIsEditing(false);
  }, [isProfileComplete]);

  // Загружаем доступные специализации
  useEffect(() => {
    let cancelled = false;
    const fetchSpecs = async () => {
      try {
        const res = await getSpecializations();
        const list = extractList(res);
        if (!cancelled) {
          setSpecializations(list);
        }
      } catch {
        // Тихо игнорируем — специализации просто не отобразятся
      } finally {
        if (!cancelled) setSpecLoading(false);
      }
    };
    fetchSpecs();
    return () => { cancelled = true; };
  }, []);

  const validate = () => {
    const errs = {};
    if (!form.first_name.trim()) errs.first_name = 'Введите имя';
    if (!form.last_name.trim()) errs.last_name = 'Введите фамилию';
    if (!form.phone || form.phone === '+7') {
      errs.phone = 'Введите номер телефона';
    } else if (!/^\+7\d{10}$/.test(form.phone)) {
      errs.phone = 'Номер должен начинаться с +7 и содержать 11 цифр';
    }
    if (!form.experience_years && form.experience_years !== 0) {
      errs.experience_years = 'Укажите стаж';
    }
    if (!form.education.trim()) errs.education = 'Укажите образование';
    if (!form.bio.trim()) errs.bio = 'Расскажите о себе';
    if (!form.price) {
      errs.price = 'Укажите стоимость консультации';
    }
    if (selectedSpecs.length === 0) {
      errs.specializations = 'Выберите хотя бы одну специализацию';
    }
    return errs;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: '' }));
    if (serverError) setServerError('');
    if (successMsg) setSuccessMsg('');
  };

  const handleNameChange = (e) => {
    const { name, value } = e.target;
    const filtered = onlyLetters(value);
    setForm((prev) => ({ ...prev, [name]: filtered }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: '' }));
    if (serverError) setServerError('');
  };

  const handlePhoneChange = (e) => {
    const normalized = normalizePhone(e.target.value);
    setForm((prev) => ({ ...prev, phone: normalized }));
    if (errors.phone) setErrors((prev) => ({ ...prev, phone: '' }));
    if (serverError) setServerError('');
  };

  const handleSpecToggle = (specId) => {
    setSelectedSpecs((prev) =>
      prev.includes(specId)
        ? prev.filter((id) => id !== specId)
        : [...prev, specId]
    );
    if (errors.specializations) {
      setErrors((prev) => ({ ...prev, specializations: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) {
      setErrors(errs);
      return;
    }

    setLoading(true);
    setServerError('');
    setSuccessMsg('');

    try {
      const formData = new FormData();
      formData.append('first_name', form.first_name);
      formData.append('last_name', form.last_name);
      if (form.patronymic.trim()) {
        formData.append('patronymic', form.patronymic);
      }
      formData.append('phone', form.phone);
      formData.append('experience_years', form.experience_years);
      formData.append('education', form.education);
      formData.append('bio', form.bio);
      formData.append('price', form.price);
      if (photoFile) {
        formData.append('photo', photoFile);
      }
      // Отправляем id специализаций
      selectedSpecs.forEach((id) => {
        formData.append('specializations', id);
      });

      await patchProfile(formData);
      await fetchProfile();
      setIsEditing(false);
      setSuccessMsg('Профиль успешно сохранён!');
    } catch (err) {
      const data = err.response?.data;
      if (data && typeof data === 'object') {
        const fieldErrors = {};
        for (const [key, val] of Object.entries(data)) {
          if (key === 'message' || key === 'detail') {
            setServerError(Array.isArray(val) ? val.join(' ') : val);
          } else if (Array.isArray(val)) {
            fieldErrors[key] = val.join(' ');
          } else if (typeof val === 'string') {
            fieldErrors[key] = val;
          }
        }
        if (Object.keys(fieldErrors).length) setErrors(fieldErrors);
      }
      if (!serverError) {
        setServerError('Не удалось сохранить профиль. Попробуйте позже.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Режим просмотра — только если профиль заполнен и не редактируется
  if (isProfileComplete && !isEditing) {
    return (
      <PsychologistProfileView
        user={user}
        onEdit={() => {
          setSuccessMsg('');
          setIsEditing(true);
        }}
      />
    );
  }

  return (
    <div className={styles.page}>
      <div className={styles.cardWide}>
        <h1 className={styles.title}>Личный кабинет психолога</h1>

        <div className={styles.statusBadge}>
          {isProfileComplete ? (
            <span className={styles.badgeComplete}>Профиль заполнен</span>
          ) : (
            <span className={styles.badgeIncomplete}>Заполните профиль, чтобы быть видимым в каталоге</span>
          )}
        </div>

        {serverError && (
          <Alert variant="error" onClose={() => setServerError('')}>
            {serverError}
          </Alert>
        )}
        {successMsg && (
          <Alert variant="success" onClose={() => setSuccessMsg('')}>
            {successMsg}
          </Alert>
        )}

        <form onSubmit={handleSubmit} className={styles.form} noValidate>
          {/* Блок ФИО */}
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Личные данные</h2>
            <div className={styles.row}>
              <Input
                label="Фамилия"
                name="last_name"
                value={form.last_name}
                onChange={handleNameChange}
                error={errors.last_name}
              />
              <Input
                label="Имя"
                name="first_name"
                value={form.first_name}
                onChange={handleNameChange}
                error={errors.first_name}
              />
            </div>
            <Input
              label="Отчество"
              name="patronymic"
              value={form.patronymic}
              onChange={handleNameChange}
              error={errors.patronymic}
            />
            <Input
              label="Телефон"
              type="tel"
              name="phone"
              placeholder="+7XXXXXXXXXX"
              value={form.phone}
              onChange={handlePhoneChange}
              error={errors.phone}
            />
            <FileUpload
              label="Фото профиля"
              name="photo"
              accept="image/*"
              onChange={(file) => setPhotoFile(file)}
              currentFile={user.photo}
              error={errors.photo}
            />
          </div>

          {/* Профессиональный блок */}
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Профессиональная информация</h2>
            <div className={styles.row}>
              <Input
                label="Стаж (лет)"
                type="number"
                name="experience_years"
                min="0"
                value={form.experience_years}
                onChange={handleChange}
                error={errors.experience_years}
              />
              <Input
                label="Стоимость консультации (руб.)"
                type="number"
                name="price"
                min="0"
                value={form.price}
                onChange={handleChange}
                error={errors.price}
              />
            </div>
            <Input
              label="Образование"
              name="education"
              placeholder="МГУ, факультет психологии, 2015"
              value={form.education}
              onChange={handleChange}
              error={errors.education}
            />
            <Input
              label="О себе"
              type="textarea"
              name="bio"
              placeholder="Расскажите о вашем опыте, подходах и методах работы..."
              value={form.bio}
              onChange={handleChange}
              error={errors.bio}
            />
          </div>

          {/* Блок специализаций */}
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Специализации</h2>
            {specLoading ? (
              <Loader size="small" />
            ) : specializations.length === 0 ? (
              <p className={styles.infoText}>Специализации пока не добавлены</p>
            ) : (
              <div className={styles.checkboxGrid}>
                {specializations.map((spec) => (
                  <label key={spec.id} className={styles.checkboxLabel}>
                    <input
                      type="checkbox"
                      checked={selectedSpecs.includes(spec.id)}
                      onChange={() => handleSpecToggle(spec.id)}
                      className={styles.checkbox}
                    />
                    <span className={styles.checkboxText}>{spec.name}</span>
                  </label>
                ))}
              </div>
            )}
            {errors.specializations && (
              <span className={styles.fieldError}>{errors.specializations}</span>
            )}
          </div>

          <Button type="submit" fullWidth loading={loading}>
            Сохранить профиль
          </Button>
          {isProfileComplete && (
            <Button
              type="button"
              variant="outline"
              fullWidth
              onClick={() => setIsEditing(false)}
            >
              Отмена
            </Button>
          )}
        </form>
      </div>
    </div>
  );
}
