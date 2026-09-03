from dataclasses import dataclass
from datetime import datetime

from core.dto.users.user_dto import UserShortOutDTO


@dataclass(frozen=True)
class ArticleInDTO: ...



@dataclass(frozen=True)
class ArticleIdOutDTO:
    id: int
    title: str
    description: str
    date_create: datetime
    date_edit: datetime
    created_by_id: int


@dataclass(frozen=True)
class ArticleOutDTO:
    id: int
    title: str
    description: str
    date_create: datetime
    date_edit: datetime
    created_by: UserShortOutDTO
