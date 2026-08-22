import uuid
from apps.users.dto.user_dto import CreateUserInDTO, UserPrivateOutDTO,UserShortOutDTO,ProfilUserUpdateInDTO
from apps.users.dto import _to_dto_short_user_out,_to_dto_id_location_profile
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
   

    def update_my_profile(self,dto:ProfilUserUpdateInDTO,user_id:int)->User_Id_PrivateOutDTO:

        user = CustomUser.objects.get(id=user_id)

        user.display_name = dto.display_name
        user.first_name = dto.first_name
        user.first_name_public = dto.first_name_public

        user.last_name = dto.last_name
        user.last_name_public = dto.last_name_public

        user.email = dto.email
        user.email_public = dto.email_public

        user.date_of_birth = dto.date_of_birth
        user.date_of_birth_public = dto.date_of_birth_public

        user.phone_number = dto.phone_number
        user.phone_public = dto.phone_public

        user.social_network = dto.social_network
        user.social_public = dto.social_public

        user.country_public = dto.country_public
        user.region_public = dto.region_public
        user.city_public = dto.city_public

        user.country_id = dto.location.country_id
        user.region_id = dto.location.region_id
        user.city_id = dto.location.city_id

        print('============================================')
        print("DTO before save:", dto)
        print('============================================')

        user.save()

        return _to_dto_id_location_profile(user)
