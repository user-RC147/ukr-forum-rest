from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

@dataclass(frozen=True)
class CategoryDTO:
    id: int
    name: str
    tags: dict


@dataclass(frozen=True)
class TagDTO:
    id: int
    name: str


class ResourceType(StrEnum):
    SHOP = "shop"
    USER = "user"
    TAG = "tag"
    DISCUSSION = "discussion"


class SortOrder(StrEnum):
    NEWEST = "newest"  # created_at DESC
    OLDEST = "oldest"  # created_at ASC
    RELEVANCE = "relevance"  # rank


@dataclass(frozen=True)
class SortParams:
    order: SortOrder = SortOrder.RELEVANCE


@dataclass(frozen=True)
class SearchParams:
    query: str | None
    sort_params: SortParams
    scope_filters: dict[str, Any] = field(default_factory=dict)
    limit: int = 30


@dataclass(frozen=True)
class SearchResultItem:
    """
    DTO for return all modules
    All algoritms in module-owners
    """

    resource_type: ResourceType
    id: int
    title: str
    description: str | None = None
    meta: dict = field(default_factory=dict)
