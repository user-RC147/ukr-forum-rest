from math import atan2, cos, radians, sin, sqrt

from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.db.models import Q
from django.http import QueryDict

from apps.search.contracts.dto import (
    ResourceType,
    SearchParams,
    SearchResultItem,
    SortOrder,
)
from apps.shop.contracts.exceptions import ProductValidationError
from apps.shop.repository import get_repo
from apps.geo.contracts.city_contract import get_city_contract
from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate
import logging
from .enums import ProductStatus
from .service import get_service

logger = logging.getLogger(__name__)

class ProductSearchHandler:
    STATUS_PARAM = "status"

    def parse_extra_filters(self, query_params: QueryDict) -> dict:
        int_param = {"country_id", "city_id", "region_id", "category_id", "radius"}

        result = {i: _parse_int_param(i, query_params.get(i, "")) for i in int_param}

        status = query_params.get(self.STATUS_PARAM, None)

        if status:
            try:
                result[self.STATUS_PARAM] = ProductStatus(status)
            except ValueError:
                raise ProductValidationError(
                    {
                        self.STATUS_PARAM: f"Allowed values: {[s.value for s in ProductStatus]}"
                    },
                    extra={"invalid_value": status, "event": "search_validaton"},
                )

        return result

    def search(self, params: SearchParams) -> PaginatorDTO[list[SearchResultItem]]:

        repo = get_repo()
        qs = repo.searchable_queryset().only("id")
        # FTS
        if params.query:
            raw_query = " & ".join(f"{w}:*" for w in params.query.split())
            query = SearchQuery(raw_query, search_type="raw", config="simple")
            vector = SearchVector("title", weight="A", config="simple") + SearchVector(
                "description", weight="B", config="simple"
            )

            qs = qs.annotate(
                rank=SearchRank(vector, query),
                similarity=TrigramSimilarity("title", params.query),
            ).filter(Q(rank__gt=0.1) | Q(similarity__gt=0.3))

        to_sort = dict()
        category_id = params.scope_filters.get("category_id")
        if category_id:
            to_sort["category_id"] = category_id

        radius = params.scope_filters.get("radius")

        if radius is None:
            city_id = params.scope_filters.get("city_id")
            country_id = params.scope_filters.get("country_id")
            if city_id:
                to_sort["city_id"] = city_id
            elif country_id:
                to_sort["country_id"] = country_id

        status = params.scope_filters.get(self.STATUS_PARAM)

        if status:
            to_sort["status"] = status.value

        qs = qs.filter(**to_sort)

        match params.sort_params.order:
            case SortOrder.NEWEST:
                qs = qs.order_by("-created_at")
            case SortOrder.OLDEST:
                qs = qs.order_by("created_at")
            case SortOrder.RELEVANCE:
                if params.query:
                    qs = qs.order_by("-rank", "-similarity")
                else:
                    qs = qs.order_by("-created_at")

        products = list(qs)

        service = get_service()
        products = service.get_many(
            page_size=params.pagination.limit,
            page=params.pagination.page,
            product_ids=[p.id for p in products],
        )

        products_count, products = products.count, products.items


        if radius is not None:
            city_contract = get_city_contract()
            user_city = city_contract.get(params.scope_filters.get("city_id"))
            products = [
                i
                for i in products
                if self._cities_within_radius(
                    user_city.latitude,
                    user_city.longitude,
                    radius,
                    i.city,
                )
            ]

        result = paginate(
            [_to_dto(obj) for obj in products],
            products_count,
            params.pagination.page,
            params.pagination.limit,
        )
        return result

    @staticmethod
    def _cities_within_radius(user_lat, user_lon, radius_km, city) -> bool:
        return (
            _haversine(user_lat, user_lon, city["latitude"], city["longitude"])
            <= radius_km
        )


def _to_dto(obj) -> SearchResultItem:

    return SearchResultItem(
        resource_type=ResourceType.SHOP,
        id=obj.id,
        title=obj.title,
        description=obj.description,
        meta={
            "owner": obj.owner,
            "price": obj.price,
            "created_at": obj.created_at.strftime("%d.%m.%Y %H:%M"),
            "status": obj.status,
            "files": obj.files,
            "country": obj.country,
            "region": obj.region,
            "city": obj.city,
            "category": obj.category,
        },
    )


def _parse_int_param(key: str, value: str) -> int | None:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        raise ProductValidationError(
            "Invalid value from key %s",
            key,
            extra={"key": key, "value": value, "event": "search_validaton"},
        )


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))
