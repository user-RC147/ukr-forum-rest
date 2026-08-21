import uuid
from apps.users.dto.user_dto import CreateUserInDTO, UserPrivateOutDTO,UserShortOutDTO,ProfilUserUpdateInDTO
from apps.users.dto import _to_dto_short_user_out
from apps.users.models import CustomUser,ReferralCode,ReferralUsage
from core.dto.users.user_dto import User_Id_PrivateOutDTO

class UserRepo:

    def create(self, dto: CreateUserInDTO,referral_code) -> UserShortOutDTO:
                 
        user = CustomUser.objects.create_user(
            username=dto.username,
            password=dto.password,
            display_name=dto.display_name,
            email=dto.email,
            consent_given=dto.consent_given,
        )

        if referral_code:
            ReferralUsage.objects.create(
                code=referral_code,
                used_by=user,
            )

        return _to_dto_short_user_out(user)
   

    def update_my_profile(self,dto:ProfilUserUpdateInDTO,user_id:int)->UserPrivateOutDTO:
        return UserPrivateOutDTO()
