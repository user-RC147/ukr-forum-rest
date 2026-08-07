from typing import Any

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.geo.api.schemas.country import country_search_schema
from apps.geo.api.serializers.resolve import (
    CountrySerializer,
    SearchQuerySerializer,
)
from apps.geo.services.country_service import get_service_country


class CountryView(viewsets.ViewSet):
    serializer_class = CountrySerializer

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = get_service_country()

    def retrieve(self, request: Request, pk: int):
        result = self.service.get(pk)

        return Response(self.serializer_class(result).data, status=status.HTTP_200_OK)

    def list(self, request: Request):
        result = self.service.get_many()

        return Response(self.serializer_class(result).data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    @country_search_schema
    def search(self, request: Request):
        qp = SearchQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)
        query = qp.validated_data.get("q", "")
        if len(query) < 2:
            return Response({"results": [], "query": query})

        result = self.service.search(query)
        serializer = CountrySerializer(result, many=True)
        return Response(serializer.data)
