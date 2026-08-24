from apps.household.dto import ListAssetDTO
from apps.household.dto.asset_dto import Asset_Id_Group_location_OutDTO, AssetOutDTO,Asset_Id_Group_OutDTO
from apps.household.dto.group_dto import Group_id_user_OutDTO
from apps.household.models.asset import Asset
from apps.household.dto.location_dto import LocationOutDTO,Location_Id_InDTO,Location_Id_OutDTO,LocationShortOutDTO,CountryNameOutDTO

from django.db.models import Q


class AssetSelector:
    """
    Селектор для читання активів (об'єктів).
    """
    def get_available_assets(self,user_id:int)->list[Asset_Id_Group_location_OutDTO]:
        """
        Повертає активи груп, у яких користувач є учасником (Власник, Редактор або Глядач).
        """
        asset_list=list(
            Asset.objects.filter(group__members__user_id=user_id)
                                .select_related('group').distinct())
        return asset_list
    
    def get_list_asset(self,dto:ListAssetDTO,user_id:int)->list[Asset_Id_Group_location_OutDTO]:
        """
        Повертає список активів (Asset), які належать до конкретної групи.
        """
        # Фільтруємо поле group_id значенням, яке лежить всередині DTO
   
        if dto.group_id is not None:
            


            asset_list = Asset.objects.filter(
                Q(group_id=dto.group_id) &
                (Q(group__members__user_id=user_id) |
                Q(group__created_by_id=user_id))
                ).distinct()
         
        else:
            # Варіант Б: Обрано "Всі групи" (group_id є None)
            # Фільтруємо активи, чия група містить нашого користувача в учасниках (members)

            asset_list=list(
                Asset.objects.filter(
                    Q(group__members__user_id=user_id) |
                    Q(group__created_by_id=user_id)
                    ).distinct()
            )

        dto = [Asset_Id_Group_location_OutDTO(
            id=asset.id,
            name=asset.name,
            group_id=asset.group_id,
            location=_to_location_id_asset(asset),
            address_line=asset.address_line,
            created_by_id=asset.created_by_id,
            created_at=asset.created_at

        )for asset in asset_list]
        
        return dto




def _to_location_id_asset(data)->Location_Id_OutDTO:
    return Location_Id_OutDTO(
        country_id=data.country_id,
        region_id=data.region_id,
        city_id=data.city_id
    )
