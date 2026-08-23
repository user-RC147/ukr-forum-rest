from apps.users.dto.user_dto import ProfilUserUpdateInDTO
from apps.users.selectors.user_selector import UserSelector
from apps.users.repositories.user_repository import UserRepo

from apps.users.dto import (
    _to_dto_short_user_out,
    UserPrivateOutDTO,
    CreateUserInDTO
)

from apps.users.dto._to_dto_profile import _to_dto_out_profile
from apps.users.dto._to_dto_location import _get_ids_location, _get_locations

from apps.geo.contracts import (
    get_country_contract,
    get_region_contract,
    get_city_contract,
)

from core.dto.users.user_dto import UserShortOutDTO

from core.func_print import prt

class UserService:

    def __init__(self):
        self._selector = UserSelector()
        self._repository = UserRepo()

    def get_many(self, ids: list[int]) -> dict[int, UserShortOutDTO]:
        return self._selector.get_many(ids)

    def get_all_user(self) -> list[UserShortOutDTO]:
        users = self._selector.get_all_users()
        dto = [_to_dto_short_user_out(user) for user in users]
        return dto

    def get_user_by_id(self, user_id) -> UserShortOutDTO:
        user = self._selector.get_user_by_id(user_id)
        dto = _to_dto_short_user_out(user)
        return dto

    def get_my_profile(self, user_id: int) -> UserPrivateOutDTO:
        my_profile = self._selector.get_my_profile(user_id)
      
        ids = _get_ids_location(my_profile)

      
        locations = _get_locations(
            ids, get_country_contract(), get_region_contract(), get_city_contract()
        )

        
   

        dto = _to_dto_out_profile(my_profile, locations)
    
        return dto

    def create(self, dto: CreateUserInDTO) -> UserShortOutDTO:
        referral_code = None

        #if dto.referral_code:
            #referral_code = self._selector.get_by_code(dto.referral_code)

        return self._repository.create(dto=dto,referral_code=dto.referral_code)

    def update_my_profile(self, dto:ProfilUserUpdateInDTO, user_id: int) -> UserPrivateOutDTO:

        my_profile = self._repository.update_my_profile(dto, user_id)

        ids = _get_ids_location(my_profile)

        locations = _get_locations(
            ids, get_country_contract(), get_region_contract(), get_city_contract()
        )

        dto = _to_dto_out_profile(my_profile, locations)
        return dto


    def delete_user(self, user_id:int)->None:
        self._repository.delete_user(user_id)
        