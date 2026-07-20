
from apps.household.dto.purchase_dto import PurchaseItemInDTO
from apps.household.repositories.purchase_item_repo import PurchaseItemRepo


class PurchaseItemService:

    def __init__(self,*args, **kwargs):
        super().__init__(**kwargs)
        #self._selector=
        self._repository = PurchaseItemRepo()


    def create(self,dto:PurchaseItemInDTO,creator_id:int):

        pass