
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework import status
from yaml import serialize


from apps.household.api.serializers.market_serializer import MarketSerializer
from apps.household.apps import HouseholdConfig
from apps.household.permissions.group_permissions import IsGroupCreator,IsOwner
from apps.household.dto.market_dto import CreateMarketInDTO
from apps.household.repositories.maket_repo import MarketRepo
from apps.household.services.market_service import MarketService



class MarketViewSet(ViewSet):

    """
    ViewSet для магазинів.

    list     — всі магазини (глобальні, бачать всі)
    retrieve — деталь магазину
    create   — будь-який залогінений може додати магазин
    update   — тільки той хто створив
    destroy  — тільки той хто створив
    """

    permission_classes=[IsAuthenticated]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #self.service=MarketService(MarketRepo())
        # Беремо готовий зібраний сервіс з контейнера додатка
        self.service = HouseholdConfig.market_service


    def list(self, request):
        """
        GET /api/household/markets/
        Повертає повний список магазинів для селекту на фронтенді.
        """
        # Передаємо дефолтні значення, оскільки сервіс чеselfкає на ці аргументи
        markets = self.service.get_all_markets(
            search_query=None,
            country_id=None,
            region_id=None,
            city_id=None,
            ordering='name'
        )
        serializer=MarketSerializer(markets,many=True)
        return Response(serializer.data)


    def create(self, request):
        """
        POST /api/household/markets/
        Створення нового магазину. Викликається кнопкою з форми чека.
        """

        serializer = MarketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vd = serializer.validated_data

        dto = CreateMarketInDTO(
            name=vd['name'],
            address_line=vd['address_line'],
            country_id=vd['country_id'],
            region_id=vd['region_id'],
            city_id=vd['city_id'],
        )

        try:
            # Передаємо DTO та поточного юзера в сервіс
            market=self.service.create(dto=dto,user=request.user)
            return Response(MarketSerializer(market).data,status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass