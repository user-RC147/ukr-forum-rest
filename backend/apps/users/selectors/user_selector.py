from apps.users.models.user import CustomUser
from apps.users.dto.user_dto import User_Id_PrivateOutDTO, UserShortOutDTO

from apps.users.dto._to_dto_user import _to_dto_short_user_out
from apps.users.dto._to_dto_profile import _to_dto_id_location_profile


class UserSelector:

    def get_my_profile(self,user_id:int)->User_Id_PrivateOutDTO:        

        my_profile = CustomUser.objects.get(id=user_id)      
        
        return _to_dto_id_location_profile(my_profile)
    

    def get_many(self, ids: list[int]) -> list[UserShortOutDTO]:
        return None

    def get_all_users(self) -> list[UserShortOutDTO]:

        users = CustomUser.objects.all()

        dto = [_to_dto_short_user_out(user) for user in users]

        return dto

    def get_user_by_id(self, user_id: int) -> UserShortOutDTO:

        user = CustomUser.objects.get(id=user_id)

        dto = _to_dto_short_user_out(user)

        return dto

