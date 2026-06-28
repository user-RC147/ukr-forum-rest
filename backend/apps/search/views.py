# search/views.py
import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from .contracts.exceptions import CategoryNotFoundError
from .dto import SearchParams, SortOrder
from .serializers import SearchResultItemSerializer, CategorySerializer
from .services import SearchService

logger = logging.getLogger(__name__)


class SearchView(viewsets.ViewSet):
    serializer_class = SearchResultItemSerializer

    def list(self, request: Request) -> Response:
        return self._search(request, scope=None)

    @action(methods=["get"], detail=False)
    def list_shop(self, request: Request) -> Response:
        return self._search(request, scope="shop")

    def _search(self, request: Request, scope: str | None) -> Response:
        query = request.query_params.get("q", "").strip()
        if len(query) < 3:
            return Response({"results": [], "query": query})

        sort_order = self._parse_sort(request)
        params = self._build_params(request, query, sort_order)

        service = SearchService()
        results = (
            service.search(params, scope=scope) if scope else service.search(params)
        )

        return Response(
            {
                "query": query,
                "results": SearchResultItemSerializer(results, many=True).data,
            }
        )

    def _parse_sort(self, request: Request) -> SortOrder:
        try:
            return SortOrder(request.query_params.get("sort", SortOrder.RELEVANCE))
        except ValueError:
            raise ValidationError(
                {"sort": f"Allowed values: {[s.value for s in SortOrder]}"}
            )

    def _build_params(
        self, request: Request, query: str, sort_order: SortOrder
    ) -> SearchParams:
        qp = request.query_params
        return SearchParams(
            query=query,
            sort_order=sort_order,
            country_id=self._parse_int_param("country_id", qp.get("country_id", "")),
            city_id=self._parse_int_param("city_id", qp.get("city_id", "")),
            region_id=self._parse_int_param("region_id", qp.get("region_id", "")),
            category_id=self._parse_int_param("category_id", qp.get("category_id", "")),
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



class CategoryView(viewsets.ViewSet):
    serializer_class = CategorySerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = SearchService()

    def retrieve(self, request:Request, pk: int) -> Response:
        try:
            result = self.service.get_category(pk)
        except CategoryNotFoundError:
            raise NotFound(detail=str(e))
        
        serializer = CategorySerializer(result)

        return Response(serializer.data)
        
    def list(self, request:Request) -> Response:
        result = self.service.get_categories_all()

        serializer = CategorySerializer(result, many=True)

        return Response(serializer.data)
