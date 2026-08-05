from django.conf import settings
import requests


class GeoApiClient:
    """
    Клієнт для зовнішнього Geo API.
    Використовується тільки при реєстрації і зміні локації.
    """

    def __init__(self):
        self.base_url = settings.GEO_API_URL
        self.token = settings.GEO_API_TOKEN
        self.headers = {"Authorization": f"Token {self.token}"}

    def get_countries(self) -> list[dict]:
        response = requests.get(
            f"{self.base_url}/countries/",
            headers=self.headers,
            timeout=3,
        )
        response.raise_for_status()
        data = response.json()
        # API повертає список або {'results': [...]}
        return data if isinstance(data, list) else data.get("results", [])

    def get_regions(self, country_id: int) -> list[dict]:
        response = requests.get(
            f"{self.base_url}/regions/",
            headers=self.headers,
            timeout=3,
            params={"country_id": country_id},
        )
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else data.get("results", [])

    def get_cities(self, region_id: int) -> list[dict]:
        response = requests.get(
            f"{self.base_url}/cities/",
            headers=self.headers,
            timeout=3,
            params={"region": region_id},
        )
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else data.get("results", [])


geo_api_client = GeoApiClient()
