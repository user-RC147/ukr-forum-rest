from apps.users.models import CustomUser,ReferralUsage

from apps.users.models.password_reset_token import PasswordResetToken
from apps.users.models.referral_code import ReferralCode
from apps.users.dto.user_dto import User_Id_PrivateOutDTO, UserShortOutDTO

from apps.users.dto._to_dto_user import _to_dto_short_user_out
from apps.users.dto._to_dto_profile import _to_dto_id_location_profile


from core.func_print import prt

class UserSelector:

    def get_by_code(self,dto)->bool:

        ref_code = ReferralCode.objects.get(code=dto)

        return  ref_code
      

    def get_my_profile(self,user_id:int)->User_Id_PrivateOutDTO:        

        my_profile = CustomUser.objects.get(id=user_id)      
        
        return _to_dto_id_location_profile(my_profile)
    

    def get_many(self,ids: set[int] | list[int],) -> dict[int,UserShortOutDTO]:

        users = CustomUser.objects.filter(id__in=ids)

        return {user.id:_to_dto_short_user_out(user)for user in users}


    def get_all_users(self) -> list[UserShortOutDTO]:

        users = CustomUser.objects.all()

        dto = [_to_dto_short_user_out(user) for user in users]

        return dto

    def get_user_by_id(self, user_id: int) -> UserShortOutDTO:

        user = CustomUser.objects.get(id=user_id)
        
        dto = _to_dto_short_user_out(user)

        return dto


    def get_password_reset_token(self, token) -> PasswordResetToken | None:
        return PasswordResetToken.objects.filter(token=token).first()



    def find_by_email(self, email: str) -> int | None:
        user = CustomUser.objects.filter(email=email).first()
        return user.id if user else None


