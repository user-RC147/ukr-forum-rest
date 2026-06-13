from tokenize import group
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