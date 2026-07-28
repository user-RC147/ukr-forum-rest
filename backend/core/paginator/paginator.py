from math import ceil

from core.paginator.dto import PaginatorDTO

#для реалізації в selectors
    # count = purchase_items.count()
    # offset = (page - 1) * page_size
    # page_items = purchase_items[offset : offset + page_size]


def paginate(items: list, count: int, page: int, page_size: int) -> PaginatorDTO:

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
