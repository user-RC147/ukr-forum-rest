import token
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str

from apps.users.dto import RegisterDTO,PasswordResetConfirmDTO,ChangePasswordDTO
from apps.users.models import CustomUser
from apps.users.repositories import user_repository
from apps.users.exceptions import InvalidPasswordError, InvalidTokenError



class AuthService:
    """
    Відповідає за все що пов'язано з акаунтом:
    реєстрація, видалення, зміна і відновлення паролю.

    Клас тому що всі методи використовують спільну логіку
    відправки email через _send_email.
    """

    # -------------------------------------------------------
    # Реєстрація
    # -------------------------------------------------------
    def register_user(self, dto: RegisterDTO) -> CustomUser:
        """Створює нового користувача в БД."""
        
        return user_repository.create(dto)

    # -------------------------------------------------------
    # Видалення акаунту
    # -------------------------------------------------------
    def delete_account(self, user: CustomUser) -> None:
        """Повністю видаляє акаунт користувача."""
        user_repository.delete(user)

    # -------------------------------------------------------
    # Зміна паролю (користувач знає старий пароль)
    # -------------------------------------------------------
    def change_password(self, user: CustomUser, dto: ChangePasswordDTO) -> None:
        """
        Змінює пароль якщо старий пароль вірний.
        Викидає ValueError якщо старий пароль невірний.
        """
        if not user.check_password(dto.old_password):  # ← dto.old_password
            raise InvalidPasswordError()

        user.set_password(dto.new_password)  # ← dto.new_password
        user_repository.save(user)

    # -------------------------------------------------------
    # Відновлення паролю — Крок 1: відправляємо email
    # -------------------------------------------------------
    def request_password_reset(self, email: str) -> None:
        """
        Знаходить користувача за email.
        Генерує токен і відправляє посилання.

        Якщо email не знайдено — мовчимо (з міркувань безпеки,
        щоб не розкривати які email зареєстровані).
        """
        user=user_repository.get_by_email(email)
        if not user:
            return
        
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        token=default_token_generator.make_token(user)
        reset_link=f"{settings.FRONTEND_URL}/reset-password/?uid={uid}&token={token}"

        self._send_email(
            to=user.email,
            subject="Відновлення паролю",
            message=f"Для відновлення паролю перейдіть за посиланням:\n\n{reset_link}\n\nПосилання діє 3 дні.",
        )

    # -------------------------------------------------------
    # Відновлення паролю — Крок 2: встановлюємо новий пароль
    # -------------------------------------------------------
    def confirm_password_reset(self, dto: PasswordResetConfirmDTO) -> None:
        """
        Перевіряє uid і token.
        Якщо все вірно — встановлює новий пароль.
        Викидає ValueError якщо токен невалідний або протермінований.
        """
        try:
            uid  = force_str(urlsafe_base64_decode(dto.uid))
            user = user_repository.get_by_pk(uid)
        except (TypeError, ValueError):
            raise InvalidTokenError("Посилання недійсне або протерміноване.")

        if not user:
            raise InvalidTokenError("Невалідне посилання.")

        if not default_token_generator.check_token(user,dto.token):
            raise InvalidTokenError()

        user.set_password(dto.new_password)
        user_repository.save(user)

    # -------------------------------------------------------
    # Приватний метод відправки email
    # -------------------------------------------------------
    def _send_email(self, to: str, subject: str, message: str) -> None:
        """
        _ на початку = приватний метод.
        Викликається тільки всередині класу.
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to],
            fail_silently=False,
        )


# Один екземпляр на весь проект — не створюємо новий об'єкт щоразу
auth_service = AuthService()