# apps/geo/services/geo_service.py
import requests
from django.conf import settings


class GeoService:
    """
    Відповідає за всі запити до зовнішнього Geo API.
    
    Клас тому що всі методи використовують спільний стан:
    _url і _headers — не повторюємо їх в кожному методі.
    """

    def __init__(self):
        self._url     = settings.GEO_API_URL
        self._headers = {"Authorization": f"Token {settings.GEO_API_TOKEN}"}

    def get_countries(self) -> dict:
        """Повертає список всіх країн."""
        return self._get("/countries/", params={"page_size": 300})

    def get_regions(self, country_code: str | None = None) -> dict:
        """Повертає регіони, опціонально фільтровані по країні."""
        params = {"page_size": 500}
        if country_code:
            params["country_code"] = country_code
        return self._get("/regions/", params=params)

    def get_cities(self, region_id: str | None = None, search: str | None = None) -> dict:
        """Повертає міста, опціонально фільтровані по регіону або пошуку."""
        params = {"page_size": 500}
        if region_id:
            params["region"] = region_id
        if search:
            params["search"] = search
        return self._get("/cities/", params=params)

    def _get(self, endpoint: str, params: dict) -> dict:
        """
        Приватний метод — робить GET запит до зовнішнього API.
        Використовується всередині класу.
        
        Викидає RuntimeError якщо зовнішній API недоступний.
        """
        try:
            response = requests.get(
                f"{self._url}{endpoint}",
                headers=self._headers,
                params=params,
                timeout=5,
            )
            response.raise_for_status()  # викидає помилку якщо статус 4xx/5xx
            return response.json()
        except requests.Timeout:
            raise RuntimeError("Geo API не відповідає (timeout).")
        except requests.RequestException as e:
            raise RuntimeError(f"Помилка Geo API: {e}")


# Один екземпляр на весь проект
geo_service = GeoService()