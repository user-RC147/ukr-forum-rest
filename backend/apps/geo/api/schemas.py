from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)

from apps.geo.api.serializers import CitySerializer, CountrySerializer

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


country_search_schema = extend_schema(
    summary="Результати пошуку країн",
    parameters=[
        OpenApiParameter(
            name="q",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Пошуковий запит",
            required=False,
        ),
    ],
    responses={200: CountrySerializer(many=True)},
)
