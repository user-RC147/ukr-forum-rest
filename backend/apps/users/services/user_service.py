from apps.users.dto.user_dto import (
    UserPrivateUpdateInDTO,
    UserPublicOutDTO,
    UserShortPublicOutDTO,
    UserPrivateOutDTO,
    CreateUserInDTO,
)
from apps.users.exceptions import UserNotFoundException
from apps.users.selectors.user_selector import UserSelector
from apps.users.repositories.user_repository import UserRepo

from apps.users.dto._to_dto_profile import _to_dto_out_profile
from apps.users.dto._to_dto_location import _get_ids_location, _get_locations
from apps.users.dto._to_dto_user import (
    _to_dto_short_public_user_out,
    _to_dto_public_user_out,
)

from apps.geo.contracts import (
    get_country_contract,
    get_region_contract,
    get_city_contract,
)

class UserService:

    def __init__(self):
        self._selector = UserSelector()
        self._repository = UserRepo()

    def get_short_public_user(self, user_id: int) -> UserShortPublicOutDTO:
        user = self._selector.get_short_public(user_id)
        if user is None:
            raise UserNotFoundException(user_id)

        return _to_dto_short_public_user_out(user)

    def get_many_short_public_user(self, ids: set[int] | None) -> list[UserShortPublicOutDTO]:
        users = self._selector.get_many_short_public(ids)
        dto = [_to_dto_short_public_user_out(user) for user in users.values()]
        return dto

    def get_many_public_user(self, ids: set[int] | None) -> list[UserPublicOutDTO]:
        users = self._selector.get_many_users(ids)
        ids = _get_ids_location(users)
        locations = _get_locations(
            ids, get_country_contract(), get_region_contract(), get_city_contract()
        )
        dto = [_to_dto_public_user_out(user, locations) for user in users]
        return dto

    def get_user_by_id(self, user_id) -> UserPublicOutDTO:
        user = self._selector.get_user_by_id(user_id)

        if user is None:
            raise UserNotFoundException(user_id)

        ids = _get_ids_location(user)

        locations = _get_locations(
            ids, get_country_contract(), get_region_contract(), get_city_contract()
        )

        dto = _to_dto_public_user_out(user, locations)
        return dto

    def get_my_profile(self, user_id: int) -> UserPrivateOutDTO:
        my_profile = self._selector.get_my_profile(user_id)

        ids = _get_ids_location(my_profile)

        locations = _get_locations(
            ids, get_country_contract(), get_region_contract(), get_city_contract()
        )

        dto = _to_dto_out_profile(my_profile, locations)

        return dto

    def create(self, dto: CreateUserInDTO) -> bool:
        referral_code = None

        # if dto.referral_code:
        # referral_code = self._selector.get_by_code(dto.referral_code)
        self._repository.create(dto=dto, referral_code=dto.referral_code)

    def update_my_profile(
        self, dto: UserPrivateUpdateInDTO, user_id: int
    ) -> UserPrivateOutDTO:

        my_profile = self._repository.update_my_profile(dto, user_id)

        ids = _get_ids_location(my_profile)

        locations = _get_locations(
            ids, get_country_contract(), get_region_contract(), get_city_contract()
        )

        dto = _to_dto_out_profile(my_profile, locations)
        return dto

    def delete_user(self, user_id: int) -> None:
        self._repository.delete_user(user_id)

        # users_list: list[User_Id_PublicOutDTO] = list(user_all.values())

        # _ids = _get_ids_location(users_list)
        # locations = _get_locations(
        #     _ids, get_country_contract(), get_region_contract(), get_city_contract()
        # )

        # dto = [_to_dto_public_user_out(user, locations) for user in users_list]

        # users_dict = {item.id: item for item in dto}

        # return users_dict
