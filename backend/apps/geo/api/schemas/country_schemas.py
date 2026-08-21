from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)

from apps.geo.api.serializers.country_serializers import CountrySerializer

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
