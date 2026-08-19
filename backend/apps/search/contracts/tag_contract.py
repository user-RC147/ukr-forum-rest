from ..services import SearchService
from .dto import TagDTO
from .protocols import TagProtocol


class TagContract:
    def __init__(self) -> None:
        self.service = SearchService()

    def get_many(self, tag_ids: list[int]) -> dict[int, TagDTO]:
        result = self.service.get_tags(tag_ids)
        return {r.id: r for r in result}

    def get(self, tag_id: int) -> TagDTO:
        return self.service.get_tag(tag_id)


def get_category_contract() -> TagProtocol:
    return TagContract()
