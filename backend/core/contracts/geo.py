from abc import ABC, abstractmethod
from typing import Any,Optional


class IGeoServiceContract(ABC):
    """
    Загальний інтерфейс (контракт) модуля GEO для взаємодії з іншими модулями.
    Всі методи повертають чисті типи даних або DTO, ніяких Django моделей.

    Загальний інтерфейс модуля GEO.
    Дозволяє іншим модулям перевіряти будь-яку комбінацію локації.
    """

    @abstractmethod
    def is_country_exists(self,country_id:int)->bool:
        """Перевірити, чи існує країна з таким ID."""
        pass


    @abstractmethod
    def is_region_exists(self,region_id:int)->bool:
        """Перевірити, чи існує регіон з таким ID."""
        pass

    @abstractmethod
    def is_city_exists(self,city_id:int)->bool:
        """Перевірити, чи існує місто з таким ID."""        
        pass
