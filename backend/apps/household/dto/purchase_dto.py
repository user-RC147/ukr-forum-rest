from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional,Sequence

from apps.household.dto.asset_dto import AssetId_Name_OutDTO, AssetOutDTO
from apps.household.dto.market_dto import Market_Id_Name_OutDTO, MarketFullOutDTO
from apps.household.dto.product_dto import ProductOutDTO # Імпортуємо абстрактну послідовність

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
    data_purchase:datetime
    items:list[PurchaseItemInDTO]   # Використовуємо Sequence замість list
    note:str=''

@dataclass(frozen=True)
class PurchaseItemOutDTO:
    id:int
    purchase_id:int
    product:ProductOutDTO
    quantity:Decimal
    price_per_unit:Decimal
    total_price:Decimal



@dataclass(frozen=True)
class PurchaseOutDTO:
    """
    DTO для віддачі даних про чек на фронтенд (Output).
    Включає повні гео-дані магазину для точної синхронізації з Vue.js.
    """
    id:int
    data_purchase:datetime
    note:str
    asset:AssetOutDTO
    market:MarketFullOutDTO
    created_at:datetime
    created_by_id:int

    items:list[PurchaseItemInDTO]

    # Фінансовий підсумок чека
    total_amount: Decimal  # Порахована базою даних загальна сума чека (Разом)



@dataclass(frozen=True)
class Purchase_Id_Name_OutDTO:
    """
    DTO для віддачі даних про чек на фронтенд (Output).
    Включає повні гео-дані магазину для точної синхронізації з Vue.js.
    """
    id:int
    data_purchase:date
    note:str
    asset:list[AssetId_Name_OutDTO]
    market:list[Market_Id_Name_OutDTO]
    created_at:datetime
    created_by_id:int

    items:list[PurchaseItemInDTO]

    # Фінансовий підсумок чека
    total_amount: Decimal  # Порахована базою даних загальна сума чека (Разом)