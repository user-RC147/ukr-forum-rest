# Коло Українців — ukr-forum

Платформа для об'єднання українців у світі. Дозволяє знаходити земляків, ділитись досвідом, публікувати оголошення та статті.

---

## Технологічний стек

| Частина | Технологія |
|---|---|
| Backend | Django 5 + Django REST Framework |
| Автентифікація | JWT (djangorestframework-simplejwt) |
| Frontend | Vue 3 + Vite |
| Стан | Pinia |
| Стилі | Tailwind CSS 4 |
| База даних | PostgreSQL |
| API документація | drf-spectacular (Swagger) |

---

## Структура проекту

```
ukr-forum/
├── backend/          ← Django бекенд
│   ├── apps/         ← модулі додатку
│   │   ├── users/    ← користувачі
│   │   └── geo/      ← геолокація
│   ├── config/       ← налаштування
│   │   └── settings/
│   │       ├── base.py
│   │       ├── dev.py
│   │       └── prod.py
│   └── core/         ← спільні міксини, пермішени
├── frontend/         ← Vue фронтенд
│   └── src/
│       ├── api/      ← спільний axios
│       ├── modules/  ← модулі
│       │   ├── users/
│       │   └── geo/
│       ├── shared/   ← спільні layouts
│       └── router/   ← маршрути
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
└── logs/
```

---

## Як запустити локально

### 1. Клонувати репозиторій

```bash
git clone <repo-url>
cd ukr-forum
```

### 2. Бекенд

```bash
# Створити віртуальне середовище
python -m venv venvUkrForum
source venvUkrForum/bin/activate  # Linux/Mac
# або
venvUkrForum\Scripts\activate     # Windows

# Встановити залежності
pip install -r requirements/dev.txt

# Створити .env файл
cp backend/.env.example backend/.env
# заповнити змінні (див. нижче)

# Застосувати міграції
cd backend
python manage.py migrate --settings=config.settings.dev

# Створити суперкористувача
python manage.py createsuperuser --settings=config.settings.dev

# Запустити сервер
python manage.py runserver --settings=config.settings.dev
```

### 3. Фронтенд

```bash
cd frontend
npm install
npm run dev
```

### 4. Відкрити в браузері

| URL | Опис |
|---|---|
| `http://localhost:5173` | Vue фронтенд |
| `http://localhost:8000/api/docs/` | Swagger документація |
| `http://localhost:8000/admin/` | Django адмін панель |

---

## Змінні середовища (backend/.env)

```env
SECRET_KEY=your-secret-key

# База даних
DB_NAME=ukr_forum
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Зовнішній Geo API
GEO_API_URL=https://api.ukrkolo.site
GEO_API_TOKEN=your-geo-token

# Email
DEFAULT_FROM_EMAIL=noreply@ukr-forum.com

# Frontend URL (для посилань в email)
FRONTEND_URL=http://localhost:5173
```

---

## Запуск тестів

```bash
cd backend
python manage.py test --settings=config.settings.dev
```
