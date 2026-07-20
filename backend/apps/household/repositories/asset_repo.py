from django.db import transaction

from apps.household.dto.asset_dto import CreateAssetDTO
from apps.household.models.asset import Asset


class AssetRepo:


    def createAsset(self,dto:CreateAssetDTO,creator_user_id:int)->Asset:
        asset = Asset.objects.create(
            name=dto.name,
            group_id=dto.group_id,
            address_line=dto.address_line,
            created_by_id=creator_user_id,
        )
        return asset