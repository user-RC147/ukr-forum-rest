from apps.household.selectors.asset_selector import AssetSelector


class AssetService:

    def __init__(self,selector:AssetSelector)->None:
        self._selector=selector

    def get_user_assets(self,user_id:int):
        return self._selector.get_available_assets(user_id)