# search/views.py
import logging

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from .contracts import SearchParams, SortOrder
from .serializers import SearchResultItemSerializer
from .services import SearchService

logger = logging.getLogger(__name__)


class SearchView(viewsets.ViewSet):
    serializer_class = SearchResultItemSerializer

    def list(self, request: Request) -> Response:
        query = request.query_params.get("q", "").strip()

        if len(query) < 3:
            return Response({"results": [], "query": query})

        try:
            sort_order = SortOrder(
                request.query_params.get("sort", SortOrder.RELEVANCE)
            )
        except ValueError:
            raise ValidationError(
                {"sort": f"Allowed values: {[s.value for s in SortOrder]}"}
            )

        params = SearchParams(
            query=query,
            sort_order=sort_order,
            country_id=self._parse_int_param(
                "country_id", request.query_params.get("country_id", "")
            ),
            city_id=self._parse_int_param(
                "city_id", request.query_params.get("country_id", "")
            ),
            region_id=self._parse_int_param(
                "region_id", request.query_params.get("country_id", "")
            ),
            category_id=self._parse_int_param(
                "category_id", request.query_params.get("country_id", "")
            ),
        )

        results = SearchService().search(params)

        return Response(
            {
                "query": query,
                "results": SearchResultItemSerializer(results, many=True).data,
            }
        )

    @staticmethod
    def _parse_int_param(key: str, value: str) -> int | None:
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            logger.info("Get param %s with non-int value: %s", key, value)
            raise ValidationError({key: f"Needs to be int: {value}"})
