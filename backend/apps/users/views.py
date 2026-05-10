# apps/users/views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import (
    UserRegisterSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
    LocationUpdateSerializer,
)
from apps.users.services import (
    auth_service,
    get_profile,
    update_profile,
    update_location,
)


class RegisterView(APIView):
    """
    POST /api/users/register/
    Реєстрація нового користувача.
    Доступно всім — без авторизації.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # 1. валідація
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. серіалізатор → DTO
        dto = serializer.to_dto()

        # 3. DTO → сервіс → БД
        user = auth_service.register_user(dto)

        return Response(
            {"detail": f"Користувача {user.username} успішно зареєстровано."},
            status=status.HTTP_201_CREATED,
        )


class ProfileView(APIView):
    """
    GET  /api/users/profile/  — отримати профіль
    PATCH /api/users/profile/ — оновити профіль
    Тільки для авторизованих користувачів.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # request.user — поточний авторизований користувач (з JWT токена)
        user = get_profile(request.user)

        # серіалізатор для відповіді — перетворює об'єкт користувача в JSON
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        # 1. валідація — partial=True означає що не всі поля обов'язкові
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. серіалізатор → DTO
        dto = serializer.to_dto()

        # 3. DTO → сервіс → БД
        user = update_profile(request.user, dto)

        return Response(
            {"detail": "Профіль успішно оновлено."},
            status=status.HTTP_200_OK,
        )


class DeleteAccountView(APIView):
    """
    DELETE /api/users/delete/
    Видалення акаунту поточного користувача.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        auth_service.delete_account(request.user)
        return Response(
            {"detail": "Акаунт успішно видалено."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ChangePasswordView(APIView):
    """
    POST /api/users/change-password/
    Зміна паролю — користувач знає старий пароль.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # 1. валідація
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. серіалізатор → DTO
        dto = serializer.to_dto()

        # 3. сервіс — може викинути ValueError якщо старий пароль невірний
        try:
            auth_service.change_password(request.user, dto)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Пароль успішно змінено."},
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(APIView):
    """
    POST /api/users/password-reset/
    Крок 1 — запит на відновлення паролю.
    Відправляє email з посиланням.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # сервіс мовчки ігнорує невідомий email (з міркувань безпеки)
        auth_service.request_password_reset(
            email=serializer.validated_data['email']
        )

        # завжди повертаємо однакову відповідь —
        # не розкриваємо чи існує такий email
        return Response(
            {"detail": "Якщо такий email існує — ми надіслали інструкції."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """
    POST /api/users/password-reset/confirm/
    Крок 2 — підтвердження відновлення паролю.
    Приймає uid, token і новий пароль.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # 1. валідація
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. серіалізатор → DTO
        dto = serializer.to_dto()

        # 3. сервіс — може викинути ValueError якщо токен невалідний
        try:
            auth_service.confirm_password_reset(dto)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Пароль успішно відновлено."},
            status=status.HTTP_200_OK,
        )
    



class LocationUpdateView(APIView):
    """
    POST /api/users/location/
    Зберігає локацію користувача в локальну БД.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # 1. валідація
        serializer = LocationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. серіалізатор → DTO
        dto = serializer.to_dto()

        # 3. сервіс → БД
        update_location(request.user, dto)

        return Response(
            {"detail": "Локацію успішно збережено."},
            status=status.HTTP_200_OK,
        )
    





