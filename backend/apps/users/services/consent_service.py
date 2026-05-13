# apps/users/services/consent_service.py
from django.utils import timezone

from apps.users.models import CustomUser
from apps.users.repositories import consent_repository


def give_consent(user: CustomUser) -> CustomUser:
    """
    Фіксує що користувач дав згоду на обробку даних.
    Записує дату і актуальну версію тексту згоди.
    """
    # беремо найновішу версію тексту згоди
    latest_consent = consent_repository.get_latest()
    user.consent_given =True
    user.consent_date=timezone.now()
    user.consent_version-latest_consent
    user.save()
    return user


def revoke_consent(user: CustomUser) -> CustomUser:
    """
    Відкликає згоду користувача.
    В реальному проекті тут може бути логіка видалення персональних даних
    згідно GDPR.
    """
    user.consent_given   = False
    user.consent_date    = None
    user.consent_version = None
    user.save()
    return user