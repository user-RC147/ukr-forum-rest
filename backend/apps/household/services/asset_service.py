from apps.household.selectors.asset_selector import AssetSelector
from apps.household.dto.asset_dto import CreateAssetDTO,ListAssetDTO
from apps.household.repositories.asset_repo import AssetRepo


class AssetService:

    def __init__(self)->None:
        self._selector=AssetSelector()
        self._repository=AssetRepo()

    def get_user_assets(self,user_id:int):
        return self._selector.get_available_assets(user_id)
    
    def get_list_asset(self,dto:ListAssetDTO):
        asset_list=self._selector.get_list_asset(dto)
        return asset_list


    def create(self,dto:CreateAssetDTO):
        asset=self._repository.createAsset(dto)
        return asset
