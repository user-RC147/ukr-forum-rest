# Модуль `users` — Архітектурна специфікація

Статус: узгоджено, готово до реалізації.
Стек: Django + DRF + PostgreSQL, Modular Monolith + Clean Architecture.

---

## 1. Auth: JWT в HttpOnly Cookie

**Рішення:** JWT access + refresh, обидва в HttpOnly cookies (не localStorage, не пам'ять фронту).

- `access_token` — короткий термін (~15 хв), звичайний `path`.
- `refresh_token` — довгий термін (~14 днів), вузький `path` (наприклад `/api/users/token/refresh/`), щоб не літав з кожним запитом.
- Фронт нічого не читає і нічого не підставляє вручну — `withCredentials: true`, все інше на бекенді.

### Refresh Token Rotation + Blacklist

- Кожен виклик `refresh` видає **нову пару** токенів і одразу заносить старий `refresh_token` у блекліст (по `jti`).
- **Reuse detection:** повторне використання вже списаного `refresh_token` → розлогін усіх сесій юзера (сигнал компрометації).
- Access-токени в блекліст не потрапляють (інакше втрачається сенс stateless JWT).

**Модель `BlacklistedToken`:**
| Поле | Тип | Примітка |
|---|---|---|
| `jti` | унікальний ID токена з payload | не сам токен цілком |
| `expires_at` | дата | для майбутньої чистки |

- Сховище: **PostgreSQL зараз**, з можливим переходом на Redis пізніше (заміна лише в Repository/Selector, вище нічого не міняється).
- **Чистка застарілих записів — відкладено** (технічний борг, реалізується разом із переходом на Redis або окремо, через management command).

### Axios-interceptor (фронт)

- 401 на будь-якому запиті → автоматичний виклик `refresh` → повтор оригінального запиту.
- Якщо `refresh` теж падає (401) → розлогін через `useUserStore` (як зараз).

---

## 2. Geo location

- **Окремий модуль `geo`**, дороблятиметься **після** завершення `users`.
- `users` не має FK на `geo`-моделі — зберігає лише сирі `id` (`country_id`, `region_id`, `city_id`) через `LocationMixin`/`PrivateLocationMixin` (вже існує, без змін).
- `geo` — проксі/кеш над зовнішнім API локацій: при реєстрації/редагуванні профілю юзер звертається до `geo`, той або віддає вже наявні дані, або підтягує з зовнішнього API і зберігає в себе.
- Коли `users` потрібні назви локацій (не тільки `id`) — звернення відбувається через **Protocol (в `users`) → Contract (реалізація в `geo`)**, а не прямий імпорт моделі.
- Зараз у `users` фіксуємо тільки контракт-намір; сама реалізація Contract'а — після доопрацювання `geo`.

---

## 3. Модель `CustomUser` — зміни

### Прибрано
- `age` (замінено, див. нижче)
- `visibility` (JSONField) — дублював явні `*_public` прапорці, ідея не мала чіткого застосування, видалено
- Методи `get_public_*()` — бізнес-логіка в Model заборонена; переносяться в Selector/Service при побудові `PublicProfileOutDTO`

### Додано
| Поле | Тип | Примітка |
|---|---|---|
| `date_of_birth` | `DateField(null=True, blank=True)` | замість `age`; вік рахується "на льоту" в Selector/Service, не зберігається |
| `date_of_birth_public` | `BooleanField(default=False)` | приватність, як і в інших персональних полів |
| `is_email_verified` | `BooleanField(default=False)` | див. розділ 5 |
| `deletion_scheduled_at` | `DateTimeField(null=True, blank=True)` | див. розділ 7 (soft/hard delete) |

### Без змін
`username`, `display_name`, `first_name_public`, `last_name_public`, `phone_number`+`phone_public`, `social_network`+`social_public`, `email_public`, `consent_given`, `consent_date`, `consent_version`, `is_banned`, `is_active` (стандартне поле з `AbstractUser`, перевикористовується для soft-delete — див. розділ 7).

`ConsentText` — без змін.

**Референс на реферальний код НЕ зберігається полями в `CustomUser`** (`referral_code`/`referred_by` не додаються) — весь зв'язок реалізований через окремі моделі `ReferralCode`/`ReferralUsage` (розділ 4).

---

## 4. Реферальна система

### Модель `ReferralCode`

| Поле | Тип / джерело | Хто змінює |
|---|---|---|
| `owner` | FK → CustomUser | автоматично (`request.user`) |
| `code` | `UUIDField`, unique, `uuid4()` (варіант А — просто випадковий рядок, без кодування-декодування) | автоматично, Service |
| `created_at` | `auto_now_add=True` | автоматично |
| `expires_at` | `created_at + 7 днів` при create (дефолт) | адмін (може продовжити через `update`) |
| `is_active` | `default=True` | юзер: тільки `True → False`; адмін: обидва напрямки |
| `max_uses` | `1` або `null` (без обмежень) — інші значення заборонені валідацією Serializer | юзер, тільки при `create` |
| `used_count` | `default=0` | автоматично, Service інкрементує при кожному `ReferralUsage` |

### Модель `ReferralUsage`

| Поле | Тип | Примітка |
|---|---|---|
| `code` | FK → ReferralCode | яким кодом скористались |
| `used_by` | FK → CustomUser, `unique=True` | один юзер = один запис (реєстрація одна) |
| `used_at` | `auto_now_add=True` | коли |

### Бізнес-правила (Service/Selector)

1. **Створити `ReferralCode` може тільки юзер, у якого вже є `ReferralUsage` (used_by=self)** — тобто сам зареєстрований за кодом або пізніше прив'язав код у профілі. Юзер без жодного `ReferralUsage` не може створювати коди.
2. **Ліміт: до 4 одночасно активних кодів** на юзера. "Активний" = `is_active=True` **і** не протух (`expires_at`) **і** не вичерпаний (`used_count < max_uses`, якщо `max_uses` заданий).
3. **`max_uses`** приймає лише `1` (тільки одна реєстрація) або `null` (необмежено за кількістю, обмежено лише строком дії).
4. **Права на поля:**
   - Юзер: `create` (з дотриманням п.1–3), `is_active: True→False` (тільки своє, тільки вимкнути).
   - Адмін: `is_active` в обидва боки (реактивація — виключно адмін), продовження `expires_at`.
5. **`role owner/viewer`** — не окреме поле в БД, а **похідне значення**, яке обчислюється Selector-функцією `has_referral_usage(user) -> bool` (`EXISTS(ReferralUsage WHERE used_by=user)`):
   - `True` → `owner` (може створювати/редагувати дії, де є власником)
   - `False` → `viewer` (тільки перегляд)
   - Ця сама функція використовується і як gate перед `create` реферального коду (п.1), і при побудові DTO профілю — **не дублюється**.
6. Пізніше (не зараз): адмінська сторінка, що схематично показує дерево використання кодів (`ReferralUsage.owner → used_by → новий owner → ...`) — рекурсивний обхід, окрема Service-функція.

### Потік валідації коду перед реєстрацією

```
GET /users/referral-code/validate/?code=<uuid4>
   → Service через Selector перевіряє: існує? is_active? не протух? used_count < max_uses?
   → повертає DTO { valid: bool, reason: str|None }
```
Повторна перевірка коду відбувається знову при фактичному `POST /users/register/` (стан могло змінитись між відкриттям сторінки і сабмітом).

---

## 5. Верифікація email

**Рішення:** глобальний feature-flag, не per-user вибір.

- `settings.EMAIL_VERIFICATION_REQUIRED` (bool, з можливістю перевизначити через env).
- `CustomUser.is_email_verified` — поле існує завжди, незалежно від флагу.

**Логіка в `RegisterService`:**
```
якщо EMAIL_VERIFICATION_REQUIRED == False:
    is_email_verified = True одразу при create, лист не надсилається
інакше:
    is_email_verified = False при create
    виклик-заглушка EmailService.send_verification(...) — реалізація листа відкладена
```

Сам механізм відправки/підтвердження листа — **реалізується пізніше**, зараз закладається тільки виклик-точка (сигнатура методу `EmailService`).

---

## 6. Відновлення пароля через email

**Рішення:** зараз закладається тільки структура, реалізація листа — пізніше.

### Модель `PasswordResetToken`

| Поле | Тип | Примітка |
|---|---|---|
| `user` | FK → CustomUser | кому належить запит |
| `token` | unique, `uuid4()` | той самий підхід, що й реферальний код |
| `created_at` | `auto_now_add=True` | |
| `expires_at` | `created_at + 5 хв` | фіксована константа `settings.PASSWORD_RESET_TOKEN_TTL_MINUTES = 5`, без адмінського контролю (короткоживучий разовий токен) |
| `is_used` | `default=False` | `True` одразу після зміни пароля (одноразовість) |

### Потік (структура)

```
POST /users/password-reset/request/  (email)
   → Selector: знайти юзера по email
   → Repository: створити PasswordResetToken
   → [ЗАГЛУШКА] EmailService.send_password_reset(...) — пізніше
   → завжди 200, незалежно від того, чи існує email (захист від перебору)

POST /users/password-reset/confirm/  (token, new_password)
   → Selector: token існує? не протух? is_used=False?
   → якщо ок: Repository оновлює пароль, token.is_used=True
   → якщо ні: доменний Exception → 400 (View)
```

---

## 7. Soft-delete / фізичне видалення `CustomUser`

**Рішення:** двоетапний підхід.

**Крок 1 (миттєво, при `DELETE /users/me/`):**
- `is_active = False` (стандартне поле з `AbstractUser`, Django сам враховує його при автентифікації — неактивний юзер не логіниться).
- `deletion_scheduled_at = now() + 30 днів` (дефолт з `settings.py`).
- Жодні поля одразу не затираються (немає сенсу — все одно фізично видаляється на кроці 2).

**Крок 2 (відкладено, майбутня періодична задача):**
- Management command знаходить усіх, де `deletion_scheduled_at <= now()`.
- `Repository.delete()` — фізичне видалення рядка з БД.
- Приєднується до того ж майбутнього механізму чистки, що й `BlacklistedToken`.

**Права:**
- Юзер: ініціює видалення (`DELETE /users/me/`), **не може** сам скасувати.
- Адмін: може змінити `deletion_scheduled_at` (раніше/пізніше), може повернути `is_active = True` (скасувати видалення) — виключне право адміна.

**`is_banned` — окреме, незалежне поле**, не плутати з `is_active`:
| Поле | Хто ставить | Сенс |
|---|---|---|
| `is_banned` | адмін (модерація) | покарання за порушення правил |
| `is_active` | Service (self-delete) / адмін | акаунт видалено/деактивовано |

Забанені юзери **лишаються видимими** в списку/каталозі (`is_banned: bool` присутнє в `PublicProfileOutDTO`), фронт сам вирішує візуальне позначення.

---

## 8. Профіль: DTO та ендпоінти

### Два DTO для читання

| DTO | Хто бачить | Вміст |
|---|---|---|
| `PrivateProfileOutDTO` | тільки власник | усі поля без фільтрації |
| `PublicProfileOutDTO` | будь-хто | **фіксована структура завжди** (усі ключі присутні); поле, де відповідний `*_public=False` → значення `null` (не відсутність ключа) |

Обидва будуються через **один Selector** (`get_user_by_id`), різниця лише в DTO-білдері поверх (з фільтрацією чи без).

### Ендпоінти CustomUser

| Ендпоінт | Призначення | DTO / примітка |
|---|---|---|
| `POST /users/register/` | реєстрація (= `create`) | реф. код (опціонально), email-verification флаг |
| `GET /users/me/` | свій профіль | `PrivateProfileOutDTO` |
| `PATCH /users/me/` | редагування свого профілю | без `is_banned`, `is_email_verified`, `deletion_scheduled_at` |
| `DELETE /users/me/` | soft-delete (крок 1) | див. розділ 7 |
| `GET /users/<id>/` | чужий профіль | `PublicProfileOutDTO` |
| `GET /users/` | каталог/список | `PublicProfileOutDTO[]`, пагінація, **без пошуку/фільтрів (поки що)** |

### Ендпоінти ReferralCode

| Ендпоінт | Хто | Дозволені дії |
|---|---|---|
| `POST /users/referral-code/` | юзер (з `has_referral_usage=True`) | `create` (з лімітом 4, `max_uses` ∈ {1, null}) |
| `PATCH /users/referral-code/<id>/` (юзер) | юзер | тільки `is_active: True→False`, тільки своє |
| `PATCH /admin/referral-code/<id>/` | адмін | `is_active` (обидва боки), `expires_at` (продовження) |
| `GET /users/referral-code/validate/?code=` | будь-хто (перед реєстрацією) | перевірка валідності |

### Ендпоінти Password Reset

| Ендпоінт | Призначення |
|---|---|
| `POST /users/password-reset/request/` | ініціація (структура готова, лист — пізніше) |
| `POST /users/password-reset/confirm/` | підтвердження + зміна пароля |

---

## 9. Технічний борг (відкладено свідомо)

- Чистка `BlacklistedToken` (протухлі `jti`) — періодична задача.
- Фізичне видалення юзерів за `deletion_scheduled_at` — періодична задача (той самий механізм, що й вище).
- Реалізація відправки email (верифікація + password reset) — `EmailService`, зараз тільки виклики-заглушки.
- Contract `geo` для отримання назв локацій по `id` — після доопрацювання модуля `geo`.
- Адмінська сторінка дерева використання реферальних кодів.
- Пошук/фільтрація в каталозі юзерів (`GET /users/`).