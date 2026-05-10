# apps/users/services/auth_service.py
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from apps.users.models import CustomUser
from apps.users.dto import RegisterDTO, PasswordResetConfirmDTO, ChangePasswordDTO  # ← додали ChangePasswordDTO


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
        user = CustomUser.objects.create_user(
            username=dto.username,
            email=dto.email,
            password=dto.password,
            country=dto.country,
            region=dto.region,
            city=dto.city,
        )
        return user

    # -------------------------------------------------------
    # Видалення акаунту
    # -------------------------------------------------------
    def delete_account(self, user: CustomUser) -> None:
        """Повністю видаляє акаунт користувача."""
        user.delete()

    # -------------------------------------------------------
    # Зміна паролю (користувач знає старий пароль)
    # -------------------------------------------------------
    def change_password(self, user: CustomUser, dto: ChangePasswordDTO) -> None:
        """
        Змінює пароль якщо старий пароль вірний.
        Викидає ValueError якщо старий пароль невірний.
        """
        if not user.check_password(dto.old_password):  # ← dto.old_password
            raise ValueError("Старий пароль невірний.")

        user.set_password(dto.new_password)  # ← dto.new_password
        user.save()

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
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return

        uid   = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"{settings.FRONTEND_URL}/reset-password/?uid={uid}&token={token}"

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
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, CustomUser.DoesNotExist):
            raise ValueError("Невалідне посилання.")

        if not default_token_generator.check_token(user, dto.token):
            raise ValueError("Посилання недійсне або протерміноване.")

        user.set_password(dto.new_password)
        user.save()

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