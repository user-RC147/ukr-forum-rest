from collections.abc import Iterable

from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.functions import Greatest
from geo.dto.city import CityDTO
from geo.exceptions.city_exc import CityNotFoundError
from geo.models.city import CityModel
from geo.repositories.region_repository import _to_dto_region

from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate


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
        city_ids: Iterable[int] | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatorDTO[list[CityDTO]]:
        result = self.model.objects.all().select_related("region", "country")

        offset = (page - 1) * page_size

        if city_ids is None:
            key = "city:all"
            result = cache.get(key)
            if result is None:
                total = result.count()
                items = list(result[offset : offset + page_size])
                result = paginate(
                    [_to_dto_city(r) for r in items], total, page, page_size
                )
                cache.set(key, result, 1200 * 24 * 7)
                return result

        result = result.filter(id__in=city_ids)

        total = result.count()
        items = list(result[offset : offset + page_size])

        return paginate([_to_dto_city(r) for r in items], total, page, page_size)

    def search(self, query: str, limit: int) -> list[CityDTO]:
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
            )
            .order_by("-similarity", "name")[:limit]
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
