
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework import status
from drf_spectacular.utils import extend_schema


from apps.household.api.serializers.market_serializer import MarketSerializer, MarketCreateSerializer,MarketFullSerializer
from apps.household.apps import HouseholdConfig
from apps.household.permissions.group_permissions import IsGroupCreator,IsOwner
from apps.household.dto.market_dto import CreateMarketInDTO, ListMarketDTO, MarketFullOutDTO
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
        self._service=MarketService()

    def list(self, request):
        """
        GET /api/household/markets/
        """
        # 1. Читаємо query-параметри з URL фронтенду (якщо вони є)
        # search_query = request.query_params.get('search', None)
        # country_id = request.query_params.get('country_id', None)
        # region_id = request.query_params.get('region_id', None)
        # city_id = request.query_params.get('city_id', None)
        # ordering = request.query_params.get('ordering', 'name')

        # 2. Викликаємо ініціалізований сервіс (а не сам клас статично!)
        # Примітка: переконайтеся, що у вашому View екземпляр сервісу лежить у self.market_service або аналогічно
        markets_data = self._service.get_all()
                
        # 3. Проганяємо дані через серіалізатор
        serializer = MarketFullSerializer(markets_data, many=True)
        
        # 4. Повертаємо саме serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=MarketCreateSerializer, responses=MarketSerializer)
    def create(self, request):
        """
        POST /api/household/markets/
        Створення нового магазину. Викликається кнопкою з форми чека.
        """

        serializer = MarketCreateSerializer(data=request.data)
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
            market=self._service.create(dto=dto,user=request.user.id)
            return Response(MarketSerializer(market).data,status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass