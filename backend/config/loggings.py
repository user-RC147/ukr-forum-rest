from pathlib import Path

# BASE_DIR вказує на папку 'backend'
BASE_DIR = Path(__file__).resolve().parent.parent

# Виходимо на рівень вище від 'backend' у корінь проекту, де лежить папка 'logs'
LOG_DIR = BASE_DIR.parent / 'logs' / 'backend'

# Створюємо папку (parents=True дозволить створити 'logs' та 'backend' одним махом)
LOG_DIR.mkdir(parents=True, exist_ok=True)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'simple': {
            'format': '{levelname}  {asctime}  {module} → {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'detailed': {
            'format': '{levelname}  {asctime}  [{name}.{funcName}:{lineno}] → {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },

    'handlers': {
        # Вивід в термінал (консоль)
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Запис помилок у файл
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'errors.log',
            'formatter': 'detailed',
            'encoding': 'utf-8',
        },
        # (Опціонально) Загальний файл з усіма логами
        # 'general_file': {
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',
        #     'filename': LOG_DIR / 'general.log',
        #     'formatter': 'detailed',
        #     'encoding': 'utf-8',
        # },
    },

    'loggers': {
        # Django сам по собі
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        # Всі твої додатки (рекомендую використовувати цей)
        'apps': {
            'handlers': ['console', 'error_file'],
            'level': 'DEBUG',           # на продакшені можна поставити INFO
            'propagate': False,
        },
    },
}
