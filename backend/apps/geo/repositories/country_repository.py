from collections.abc import Iterable

from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.functions import Greatest

from apps.geo.contracts.dto.country_dto import CountryDTO
from apps.geo.contracts.exceptions.country_exception import CountryNotFoundError
from apps.geo.models.country_model import CountryModel
from apps.geo.ports.repo_ports import CountryRepositoryPort


class CountryRepository:
    def __init__(self, model=CountryModel) -> None:
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
        return _to_dto_country(result)

    def get_many(
        self,
        country_ids: Iterable[int] | None = None,
    ) -> list[CountryDTO]:

        all_countries = cache.get_or_set(
            "country:all",
            lambda: [_to_dto_country(r) for r in self.model.objects.all()],
            1200 * 24 * 7,
        )
        if country_ids is None:
            return all_countries

        ids_set = set(country_ids)
        return [c for c in all_countries if c.id in ids_set]

    def search(self, query: str) -> list[CountryDTO]:
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
            .order_by("-similarity", "name")
        )
        return [_to_dto_country(r) for r in result]


def _to_dto_country(data: CountryModel) -> CountryDTO:
    return CountryDTO(
        id=data.id,
        name=data.name,
        name_ua=data.name_ua,
        code=data.code,
        flag_emoji=data.flag_emoji,
        currency=data.currency,
    )


def get_repo_country() -> CountryRepositoryPort:
    return CountryRepository()
