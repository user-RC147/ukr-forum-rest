# search/views.py
import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .contracts.dto import PaginationParams, SearchParams, SortOrder, SortParams
from .contracts.serializers import CategorySerializer, TagSerializer
from .registry import get_search_registry
from .serializers import (
    PageSerializer,
    SearchResultItemSerializer,
)
from .services import get_category_service, get_search_service, get_tag_service

logger = logging.getLogger(__name__)


class SearchView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    serializer_class = SearchResultItemSerializer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.registry = get_search_registry()
        self.service = get_search_service()

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
        extra_filters = (
            handler.parse_extra_filters(request.query_params) if handler else {}
        )

        page = self._parse_int_param("page", request.query_params.get("page", 1))

        pagination = PaginationParams(page=page)

        params = self._build_params(
            request, query, sort_params, extra_filters, pagination
        )

        results = (
            self.service.search(params, scope=scope)
            if scope
            else self.service.search(params)
        )

        return Response({"query": query, "results": PageSerializer(results).data})

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
        self,
        request: Request,
        query: str | None,
        sort_params: SortParams,
        extra_filters: dict,
        pagination: PaginationParams,
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
            logger.info(
                "Get param with non-int value",
                extra={"key": key, "value": value, "event": "search_validation"},
            )
            raise ValidationError({key: f"Needs to be int: {value}"})


class CategoryView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = get_category_service()

    def retrieve(self, request: Request, pk: int) -> Response:

        result = self.service.get(pk)

        serializer = CategorySerializer(result)

        return Response(serializer.data)

    def list(self, request: Request) -> Response:
        result = self.service.get_many()

        serializer = CategorySerializer(result, many=True)

        return Response(serializer.data)


class TagView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = TagSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = get_tag_service()

    def retrieve(self, request: Request, pk: int) -> Response:

        result = self.service.get(pk)

        serializer = TagSerializer(result)

        return Response(serializer.data)

    def list(self, request: Request) -> Response:
        result = self.service.get_many()

        serializer = TagSerializer(result, many=True)

        return Response(serializer.data)
