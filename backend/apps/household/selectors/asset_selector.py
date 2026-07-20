from apps.household.dto import ListAssetDTO
from apps.household.models.asset import Asset


class AssetSelector:
    """
    Селектор для читання активів (об'єктів).
    """
    def get_available_assets(self,user_id:int)->list[Asset]:
        """
        Повертає активи груп, у яких користувач є учасником (Власник, Редактор або Глядач).
        """
        asset_list=list(
            Asset.objects.filter(group__members__user_id=user_id)
                                .select_related('group').distinct())
        return asset_list
    
    def get_list_asset(self,dto:ListAssetDTO)->list[Asset]:
        """
        Повертає список активів (Asset), які належать до конкретної групи.
        """
        # Фільтруємо поле group_id значенням, яке лежить всередині DTO
        if dto.group_id is not None:
            
            asset_list = list(Asset.objects.filter(group_id=dto.group_id))
           
        else:
            # Варіант Б: Обрано "Всі групи" (group_id є None)
            # Фільтруємо активи, чия група містить нашого користувача в учасниках (members)

            asset_list=list(
                Asset.objects.filter(group__members__user_id=dto.user_id).distinct()
            )
       
        return asset_list