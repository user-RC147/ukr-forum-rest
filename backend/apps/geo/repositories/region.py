from collections.abc import Iterable

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from apps.geo.dto.region import RegionDTO
from apps.geo.exceptions.region import RegionNotFoundError
from apps.geo.models.region import RegionModel
from apps.geo.ports.repos import RegionRepositoryPort


class RegionRepository:
    def __init__(self, model=RegionModel) -> None:
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
        region_ids: Iterable[int],
    ) -> list[RegionDTO]:

        qs = self.model.objects.filter(id__in=region_ids).select_related("country")

        return [_to_dto_region(r) for r in qs]

    def get_by_country(self, country_id: int) -> list[RegionDTO]:
        qs = self.model.objects.filter(country__id=country_id).select_related("country")

        return cache.get_or_set(
            f"region:country:{country_id}",
            lambda: [_to_dto_region(r) for r in qs],
            1200 * 24 * 7,
        )


def _to_dto_region(data: RegionModel) -> RegionDTO:
    return RegionDTO(
        id=data.id, name=data.name, name_ua=data.name_ua, country_id=data.country.id
    )


def get_repo_region() -> RegionRepositoryPort:
    return RegionRepository()
