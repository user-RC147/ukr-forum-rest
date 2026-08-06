from collections.abc import Iterable

from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.functions import Greatest

from apps.geo.dto.city import CityDTO
from apps.geo.exceptions.city_exc import CityNotFoundError
from apps.geo.models.city import CityModel
from apps.geo.repositories.region_repository import _to_dto_region


class CityRepository:
    def __init__(self, model=CityModel()) -> None:
        self.model = model

    def _get_model(self, city_id: int) -> CityModel:
        try:
            result = self.model.objects.select_related("region", "country").get(
                id=city_id
            )
            return result
        except ObjectDoesNotExist:
            raise CityNotFoundError(extra={"city_id": city_id, "event": "get_city"})

    def get(self, city_id: int) -> CityDTO:
        result = self._get_model(city_id)
        return _to_dto_city(result)

    def get_many(
        self,
        city_ids: Iterable[int],
    ) -> list[CityDTO]:
        qs = self.model.objects.filter(id__in=city_ids).select_related(
            "region", "country"
        )

        qs = qs.filter(id__in=city_ids)

        return [_to_dto_city(r) for r in qs]

    def get_by_region(self, region_id: int) -> list[CityDTO]:
        qs = self.model.objects.filter(country__id=region_id).select_related("country")

        return cache.get_or_set(
            f"city:country:{region_id}",
            lambda: [_to_dto_region(r) for r in qs],
            1200 * 24 * 7,
        )

    def search(self, query: str, country_id: int) -> list[CityDTO]:
        result = (
            self.model.objects.all()
            .only("id", "name", "name_ua")
            .annotate(
                similarity=Greatest(
                    TrigramSimilarity("name", query),
                    TrigramSimilarity("name_ua", query),
                )
            )
            .filter(
                Q(name__istartswith=query)
                | Q(name_ua__istartswith=query)
                | Q(similarity__gt=0.3)
                | Q(country__id=country_id)
            )
            .order_by("-similarity", "name")
        )
        return [_to_dto_city(r) for r in result]


def _to_dto_city(data: CityModel) -> CityDTO:
    return CityDTO(
        id=data.id,
        name=data.name,
        name_ua=data.name_ua,
        country_id=data.country.id,
        region=_to_dto_region(data.region),
        latitude=data.latitude,
        longitude=data.longitude,
    )
