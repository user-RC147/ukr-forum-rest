from dataclasses import dataclass, field
from enum import StrEnum


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
class SearchParams:
    query: str
    country_id: int | None
    region_id: int | None
    city_id: int | None
    category_id: int | None
    sort_order: SortOrder = SortOrder.RELEVANCE
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
