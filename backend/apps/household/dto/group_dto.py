from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from apps.household.dto.role_dto import RoleOutDTO
from apps.household.dto.user_dto import User_Id_OutDTO, UserOutDTO


# ==========================================
# DTO ДЛЯ ВИХОДУ (ОПИС ЧИТАННЯ ДАНИХ)
# ==========================================

@dataclass(frozen=True)
class GroupMember_id_user_OutDTO:
    """
    DTO учасника групи для відображення (Output).
    Повністю збігається з полями моделі GroupMember.
    """
    id:int
    group_id:int
    user_id:int
    role:RoleOutDTO
    joined_at: datetime


@dataclass(frozen=True)
class GroupMemberOutDTO:
    """
    DTO учасника групи для відображення (Output).
    Повністю збігається з полями моделі GroupMember.
    """
    id:int
    group_id:int
    user:UserOutDTO
    role:RoleOutDTO
    joined_at: datetime



@dataclass
class Group_Id_Name_OutDTO:
    id:int
    name:str

@dataclass(frozen=True)
class GroupOutDTO:
    """
    DTO всієї групи для відображення (Output).
    Збирає в собі шапку групи та вкладений список учасників Sequence.
    """
    id:int
    name:str
    created_by: UserOutDTO
    created_at: datetime
    members: Sequence[GroupMemberOutDTO]  # Послідовність учасників для серіалізатора


@dataclass(frozen=True)
class Group_id_user_OutDTO:
    """
    DTO всієї групи для відображення (Output).
    Збирає в собі шапку групи та вкладений список учасників Sequence.
    """
    id:int
    name:str
    created_by_id: int
    created_at: datetime
    members: Sequence[GroupMemberOutDTO]  # Послідовність учасників для серіалізатора

# ==========================================
# DTO ДЛЯ ВХОДУ (ОПИС СТВОРЕННЯ ГРУПИ)
# ==========================================

@dataclass(frozen=True)
class CreateGroupInDTO:
    name:str
