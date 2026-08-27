from typing import Protocol

from core.dto.users.user_dto import UserShortOutDTO

from apps.users.dto.user_dto import UserPrivateOutDTO, UserPublicOutDTO


class UserShortProtocol(Protocol):
    def get(self, user_id: int) -> UserShortOutDTO | None: ...
    def get_many(self, ids: list[int]) -> dict[int,UserShortOutDTO]: ...


class UserPublicProtocol(Protocol):
    def get(self, user_id: int) -> UserPublicOutDTO | None: ...
    def get_many(self, ids: list[int]) -> dict[int,UserPublicOutDTO]: ...


class UserPrivateProtocol(Protocol):
    def get(self, user_id: int) -> UserPrivateOutDTO | None: ...
    def get_many(self, ids: list[int]) -> dict[int,UserPrivateOutDTO]: ...
