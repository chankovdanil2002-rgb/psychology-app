# CLAUDE.md — Контекст проекта «Сайт для записи на беседу с психологом»

## Обзор проекта

Веб-приложение для записи на консультацию с психологом. Клиенты выбирают специализацию, затем психолога, затем свободное время — и записываются на приём. Психологи управляют своим расписанием и подтверждают записи. Администратор верифицирует психологов.

Курсовая работа по дисциплине «Технологии программирования» (СФУ). Целевая оценка — «5».

## Технологический стек

* **Backend:** Python 3.12+, Django 5.x, Django REST Framework
* **Frontend:** React 18+ (отдельное SPA-приложение), Axios для API-запросов
* **СУБД:** PostgreSQL 16+
* **Стилизация:** CSS-модули или Tailwind CSS, адаптивный дизайн (media queries)
* **Аутентификация:** JWT (djangorestframework-simplejwt)
* **Email:** django.core.mail, подтверждение регистрации через токен (синхронно)
* **Кэширование:** Django cache framework (LocMemCache в dev, Redis в prod)

## Структура репозитория

```
psychology-app/
├── backend/
│   ├── config/                 # Настройки Django-проекта
│   │   ├── settings/
│   │   │   ├── base.py         # Общие настройки
│   │   │   ├── dev.py          # Настройки для разработки (DEBUG=True)
│   │   │   └── prod.py         # Продакшн-настройки
│   │   ├── urls.py             # Корневой URL-конфигурация
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/
│   │   ├── users/              # Пользователи, аутентификация, токены
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py  # Кастомные права доступа
│   │   │   ├── signals.py      # Создание профилей при регистрации
│   │   │   └── tasks.py        # Вспомогательные функции отправки email
│   │   ├── clients/            # Профили клиентов
│   │   ├── psychologists/      # Профили психологов, верификация
│   │   ├── specializations/    # Справочник специализаций
│   │   ├── schedule/           # Тайм-слоты, расписание
│   │   ├── appointments/       # Записи на приём
│   │   └── reviews/            # Отзывы
│   ├── manage.py
│   ├── requirements.txt
│   └── fixtures/               # Начальные данные (≥15 записей на таблицу)
│       ├── specializations.json
│       └── test\_data.json
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/                # Axios-инстанс, API-функции
│   │   ├── components/         # Переиспользуемые компоненты
│   │   │   ├── ui/             # Кнопки, инпуты, модалки, рейтинг-звёзды
│   │   │   ├── layout/         # Header, Footer, Sidebar
│   │   │   └── forms/          # Формы регистрации, профиля, отзыва
│   │   ├── pages/              # Страницы приложения
│   │   │   ├── Home/
│   │   │   ├── Auth/           # Login, Register, EmailConfirm
│   │   │   ├── Profile/        # Личный кабинет (клиент/психолог)
│   │   │   ├── Catalog/        # Каталог психологов
│   │   │   ├── Booking/        # Wizard записи на приём
│   │   │   ├── Dashboard/      # Панель психолога (слоты, записи)
│   │   │   └── Admin/          # Верификация психологов
│   │   ├── hooks/              # Кастомные React-хуки
│   │   ├── context/            # AuthContext, NotificationContext
│   │   ├── utils/              # Хелперы, константы
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── package.json
│   └── vite.config.js          # Или аналогичный конфиг сборщика
├── docker-compose.yml          # PostgreSQL, Redis, backend, frontend
├── create\_database.sql         # SQL-скрипт создания БД
├── CLAUDE.md                   # Этот файл
└── README.md
```

## База данных — 10 таблиц

### Основные таблицы

1. **users** — расширенная модель пользователя (email как логин, role: client/psychologist/admin, is\_active)
2. **client\_profiles** — профиль клиента (OneToOne → users; имя, телефон, дата рождения, аватар, is\_profile\_complete)
3. **psychologist\_profiles** — профиль психолога (OneToOne → users; ФИО, скан диплома при регистрации; после верификации: телефон, фото, опыт, био, цена, is\_verified, is\_profile\_complete)
4. **specializations** — справочник специализаций (name, slug, description)
5. **psychologist\_specializations** — связь M2M: психолог ↔ специализация (is\_primary)
6. **time\_slots** — расписание психолога (date, start\_time, end\_time, is\_available)
7. **appointments** — записи на приём (client, psychologist, time\_slot; статусы: pending → confirmed → completed / rejected / cancelled)
8. **reviews** — отзывы (OneToOne → appointment; rating 1–5, text)

### Вспомогательные таблицы

9. **email\_confirmation\_tokens** — токены подтверждения email (token, is\_used, expires\_at)

### Связи между таблицами

```
users 1──1 client\_profiles
users 1──1 psychologist\_profiles
psychologist\_profiles M──M specializations  (через psychologist\_specializations)
psychologist\_profiles 1──N time\_slots
client\_profiles 1──N appointments
psychologist\_profiles 1──N appointments
time\_slots 1──1 appointments
appointments 1──1 reviews
users 1──N email\_confirmation\_tokens
```

## Бизнес-логика — пошаговый процесс

### Регистрация клиента

1. Клиент заполняет: email, пароль, подтверждение пароля
2. Создаётся User (is\_active=False, role='client') + пустой ClientProfile
3. Отправляется email с токеном подтверждения
4. Клиент переходит по ссылке → is\_active=True

### Регистрация психолога

1. Психолог заполняет: email, пароль, ФИО, загрузка скана диплома
2. Создаётся User (is\_active=False, role='psychologist') + PsychologistProfile с документом
3. Подтверждение email → is\_active=True, но is\_verified=False
4. Психолог видит страницу «Ваша заявка на рассмотрении»

### Верификация психолога (админ)

1. Админ видит список неверифицированных психологов
2. Просматривает загруженный документ об образовании
3. Нажимает «Подтвердить» → is\_verified=True, verified\_at=now()
4. Психологу отправляется email-уведомление

### Заполнение профиля

* **Клиент (после первого входа):** имя, фамилия, телефон, дата рождения, аватар → is\_profile\_complete=True → доступ к каталогу и записи
* **Психолог (после верификации):** телефон, фото, опыт, образование, био, цена, специализации → is\_profile\_complete=True → профиль виден в каталоге

### Запись на приём (wizard из 4 шагов)

1. **Выбор специализации** — карточки специализаций
2. **Выбор психолога** — список с фильтрацией, поиском по имени, сортировкой по рейтингу/цене
3. **Выбор времени** — календарь со свободными слотами
4. **Подтверждение** — сводка + комментарий → Appointment(status='pending'), TimeSlot(is\_available=False)

### Подтверждение записи (психолог)

* Список входящих записей (status='pending')
* «Подтвердить» → status='confirmed'
* «Отклонить» → status='rejected', TimeSlot(is\_available=True)
* Клиенту отправляется уведомление

### Завершение приёма

1. Психолог отмечает приём как завершённый → status='completed'
2. Клиенту отправляется уведомление с просьбой оставить отзыв (review\_requested=True)
3. Клиент заполняет форму отзыва: рейтинг (звёзды), текст

## Группы пользователей и права доступа

### Незарегистрированный пользователь

* Просмотр главной страницы
* Просмотр каталога психологов (без возможности записи)
* Регистрация / вход

### Клиент (профиль не заполнен)

* Заполнение профиля
* Просмотр каталога (без записи)

### Клиент (профиль заполнен)

* Запись на приём (wizard)
* Просмотр своих записей и их статусов
* Отмена записи (если status='pending' или 'confirmed')
* Оставление отзыва (если status='completed')
* Редактирование профиля

### Психолог (не верифицирован)

* Просмотр страницы ожидания верификации
* Редактирование ФИО и документа

### Психолог (верифицирован, профиль заполнен)

* Управление расписанием (CRUD тайм-слотов, массовое создание)
* Просмотр входящих записей, подтверждение/отклонение
* Отметка приёма как завершённого
* Просмотр своих отзывов
* Редактирование профиля

### Администратор

* Верификация психологов
* Управление справочником специализаций
* Модерация отзывов
* Доступ к Django Admin

## API Endpoints (REST)

### Аутентификация

```
POST   /api/auth/register/client/          — Регистрация клиента
POST   /api/auth/register/psychologist/    — Регистрация психолога
POST   /api/auth/login/                    — Вход (получение JWT)
POST   /api/auth/token/refresh/            — Обновление JWT
GET    /api/auth/confirm-email/<token>/    — Подтверждение email
POST   /api/auth/password-reset/           — Сброс пароля
```

### Профили

```
GET    /api/profile/me/                    — Получить свой профиль
PUT    /api/profile/me/                    — Обновить профиль
PATCH  /api/profile/me/                    — Частичное обновление
```

### Специализации

```
GET    /api/specializations/               — Список всех специализаций
GET    /api/specializations/<slug>/        — Детали специализации
```

### Психологи (каталог)

```
GET    /api/psychologists/                 — Список (фильтрация по специализации, поиск, пагинация)
GET    /api/psychologists/<id>/            — Детали психолога с отзывами и рейтингом
```

### Расписание

```
GET    /api/schedule/slots/?psychologist=<id>\&date=<date>  — Свободные слоты
POST   /api/schedule/slots/                — Создать слот (только психолог)
POST   /api/schedule/slots/bulk/           — Массовое создание слотов
DELETE /api/schedule/slots/<id>/           — Удалить слот
```

### Записи

```
POST   /api/appointments/                  — Создать запись (клиент)
GET    /api/appointments/                  — Мои записи (клиент или психолог)
PATCH  /api/appointments/<id>/confirm/     — Подтвердить (психолог)
PATCH  /api/appointments/<id>/reject/      — Отклонить (психолог)
PATCH  /api/appointments/<id>/complete/    — Завершить (психолог)
PATCH  /api/appointments/<id>/cancel/      — Отменить (клиент)
```

### Отзывы

```
POST   /api/reviews/                       — Создать отзыв (клиент, только для completed)
GET    /api/reviews/?psychologist=<id>     — Отзывы о психологе
```

### Уведомления

### Админ

```
GET    /api/admin/unverified/              — Неверифицированные психологи
PATCH  /api/admin/verify/<id>/             — Верифицировать психолога
```

## Правила кодирования

### Backend (Django)

* Кастомная модель User наследуется от AbstractBaseUser + PermissionsMixin
* Менеджер пользователей — кастомный UserManager (email вместо username)
* Профили создаются через Django signals (post\_save на User)
* Сериализаторы — отдельные для создания и чтения (CreateSerializer / DetailSerializer)
* Пагинация — PageNumberPagination, по 12 элементов
* Фильтрация — django-filter, поиск — SearchFilter
* Права доступа — кастомные permission-классы в permissions.py
* Загрузка файлов — в MEDIA\_ROOT, отдача через MEDIA\_URL
* Email — синхронная отправка через `send_mail()` (tasks.py)
* Все ответы API — в едином формате: { "status": "success/error", "data": {...}, "message": "..." }
* Обработка ошибок — кастомный exception handler
* Настройки БД — PostgreSQL через dj-database-url или прямая конфигурация

### Frontend (React)

* Роутинг — react-router-dom v6
* Состояние авторизации — React Context (AuthProvider)
* API-запросы — через централизованный Axios-инстанс с interceptor для JWT
* Защищённые маршруты — компонент ProtectedRoute с проверкой роли и статуса профиля
* Формы — controlled components, валидация на клиенте перед отправкой
* Рейтинг-звёзды — кастомный компонент на JS (критерий «элементы на javascript»)
* Адаптивный дизайн — mobile-first, breakpoints: 480px, 768px, 1024px, 1280px
* Пагинация — компонент Pagination с номерами страниц
* Фильтрация и поиск — параметры в URL (query string), debounce на поиске

### Общее

* Весь код и комментарии — на английском языке
* Интерфейс пользователя — на русском языке
* Docker Compose для локального запуска (PostgreSQL, Redis, backend, frontend)
* Переменные окружения — через .env файл (не коммитить в репозиторий)
* Фикстуры — не менее 15 записей в каждой таблице

## Критерии оценки «5» — чек-лист

* \[ ] ≥ 5 таблиц в БД → 10 таблиц
* \[ ] PostgreSQL → да
* \[ ] 2+ группы авторизованных пользователей → клиент, психолог, админ
* \[ ] Подтверждение регистрации через email (токен) → да
* \[ ] Расширение базовой модели пользователя → ClientProfile, PsychologistProfile
* \[ ] Фильтрация по тегам/группам → по специализациям
* \[ ] Поиск по записям → по имени и описанию психолога
* \[ ] Cookie \& Cache → кэширование каталога, JWT в cookie/localStorage
* \[ ] JavaScript элементы → React SPA, рейтинг-звёзды, wizard записи, динамические фильтры
* \[ ] Шаблонизация → компоненты React (аналог Django templates)
* \[ ] Адаптивный дизайн → CSS media queries, mobile-first
* \[ ] Формы вне админки → регистрация, профиль, тайм-слоты, запись, отзыв
* \[ ] Личный кабинет с редактированием → да (клиент и психолог)
* \[ ] ≥ 15 записей в каждой таблице → фикстуры
* \[ ] Пагинация → на каталоге психологов, отзывах, записях
* \[ ] Асинхронность (доп.) → не реализовано (необязательный критерий)
* \[ ] Архитектура MVT → Django views/serializers + React (фронтенд отделён)
* \[ ] ООП → модели, сериализаторы, views как классы (APIView / ViewSet)

## Команды для разработки

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/specializations.json
python manage.py createsuperuser
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev

# Docker
docker-compose up --build
```

## Важные ограничения

* Отзыв можно оставить ТОЛЬКО для записей со статусом 'completed'
* Запись на приём доступна ТОЛЬКО клиентам с is\_profile\_complete=True
* Психолог виден в каталоге ТОЛЬКО при is\_verified=True и is\_profile\_complete=True
* При отклонении записи (rejected) — тайм-слот автоматически возвращается в is\_available=True
* Один тайм-слот — одна запись (OneToOne)
* Один отзыв на одну запись (OneToOne)
* Удаление тайм-слота с привязанной записью запрещено (ON DELETE RESTRICT)

