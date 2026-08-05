from collections.abc import Iterable

from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.functions import Greatest
from geo.dto.country import CountryDTO
from geo.exceptions.country_exc import CountryNotFoundError
from geo.models.country import CountryModel

from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate


class CountryRepository:
    def __init__(self, model=CountryModel()) -> None:
        self.model = model

    def _get_model(self, country_id: int) -> CountryModel:
        try:
            result = self.model.objects.get(id=country_id)
            return result
        except ObjectDoesNotExist:
            raise CountryNotFoundError(
                extra={"product_id": country_id, "event": "get_country"}
            )

    def get(self, country_id: int) -> CountryDTO:
        result = self._get_model(country_id)
        return _to_dto(result)

    def get_many(
        self,
        country_ids: Iterable[int] | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatorDTO[list[CountryDTO]]:
        result = self.model.objects.all()
        offset = (page - 1) * page_size

        if country_ids is None:
            result = cache.get("country:all")
            if result is None:
                total = result.count()
                items = list(result[offset : offset + page_size])
                result = paginate([_to_dto(r) for r in items], total, page, page_size)
                cache.set("country:all", result, 1200 * 24 * 7)
                return result

        result = result.filter(id__in=country_ids)

        total = result.count()
        items = list(result[offset : offset + page_size])

        return paginate([_to_dto(r) for r in items], total, page, page_size)

    def search(self, query: str, limit: int = 10) -> list[CountryDTO]:
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
        return [_to_dto(r) for r in result]


def _to_dto(data: CountryModel) -> CountryDTO:
    return CountryDTO(
        id=data.id,
        name=data.name,
        name_ua=data.name_ua,
        code=data.code,
        flag_emoji=data.flag_emoji,
        currency=data.currency,
    )
