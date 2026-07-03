import dataclasses

from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.db.models import Q

from apps.files.contracts import get_file_contract
from apps.search.contracts.protocols import SearchParams, SearchResultItem
from apps.search.dto import ResourceType, SortOrder
from apps.shop.service import ProductService


class ProductSearchHandler:
    def search(self, params: SearchParams) -> list[SearchResultItem]:

        # FTS
        raw_query = " & ".join(f"{w}:*" for w in params.query.split())
        query = SearchQuery(raw_query, search_type="raw", config="simple")
        vector = SearchVector("title", weight="A", config="simple")

        qs = (
            ProductService.get_searchable_queryset()
            .only("id", "title", "description", "price", "created_at", "files_ids")
            .annotate(
                rank=SearchRank(vector, query),
                similarity=TrigramSimilarity("title", params.query),
            )
            .filter(Q(rank__gt=0.1) | Q(similarity__gt=0.3))
        )
        # sort
        match params.sort_order:
            case SortOrder.NEWEST:
                qs = qs.order_by("created_at")
            case SortOrder.OLDEST:
                qs = qs.order_by("-created_at")
            case SortOrder.RELEVANCE:
                qs = qs.order_by("-rank", "-similarity")

        products = list(qs[: params.limit])

        all_file_ids = [fid for obj in products for fid in (obj.files_ids or [])]
        files_map = get_file_contract().get_many(all_file_ids) if all_file_ids else {}

        return [self._to_dto(obj, files_map) for obj in products]

    @staticmethod
    def _to_dto(obj, files_map: dict) -> SearchResultItem:
        files = [
            dataclasses.asdict(files_map[fid])
            for fid in (obj.files_ids or [])
            if fid in files_map
        ]

        return SearchResultItem(
            resource_type=ResourceType.SHOP,
            id=obj.id,
            title=obj.title,
            description=obj.description,
            meta={
                "price": obj.price,
                "created_at": obj.created_at.strftime("%d.%m.%Y %H:%M:%S"),
                "files": files,
            },
        )
