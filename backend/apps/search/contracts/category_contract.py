from ..services import CategoryService, get_category_service
from .dto import CategoryDTO
from .protocols import CategoryProtocol


class CategoryContract:
    def __init__(self, service: CategoryService) -> None:
        self.service = service

    def get_many(self, category_ids: list[int]) -> dict[int, CategoryDTO]:
        result = self.service.get_many(category_ids)
        return {r.id: r for r in result}

    def get(self, category_id: int) -> CategoryDTO:
        return self.service.get(category_id)


def get_category_contract() -> CategoryProtocol:
    return CategoryContract(get_category_service())
