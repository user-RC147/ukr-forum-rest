# search/services.py
import logging

from django.core.exceptions import ObjectDoesNotExist

from .contracts.exceptions import CategoryNotFoundError, TagNotFoundError
from .contracts.protocols import SearchResultItem
from .dto import CategoryDTO, TagDTO
from .models import CategoryModel, TagModel
from .registry import SearchRegistry

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, limit_per_module: int = 10) -> None:
        self.limit_per_module = limit_per_module
        self.category_model = CategoryModel
        self.tag_model = TagModel

    def search(self, params, scope: str | None = None) -> list[SearchResultItem]:
        handlers = SearchRegistry.all()
        items = handlers.items() if scope is None else [(scope, handlers[scope])]

        results: list[SearchResultItem] = []
        for name, handler in items:
            try:
                results.extend(handler.search(params))
            except Exception:
                logger.exception("Search failed in module: %s", name)
                if scope is not None:
                    raise

        return results

    def get_categories(self, category_ids: list[int] | None = None) -> list[CategoryDTO]:
        result = self.category_model.objects.prefetch_related("tags")
        if category_ids is not None:
            result = result.filter(id__in=category_ids)
        return [_to_dto_category(r) for r in result]
    

    def get_category(self, category_id: int) -> CategoryDTO:
        try:
            result = self.category_model.objects.get(id=category_id)
        except ObjectDoesNotExist:
            logger.info("Category with id: %s not found!", category_id)
            raise CategoryNotFoundError("Category with this id does not exist")

        return _to_dto_category(result)

    def get_tag(self, tag_id: int) -> TagDTO:
        try:
            result = self.tag_model.objects.get(id=tag_id)
        except ObjectDoesNotExist:
            logger.info("Tag with id: %s not found!", tag_id)
            raise TagNotFoundError("Category with this id does not exist")

        return _to_dto_tag(result)

    def get_tags(self, tag_ids: list[int] | None = None) -> list[TagDTO]:
        result = self.tag_model.objects.all()
        if tag_ids is not None:
            result.filter(id__in=tag_ids)
        return [_to_dto_tag(r) for r in result]


def _to_dto_category(data) -> CategoryDTO:
    return CategoryDTO(
        id=data.id, name=data.name, tags={t.id: _to_dto_tag(t) for t in data.tags.all()}
    )


def _to_dto_tag(data) -> TagDTO:
    return TagDTO(id=data.id, name=data.name)
