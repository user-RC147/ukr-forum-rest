from ..services import SearchService
from .dto import CategoryDTO
from .protocols import CategoryProtocol


class CategoryContract:
    def __init__(self) -> None:
        self.service = SearchService()

    def get_many(self, category_ids: list[int]) -> dict[int, CategoryDTO]:
        result = self.service.get_categories(category_ids)
        return {r.id: r for r in result}

    def get(self, category_id: int) -> CategoryDTO:
        return self.service.get_category(category_id)


def get_category_contract() -> CategoryProtocol:
    return CategoryContract()
