from math import ceil

from backend.core.paginations.dto import PaginatorDTO, T


def paginate_build(
    items: list[T], count: int, page: int, page_size: int
) -> PaginatorDTO[T]:

    total_pages = ceil(count / page_size)
    has_next: bool = page < total_pages
    has_previous = page > 1

    return PaginatorDTO(
        items=items,
        count=count,
        page=page,
        page_size=page_size,
        has_next=has_next,
        has_previous=has_previous,
        total_pages=total_pages,
    )
