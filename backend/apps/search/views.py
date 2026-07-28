# search/views.py
import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from .dto import SearchParams, SortOrder, SortParams, PaginationParams
from .serializers import SearchResultItemSerializer, CategorySerializer, TagSerializer
from .services import SearchService
from .registry import SearchRegistry

logger = logging.getLogger(__name__)


class SearchView(viewsets.ViewSet):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.registry = SearchRegistry

    serializer_class = SearchResultItemSerializer

    def list(self, request: Request) -> Response:
        return self._search(request, scope=None)

    @action(methods=["get"], detail=False)
    def list_shop(self, request: Request) -> Response:
        return self._search(request, scope="shop")

    def _search(self, request: Request, scope: str | None) -> Response:
        query = request.query_params.get("q", None)

        if query is not None:
            query = query.strip()
            if len(query) < 3:
                return Response({"results": [], "query": query})

        sort_params = self._parse_sort(request)

        handler = self.registry.all()[scope] if scope else None
        extra_filters = handler.parse_extra_filters(request.query_params) if handler else {}

        page = self._parse_int_param("page", request.query_params.get("page", 1))

        pagination = PaginationParams(page=page)


        params = self._build_params(request, query, sort_params, extra_filters, pagination)

        service = SearchService()
        results = (
            service.search(params, scope=scope) if scope else service.search(params)
        )

        return Response(
            {
                "query": query,
                "total": results[0],
                "results": SearchResultItemSerializer(results[1], many=True).data,
            }
        )

    def _parse_sort(self, request: Request) -> SortParams:
        raw = request.query_params.get("sort", SortOrder.RELEVANCE)
        try:
            order = SortOrder(raw)
        except ValueError:
            logger.info(
                "Invalid sort param",
                extra={"value": raw, "event": "search_validation"},
            )
            raise ValidationError(
                {"sort": f"Allowed values: {[s.value for s in SortOrder]}"}
            )
        return SortParams(order=order)

    def _build_params(
        self, request: Request, query: str | None, sort_params: SortParams, extra_filters: dict, pagination: PaginationParams
    ) -> SearchParams:
        return SearchParams(
            query=query,
            pagination=pagination,
            sort_params=sort_params,
            scope_filters=extra_filters,
        )

    @staticmethod
    def _parse_int_param(key: str, value: str) -> int | None:
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            logger.info("Get param with non-int value", extra={"key": key, "value": value, "event": "search_validation"})
            raise ValidationError({key: f"Needs to be int: {value}"})



class CategoryView(viewsets.ViewSet):
    serializer_class = CategorySerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = SearchService()

    def retrieve(self, request:Request, pk: int) -> Response:

        result = self.service.get_category(pk)
        
        serializer = CategorySerializer(result)

        return Response(serializer.data)
        
    def list(self, request:Request) -> Response:
        result = self.service.get_categories()

        serializer = CategorySerializer(result, many=True)

        return Response(serializer.data)
    
class TagView(viewsets.ViewSet):
    serializer_class = TagSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = SearchService()

    def retrieve(self, request:Request, pk: int) -> Response:

        result = self.service.get_tag(pk)
        
        serializer = TagSerializer(result)

        return Response(serializer.data)
        
    def list(self, request:Request) -> Response:
        result = self.service.get_tags()

        serializer = TagSerializer(result, many=True)

        return Response(serializer.data)
