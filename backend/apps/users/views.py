from django.shortcuts import render


# Наприклад, у backend/apps/users/views.py
import logging

# logger отримає налаштування з секції 'apps'
logger = logging.getLogger('apps.' + __name__) 
# Або просто:
# logger = logging.getLogger('apps')

logger.debug("Це тільки для розробки")
logger.info("Користувач увійшов в систему")
logger.error("Щось пішло не так", exc_info=True)

