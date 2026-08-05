from collections.abc import Iterable

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from geo.dto.region import RegionDTO
from geo.exceptions.region_exc import RegionNotFoundError
from geo.models.region import RegionModel

from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate


class RegionRepository:
    def __init__(self, model=RegionModel()) -> None:
        self.model = model

    def _get_model(self, region_id: int) -> RegionModel:
        try:
            result = self.model.objects.select_related("country").get(id=region_id)
            return result
        except ObjectDoesNotExist:
            raise RegionNotFoundError(
                extra={"region_id": region_id, "event": "get_region"}
            )

    def get(self, region_id: int) -> RegionDTO:
        result = self._get_model(region_id)
        return _to_dto_region(result)

    def get_many(
        self,
        region_ids: Iterable[int] | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatorDTO[list[RegionDTO]]:
        result = self.model.objects.all().select_related("country")

        offset = (page - 1) * page_size

        if region_ids is None:
            key = "region:all"
            result = cache.get(key)
            if result is None:
                total = result.count()
                items = list(result[offset : offset + page_size])
                result = paginate(
                    [_to_dto_region(r) for r in items], total, page, page_size
                )
                cache.set(key, result, 1200 * 24 * 7)
                return result

        result = result.filter(id__in=region_ids)

        total = result.count()
        items = list(result[offset : offset + page_size])

        return paginate([_to_dto_region(r) for r in items], total, page, page_size)


def _to_dto_region(data: RegionModel) -> RegionDTO:
    return RegionDTO(
        id=data.id, name=data.name, name_ua=data.name_ua, country_id=data.country.id
    )
