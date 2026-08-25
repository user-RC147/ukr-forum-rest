from apps.users.models.user import CustomUser
from apps.users.dto.user_dto import UserStarIdOutDTO

from apps.users.dto.user_dto import Location_Id_OutDTO


class StarSelector:

    def get_all_user_grouped(self) -> list[UserStarIdOutDTO]:
        # users = (
        #     CustomUser.objects.values("country_id", "city_id")
        #     .annotate(user_count=Count("id"))
        #     .order_by("country_id", "city_id")
        # )

        dtos = ''
        #[
        #     UserStarIdOutDTO(
        #         id=user.id,
        #         location=Location_Id_OutDTO(
        #             country_id=user.country_id,
        #             region_id=user.region_id,
        #             city_id=user.city_id,
        #         ),
        #     )
        #     for user in users
        # ]

        return dtos | None
