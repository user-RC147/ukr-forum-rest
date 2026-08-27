from core.dto.users.user_dto import UserShortOutDTO

from apps.users.dto.user_dto import UserPublicOutDTO,UserPrivateOutDTO

from apps.users.protocols.user_protocol import UserPublicProtocol,UserShortProtocol,UserPrivateProtocol
from apps.users.services.user_service import UserService  


class UserShortContract:
    def __init__(self) -> None:
        self._service = UserService()

    def get(self, user_id: int) -> UserShortOutDTO:
        return self._service.get_user_by_id(user_id)

    def get_many(self, ids: list[int]) -> dict[int,UserShortOutDTO]:
        return self._service.get_many(ids)


def get_user_short_contract() -> UserShortProtocol:
    return UserShortContract()


class UserPublicContract:
    def __init__(self) -> None:
        self._service = UserService()

    def get(self, user_id: int) -> UserPublicOutDTO:
        return self._service.get_user_by_id(user_id)

    def get_many(self, ids: list[int]) -> dict[int,UserPublicOutDTO]:
        return self._service.get_many(ids)

def get_user_public_contract() -> UserPublicProtocol:
    return UserPublicContract()


class UserPrivatContract:
    def __init__(self) -> None:
        self._service = UserService()

    def get(self, user_id: int) -> UserPrivateOutDTO:
        return self._service.get_user_by_id(user_id)

    def get_many(self, ids: list[int]) -> dict[int,UserPrivateOutDTO]:
        return self._service.get_many(ids)

def get_user_privat_contract() -> UserPrivateProtocol:
    return UserPrivatContract()