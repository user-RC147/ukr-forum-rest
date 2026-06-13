from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional,Sequence # Імпортуємо абстрактну послідовність

@dataclass(frozen=True)
class PurchaseFilterDTO:
    """
    DTO для фільтрації списку чеків.
    Приймає параметри з query-запиту URL (GET-запит).
    """
    asset_id: int  # Обов'язковий фільтр: чеки завжди дивимося в розрізі Об'єкта
    date_from: Optional[date] = None  # Фільтр "від якої дати"
    date_to: Optional[date] = None    # Фільтр "до якої дати"
    market_id: Optional[int] = None   # Фільтр за конкретним магазином


@dataclass(frozen=True)
class PurchaseItemInDTO:
    """
    DTO для одного рядка в таблиці товарів всередині чека.
    Захищає бізнес-рівень від структури DRF-серіалізаторів.
    """
    
    product_id:int
    quantity:Decimal
    price_per_unit:Decimal


@dataclass(frozen=True)
class CreatePurchaseInDTO:
    """
    DTO для всієї форми чека (Шапка + Таблиця товарів).
    Використовує Sequence для гнучкості передачі списків.
    """

    asset_id:int
    market_id:int
    data_purchase:date
    items:Sequence[PurchaseItemInDTO]  # Використовуємо Sequence замість list
    note:str=''



@dataclass(frozen=True)
class PurchaseOutDTO:
    """
    DTO для віддачі даних про чек на фронтенд (Output).
    Включає повні гео-дані магазину для точної синхронізації з Vue.js.
    """
    id:int
    data_purchase:date
    note:str

    # Дані магазину та його повна локація
    market_id:int
    market_name:str
    market_address_line:str
    market_country_id:int
    market_region_id:int
    market_city_id:int

    # Фінансовий підсумок чека
    total_amount: Decimal  # Порахована базою даних загальна сума чека (Разом)