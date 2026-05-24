from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from yaml import serialize

# Імпортуємо серіалізатор чеків
from apps.household.api.serializers import PurchaseCreateSerializer
# Імпортуємо конфіг додатка як контейнер сервісів
from apps.household.apps import HouseholdConfig
from apps.household.models import purchase


class PurchaseViewSet(viewsets.ViewSet):
    """
    ViewSet для управління чеками (Purchases) через шари сервісів.
    Контролер для управління чеками та витратами.
    Працює виключно з авторизованими користувачами платформи.
    """

    # Захищаємо ендпоінт: тільки зареєстровані юзери мають доступ до модуля household
    permission_classes=[IsAuthenticated]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Пояснення дії: Зв'язуємо контролер із сервісом через наш контейнер додатка.
        # Записуємо посилання на сам сервіс чеків у приватну змінну контролера.
        self._service=HouseholdConfig.purchase_service


    def list(self, request):
        pass

    def create(self, request):
        """
        POST-метод для створення нового чека з товарами.
        """
        # 1. Передаємо сирі дані з фронтенду в серіалізатор
        serializer=PurchaseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Переводимо перевірені дані в чисте DTO
        dto=serializer.to_dto()

        try:
            # 3. Викликаємо наш сервіс, який ми зберегли в конструкторі класу
            purchase=self._service.create_purchase(dto=dto,user=request.user)

            # 4. Повертаємо успішну відповідь
            return Response(
                {
                    "message": "Чек успішно збережено", 
                    "purchase_id": purchase.id
                },
                status=status.HTTP_201_CREATED
            )

        except PermissionError as e:
            # 5. Якщо Селектор прав виявив роль VIEWER — повертаємо 403
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_403_FORBIDDEN
            )


    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
