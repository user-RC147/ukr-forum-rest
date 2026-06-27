from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)

from apps.geo.api.serializers.resolve import CitySerializer

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
