from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, name="send_confirmation_email_task")
def send_confirmation_email_task(self, user_id: int, token: str) -> None:
    from apps.users.models import CustomUser

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return

    confirmation_url = f"{settings.FRONTEND_URL}/auth/confirm-email?token={token}"

    send_mail(
        subject="Підтвердження реєстрації на ukrkolo.site",
        message=f"Для підтвердження акаунта перейдіть за посиланням: {confirmation_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )