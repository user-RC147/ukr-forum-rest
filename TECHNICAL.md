# Технічна документація — ukr-forum

## Архітектура

Проект побудований як **модульний моноліт** — один проект з незалежними модулями. Кожен модуль має чітко визначену відповідальність і мінімально залежить від інших.

---

## Бекенд

### Архітектурний патерн

Кожен модуль (`apps/<module>/`) має однакову структуру:

```
apps/<module>/
├── models.py       ← структура БД
├── dto.py          ← контракти даних між шарами
├── services/       ← бізнес-логіка
│   ├── __init__.py ← експортує назовні
│   └── *.py
├── serializers.py  ← валідація JSON + перетворення в DTO
├── views.py        ← тонкі view, тільки HTTP
└── urls.py         ← маршрути
```

### Потік даних

```
HTTP запит
    ↓
View (приймає запит)
    ↓
Serializer (валідує JSON → DTO)
    ↓
Service (бізнес-логіка)
    ↓
Model (БД)
    ↓
HTTP відповідь
```

### Модуль `apps/users/`

**Моделі:**
- `CustomUser` — розширений AbstractUser з локацією (через `PrivateLocationMixin`) та полями публічності
- `ConsentText` — тексти згоди на обробку даних

**DTO:**
- `RegisterDTO` — дані реєстрації
- `ProfileUpdateDTO` — дані оновлення профілю
- `PasswordResetConfirmDTO` — підтвердження відновлення паролю
- `ChangePasswordDTO` — зміна паролю
- `LocationUpdateDTO` — оновлення локації

**Сервіси:**
- `auth_service` (клас) — реєстрація, видалення, зміна/відновлення паролю, відправка email
- `profile_service` (функції) — перегляд та оновлення профілю, оновлення локації
- `consent_service` (функції) — надання/відкликання згоди

**API ендпоінти:**

| Метод | URL | Опис | Доступ |
|---|---|---|---|
| POST | `/api/users/register/` | Реєстрація | Всі |
| POST | `/api/users/login/` | Логін (JWT) | Всі |
| POST | `/api/users/token/refresh/` | Оновлення токена | Всі |
| GET | `/api/users/profile/` | Отримати профіль | Авторизовані |
| PATCH | `/api/users/profile/` | Оновити профіль | Авторизовані |
| DELETE | `/api/users/delete/` | Видалити акаунт | Авторизовані |
| POST | `/api/users/change-password/` | Змінити пароль | Авторизовані |
| POST | `/api/users/password-reset/` | Запит відновлення паролю | Всі |
| POST | `/api/users/password-reset/confirm/` | Підтвердження відновлення | Всі |
| POST | `/api/users/location/` | Оновити локацію | Авторизовані |

### Модуль `apps/geo/`

Проксує запити до зовнішнього Geo API (`api.ukrkolo.site`) і зберігає дані в локальну БД.

**Моделі:** `Country`, `Region`, `City`

**Сервіси:**
- `geo_service` (клас) — запити до зовнішнього API
- `geo_db_service` (функції) — збереження в локальну БД через `get_or_create`

**API ендпоінти:**

| Метод | URL | Опис | Доступ |
|---|---|---|---|
| GET | `/api/geo/countries/` | Список країн | Всі |
| GET | `/api/geo/regions/?country_code=UA` | Список регіонів | Всі |
| GET | `/api/geo/cities/?region=123` | Список міст | Всі |

### `core/`

Спільні компоненти для всіх модулів:

- `core/mixins/LocationMixin.py` — абстрактний міксин локації (country, region, city як ForeignKey)
- `core/mixins/LocationMixin.py` → `PrivateLocationMixin` — з полями публічності (country_public, region_public, city_public)

### Налаштування

```
config/settings/
├── base.py   ← спільні налаштування
├── dev.py    ← локальна розробка (DEBUG=True, debug toolbar)
└── prod.py   ← продакшен
```

---

## Фронтенд

### Архітектурний патерн

Модульна структура — кожен модуль повністю самостійний:

```
src/
├── api/
│   └── axios.js          ← спільний HTTP клієнт (BaseURL + JWT interceptor)
├── modules/
│   ├── users/
│   │   ├── api/
│   │   │   └── users.js  ← всі запити до /api/users/
│   │   ├── stores/
│   │   │   └── useUserStore.js  ← стан користувача (Pinia)
│   │   └── views/
│   │       ├── LoginView.vue
│   │       ├── RegisterView.vue
│   │       ├── ProfileView.vue
│   │       └── HomeView.vue
│   └── geo/
│       ├── api/
│       │   └── geo.js    ← всі запити до /api/geo/
│       └── views/
│           └── LocationView.vue
├── shared/
│   └── layouts/
│       ├── DefaultLayout.vue  ← для авторизованих (з навігацією)
│       └── AuthLayout.vue     ← для login/register (без меню)
└── router/
    └── index.js
```

### Layouts

**`DefaultLayout`** — для авторизованих сторінок:
- Навігація з меню (Барахолка, Оголошення, Поради, Розповіді)
- Username + кнопка виходу
- Мобільне бургер-меню

**`AuthLayout`** — для сторінок входу/реєстрації:
- Навігація тільки з логотипом
- Кнопки "Увійти" і "Реєстрація"
- Без меню

### Стан (Pinia)

**`useUserStore`:**
```javascript
state: {
    user,           // дані профілю
    accessToken,    // JWT access токен
    refreshToken,   // JWT refresh токен
}

actions:
    login(credentials)   // логін + збереження токенів
    fetchProfile()       // завантаження профілю
    logout()             // очищення стану і токенів
```

### Автентифікація

JWT токени зберігаються в `localStorage`. Axios interceptor автоматично додає токен до кожного запиту:

```javascript
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})
```

### Маршрутизація

```javascript
/ (DefaultLayout)           ← requiresAuth: true
├── /                       ← HomeView
├── /profile                ← ProfileView
├── /geo/location           ← LocationView
├── /shop                   ← ShopView (тимчасово HomeView)
├── /advboard               ← AdvboardView (тимчасово HomeView)
├── /articles               ← ArticlesView (тимчасово HomeView)
└── /stories                ← StoriesView (тимчасово HomeView)

/auth (AuthLayout)          ← requiresAuth: false
├── /auth/login             ← LoginView
└── /auth/register          ← RegisterView
```

### Стилі

```
src/assets/css/
├── style.css      ← Tailwind CSS 4 (@import "tailwindcss")
└── my_style.css   ← кастомні стилі (.app-bg — фонове зображення)
```

---

## Як додати новий модуль

### Бекенд

1. Створити папку `apps/<module>/` зі стандартною структурою
2. Додати один рядок в `config/settings/base.py`:
```python
INSTALLED_APPS += ['apps.<module>']
```
3. Додати один рядок в `config/urls.py`:
```python
path('api/<module>/', include('apps.<module>.urls'))
```
4. Створити міграції: `python manage.py makemigrations`

### Фронтенд

1. Створити папку `src/modules/<module>/` з підпапками `api/`, `stores/`, `views/`
2. Додати маршрути в `src/router/index.js`

### Спільні файли яких торкаються при додаванні модуля

| Файл | Зміна |
|---|---|
| `config/settings/base.py` | 1 рядок в INSTALLED_APPS |
| `config/urls.py` | 1 рядок path() |
| `src/router/index.js` | 1 блок маршрутів |

---

## Заплановані модулі

| Модуль | Опис | Статус |
|---|---|---|
| `users` | Користувачі, профіль, авторизація | ✅ Готово |
| `geo` | Країни, регіони, міста | ✅ Готово |
| `articles` | Статті та поради | 🔄 В розробці |
| `advboard` | Дошка оголошень | 🔄 В розробці |
| `comments` | Коментарі | 🔄 В розробці |
| `reactions` | Лайки/дизлайки | 🔄 В розробці |
| `shop` | Барахолка | 🔄 В розробці |
| `moderation` | Модерація контенту | 🔄 В розробці |
| `stories` | Розповіді та досвід | 🔄 В розробці |
