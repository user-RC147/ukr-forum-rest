from django.utils import timezone
from apps.users.models.email_confirmation_token import EmailConfirmationToken
from apps.users.dto.user_dto import EmailConfirmationTokenOutDTO


class EmailConfirmationTokenSelector:

    def get_valid_token(self,token: str) -> EmailConfirmationTokenOutDTO | None:
        try:
            record = EmailConfirmationToken.objects.get(
                token=token,
                is_used=False,
                expires_at__gt=timezone.now(),
            )
        except EmailConfirmationToken.DoesNotExist:
            return None

        return EmailConfirmationTokenOutDTO(
            id=record.id,
            user_id=record.user_id,
            token=str(record.token),
        )
