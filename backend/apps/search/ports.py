from typing import Protocol

from .contracts.dto import CategoryDTO, TagDTO


class CategoryRepositoryPort(Protocol):
    def get(self, id: int): ...

    def get_many(self, ids: list[int] | None = None) -> list[CategoryDTO]: ...


class TagRepositoryPort(Protocol):
    def get(self, id: int) -> TagDTO: ...

    def get_many(self, ids: list[int] | None = None) -> list[TagDTO]: ...
