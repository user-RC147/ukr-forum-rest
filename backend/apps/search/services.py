# search/services.py
import logging

from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate

from .contracts.dto import CategoryDTO, SearchParams, TagDTO
from .contracts.protocols import SearchResultItem
from .ports import CategoryRepositoryPort, TagRepositoryPort
from .registry import SearchRegistry
from .repository import get_category_repo, get_tag_repo

logger = logging.getLogger(__name__)


class CategoryService:
    def __init__(self, category_repo: CategoryRepositoryPort) -> None:
        self.repo = category_repo

    def get_many(self, category_ids: list[int] | None = None) -> list[CategoryDTO]:
        return self.repo.get_many(category_ids)

    def get(self, category_id: int) -> CategoryDTO:
        return self.repo.get(category_id)


class TagService:
    def __init__(
        self,
        tag_repo: TagRepositoryPort,
    ) -> None:
        self.repo = tag_repo

    def get(self, tag_id: int) -> TagDTO:
        return self.repo.get(tag_id)

    def get_many(self, tag_ids: list[int] | None = None) -> list[TagDTO]:
        return self.repo.get_many(tag_ids)


class SearchService:
    def __init__(
        self,
        limit_per_module: int = 10,
    ) -> None:
        self.limit_per_module = limit_per_module

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


def get_search_service() -> SearchService:
    return SearchService()


def get_category_service() -> CategoryService:
    return CategoryService(category_repo=get_category_repo())


def get_tag_service() -> TagService:
    return TagService(tag_repo=get_tag_repo())
