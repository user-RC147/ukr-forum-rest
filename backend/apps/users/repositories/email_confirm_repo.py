import uuid
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from apps.users.models.email_confirmation_token import EmailConfirmationToken
from apps.users.models.user import CustomUser
from apps.users.dto.user_dto import EmailConfirmationTokenOutDTO

class EmailConfirmationTokenRepo:

    def create_email_confirmation_token(self, user_id: int) -> EmailConfirmationTokenOutDTO:
        record = EmailConfirmationToken.objects.create(
            user_id=user_id,
            token=uuid.uuid4(),
            expires_at=timezone.now()
            + timedelta(minutes=settings.EMAIL_CONFIRMATION_TOKEN_TTL_MINUTES),
        )

        return EmailConfirmationTokenOutDTO(
            id=record.id,
            user_id=record.user_id,
            token=str(record.token),
        )

    def confirm_email(self, user_id: int, token_id: int) -> None:
        user = CustomUser.objects.get(id=user_id)
        user.is_active = True
        user.save()

        EmailConfirmationToken.objects.filter(id=token_id).update(is_used=True)
