# apps/users/services/consent_service.py
from django.utils import timezone

from apps.users.models import CustomUser, ConsentText


def give_consent(user: CustomUser) -> CustomUser:
    """
    Фіксує що користувач дав згоду на обробку даних.
    Записує дату і актуальну версію тексту згоди.
    """
    # беремо найновішу версію тексту згоди
    latest_consent = ConsentText.objects.order_by('-created_at').first()

    user.consent_given   = True
    user.consent_date    = timezone.now()
    user.consent_version = latest_consent  # може бути None якщо текстів ще немає
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