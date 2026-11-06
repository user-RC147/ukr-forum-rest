from dataclasses import dataclass
from datetime import datetime

from apps.household.dto.group_dto import Group_id_user_OutDTO, GroupOutDTO
from apps.household.dto.location_dto import (
    Location_Id_InDTO,
    LocationId_Name_OutDTO,
    LocationOutDTO,
)


@dataclass(frozen=True)
class Asset_Id_Group_location_OutDTO:
    id: int
    name: str
    group_id: int
    location: Location_Id_InDTO
    address_line: str
    created_by_id: int
    created_at: datetime


@dataclass(frozen=True)
class Asset_Id_Group_OutDTO:
    id: int
    name: str
    group_id: int
    location: LocationOutDTO
    address_line: str
    created_by_id: int
    created_at: datetime


@dataclass(frozen=True)
class AssetOutDTO:
    id: int
    name: str
    group: GroupOutDTO
    location: LocationOutDTO
    address_line: str
    created_by_id: int
    created_at: datetime


@dataclass(frozen=True)
class AssetId_Name_OutDTO:
    id: int
    name: str
    group: Group_id_user_OutDTO
    location: LocationId_Name_OutDTO
    address_line: str
    created_by_id: int
    created_at: datetime


@dataclass(frozen=True)
class CreateAssetDTO:
    name: str
    group_id: int
    location: Location_Id_InDTO
    address_line: str | None = None  # Може бути рядком або None, за замовчуванням None


@dataclass(frozen=True)
class ListAssetDTO:
    group_id: int | None = None
