from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.apps import apps

from apps.household.api.serializers import GroupMemberOutSerializer,GroupOutSerializer,CreateGroupInSerializer
from apps.household.selectors import GroupSelector
from apps.household.apps import HouseholdConfig
from apps.household.services import GroupService
from drf_spectacular.utils import extend_schema



class GroupViewSet(viewsets.ViewSet):
    """
    Контролер для управління групами користувачів.
    Працює виключно через сервісний шар Чистої Архітектури.
    """
    permission_classes=[IsAuthenticated]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        # 1. Отримуємо живий екземпляр конфігу додатка з реєстру Django
        household_config = apps.get_app_config('household')
        
        # 2. Тепер властивість спрацює правильно і поверне зібраний GroupService
        self._service = household_config.group_service




    def list(self, request):
        """
        GET /api/household/groups/
        Отримання списку всіх груп поточного користувача.
        """

        # 1. Викликаємо метод екземпляра сервісу, передаючи ID авторизованого юзера
        dtos = self._service.get_all_list(user_id=request.user.id)

        # 2. Передаємо отриманий масив DTO в серіалізатор для виводу (many=True)

        serializer = GroupOutSerializer(dtos,many=True)

        # 3. Повертаємо сформований JSON
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @extend_schema(
    #     request=CreateGroupInSerializer,
    #     responses={201: {"type": "object", "properties": {"id": {"type": "integer"}, "detail": {"type": "string"}}}}
    # )
    def create(self, request):
        """
        POST /api/household/groups/
        Створення нової групи поточним аутентифікованим користувачем.
        """
        # 1. Передаємо сирі дані в серіалізатор для перевірки
        serializer=CreateGroupInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Перетворюємо перевірені дані у чисте вхідне DTO
        dto=serializer.to_dto()

        # 3. Викликаємо сервіс через публічну точку доступу в AppConfig
        # Поточний юзер (request.user.id) автоматично стає творцем
        group_id=self._service.create_new_group(
            dto=dto,
            creator_id=request.user.id
        )

        # 4. Повертаємо відповідь про успішне створення
        return Response(
            {"id": group_id, "detail": "Групу успішно створено."},
            status=status.HTTP_201_CREATED
        )


    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass