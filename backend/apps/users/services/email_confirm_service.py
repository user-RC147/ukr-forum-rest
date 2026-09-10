from apps.users.selectors.email_confirm_selector import EmailConfirmationTokenSelector
from apps.users.repositories.email_confirm_repo import EmailConfirmationTokenRepo


class EmailConfirmationTokenService:

    def __init__(self):
        self._selector = EmailConfirmationTokenSelector()
        self._repository = EmailConfirmationTokenRepo()

    def create_token_for_user(self, user_id: int) -> str:
        dto = self._repository.create_email_confirmation_token(user_id)
        return dto.token

    def confirm_email(self, token: str) -> None:
        dto = self._selector.get_valid_token(token)

        if dto is None:
            raise ValueError("Токен недійсний або протермінований")

        self._repository.confirm_email(dto.user_id, dto.id)