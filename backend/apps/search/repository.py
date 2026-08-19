from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from .contracts.dto import CategoryDTO, TagDTO
from .contracts.exceptions import CategoryNotFoundError, TagNotFoundError
from .models import CategoryModel, TagModel


class CategoryRepository:
    def __init__(self) -> None:
        self.model = CategoryModel

    def get(self, id: int):
        try:
            result = self.model.objects.prefetch_related("tags").get(id=id)
        except ObjectDoesNotExist:
            raise CategoryNotFoundError(
                extra={"category_id": id, "event": "category_get"}
            )
        return _to_dto_category(result)

    def get_many(self, ids: list[int] | None = None) -> list[CategoryDTO]:
        result = self.model.objects.prefetch_related("tags")
        if ids is None:
            return cache.get_or_set(
                "category:all", lambda: [_to_dto_category(r) for r in result], 60 * 5
            )

        result = result.filter(id__in=ids)

        return [_to_dto_category(r) for r in result]


class TagRepository:
    def __init__(self) -> None:
        self.model = TagModel

    def get(self, id: int) -> TagDTO:
        try:
            result = self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            raise TagNotFoundError(extra={"tag_id": id, "event": "tag_get"})

        return _to_dto_tag(result)

    def get_many(self, ids: list[int] | None = None) -> list[TagDTO]:
        result = self.model.objects.all()
        if ids is None:
            return cache.get_or_set(
                "tag:all", lambda: [_to_dto_tag(r) for r in result], 60 * 5
            )

        result = result.filter(id__in=ids)
        return [_to_dto_tag(r) for r in result]


def _to_dto_category(data: CategoryModel) -> CategoryDTO:
    return CategoryDTO(
        id=data.id,
        name=data.name,
        tags={t.id: _to_dto_tag(t) for t in data.tags.all()},
    )


def _to_dto_tag(data) -> TagDTO:
    return TagDTO(id=data.id, name=data.name)


def get_category_repo() -> CategoryRepository:
    return CategoryRepository()


def get_tag_repo() -> TagRepository:
    return TagRepository()
