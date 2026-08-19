# search/services.py
import logging

from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate

from .contracts.dto import CategoryDTO, SearchParams, TagDTO
from .contracts.protocols import SearchResultItem
from .registry import SearchRegistry
from .repository import get_category_repo, get_tag_repo

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, limit_per_module: int = 10) -> None:
        self.limit_per_module = limit_per_module
        self.category_repo = get_category_repo()
        self.tag_repo = get_tag_repo()

    def search(
        self, params: SearchParams, scope: str | None = None
    ) -> PaginatorDTO[list[SearchResultItem]]:
        handlers = SearchRegistry.all()
        items = handlers.items() if scope is None else [(scope, handlers[scope])]
        total = 0

        results: list[SearchResultItem] = []
        for name, handler in items:
            try:
                search = handler.search(params)
            except Exception:
                logger.exception("Search failed in module: %s", name)
                if scope is not None:
                    raise
            total += search.count
            results.extend(search.items)

        return paginate(results, total, params.pagination.page, params.pagination.limit)

    def get_categories(
        self, category_ids: list[int] | None = None
    ) -> list[CategoryDTO]:
        return self.category_repo.get_many(category_ids)

    def get_category(self, category_id: int) -> CategoryDTO:
        return self.category_repo.get(category_id)

    def get_tag(self, tag_id: int) -> TagDTO:
        return self.tag_repo.get(tag_id)

    def get_tags(self, tag_ids: list[int] | None = None) -> list[TagDTO]:
        return self.tag_repo.get_many(tag_ids)
