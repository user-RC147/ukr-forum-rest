from dataclasses import dataclass
from datetime import datetime
from typing import Sequence


# ==========================================
# DTO ДЛЯ ВИХОДУ (ОПИС ЧИТАННЯ ДАНИХ)
# ==========================================

@dataclass(frozen=True)
class GroupMemberOutDTO:
    """
    DTO учасника групи для відображення (Output).
    Повністю збігається з полями моделі GroupMember.
    """
    id:int
    user_id:int
    username:str
    role:str
    joined_at: datetime




@dataclass(frozen=True)
class GroupOutDTO:
    """
    DTO всієї групи для відображення (Output).
    Збирає в собі шапку групи та вкладений список учасників Sequence.
    """
    id:int
    name:str
    created_by_username: str
    created_at: datetime
    members: Sequence[GroupMemberOutDTO]  # Послідовність учасників для серіалізатора


# ==========================================
# DTO ДЛЯ ВХОДУ (ОПИС СТВОРЕННЯ ГРУПИ)
# ==========================================

@dataclass(frozen=True)
class CreateGroupInDTO:
    name:str
