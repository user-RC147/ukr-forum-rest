from typing import Protocol, runtime_checkable

from core.paginator.dto import PaginatorDTO

from ..dto import CategoryDTO, SearchParams, SearchResultItem, TagDTO


@runtime_checkable
class Searchable(Protocol):
    def search(self, params: SearchParams) -> PaginatorDTO[list[SearchResultItem]]: ...


class CategoryProtocol(Protocol):
    def get_many(self, category_ids: list[int]) -> dict[int, CategoryDTO]: ...

    def get(self, category_id: int) -> CategoryDTO: ...


class TagProtocol(Protocol):
    def get_many(self, tag_ids: list[int]) -> dict[int, TagDTO]: ...

    def get(self, tag_id: int) -> TagDTO: ...
