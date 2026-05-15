from typing import Protocol


class GeoServiceProtocol(Protocol):

    def get_countries(self) -> dict: ...

    def get_regions(self, country_code: str | None = None) -> dict: ...

    def get_cities(
        self, region_id: str | None = None, search: str | None = None
    ) -> dict: ...


class GeoRepositoryProtocol(Protocol):

    def get_or_create_country(self, api_data: dict): ...

    def get_or_create_region(self, api_data: dict, country): ...

    def get_or_ctreate_city(self, api_data: dict, country, region): ...


class LocationProtocol(Protocol):
    """
    Контракт для моделей які мають локацію.
    Замість ForeignKey до geo моделей — просто id.
    """

    country_id: int | None
    region_id: int | None
    city_id: int | None
