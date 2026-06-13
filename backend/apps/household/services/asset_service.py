from apps.household.selectors.asset_selector import AssetSelector
from apps.household.dto.asset_dto import CreateAssetDTO
from apps.household.repositories.asset_repo import AssetRepo


class AssetService:

    def __init__(self,selector:AssetSelector,repository:AssetRepo)->None:
        self._selector=selector
        self._repository=repository

    def get_user_assets(self,user_id:int):
        return self._selector.get_available_assets(user_id)
    

    def create(self,dto:CreateAssetDTO):
        asset=self._repository.createAsset(dto)
        return asset