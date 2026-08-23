from django.utils import timezone
from apps.users.selectors.user_selector import UserSelector
from apps.users.repositories.user_repository import UserRepo



class PasswordResetService:
    

    def __init__(self):
        self._selector = UserSelector()
        self._repository = UserRepo()


    def confirm_password_reset(self, token: str, new_password: str) -> None:
        token_obj = self._selector.get_password_reset_token(token)

        if token_obj is None:
            raise ValueError("Токен недійсний")

        if token_obj.is_used:
            raise ValueError("Токен уже використаний")

        if token_obj.expires_at < timezone.now():
            raise ValueError("Токен протух")

        self._repository.confirm_password_reset(token_obj, new_password)

    def request_password_reset(self, email: str) -> None:
        user_id = self._selector.find_by_email(email)

        if user_id is None:
            return

        self._repository.create_password_reset_token(user_id)
        # TODO: EmailService.send_password_reset(email, token) — заглушка, реалізація пізніше


    