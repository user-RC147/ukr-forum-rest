from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)

from apps.geo.api.serializers.city_serializers import CitySerializer

city_get_schema = extend_schema(
    summary="Отримати усі міста по айді",
    parameters=[
        OpenApiParameter(
            name="region_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Айді регіона",
            required=True,
        ),
    ],
    responses={200: CitySerializer(many=True)},
)

city_search_schema = extend_schema(
    summary="Результати пошуку міст",
    parameters=[
        OpenApiParameter(
            name="q",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Пошуковий запит",
            required=False,
        ),
        OpenApiParameter(
            name="country_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Айді країни",
            required=True,
        ),
    ],
    responses={200: CitySerializer(many=True)},
)
