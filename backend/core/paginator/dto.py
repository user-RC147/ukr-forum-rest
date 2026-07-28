from dataclasses import dataclass


@dataclass(frozen=True)
class PaginatorDTO[T]:
    items: list[T]  # самі дані сторінки
    count: int  # загальна кількість елементів (всього, без урахування сторінки)
    page: int  # поточна сторінка
    page_size: int  # розмір сторінки
    total_pages: int  # загальна кількість сторінок
    has_next: bool  # чи є наступна сторінка
    has_previous: bool  # чи є попередня сторінка
