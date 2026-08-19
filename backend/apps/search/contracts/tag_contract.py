from ..services import TagService, get_tag_service
from .dto import TagDTO
from .protocols import TagProtocol


class TagContract:
    def __init__(self, service: TagService) -> None:
        self.service = service

    def get_many(self, tag_ids: list[int]) -> dict[int, TagDTO]:
        result = self.service.get_many(tag_ids)
        return {r.id: r for r in result}

    def get(self, tag_id: int) -> TagDTO:
        return self.service.get(tag_id)


def get_category_contract() -> TagProtocol:
    return TagContract(get_tag_service())
