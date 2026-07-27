
from apps.household.dto.purchase_dto import PurchaseItemInDTO, PurchaseItemOutDTO
from apps.household.repositories.purchase_item_repo import PurchaseItemRepo
from apps.household.selectors.purchase_item_selector import PurchaseItemSelector


class PurchaseItemService:

    def __init__(self,*args, **kwargs):
        super().__init__(**kwargs)
        #self._selector=
        self._repository = PurchaseItemRepo()
        self._selector = PurchaseItemSelector()



    def get_all_purchase_item(self, user_id:int)->list[PurchaseItemOutDTO]:
        return self._selector.get_all_purchase_item(user_id)

    def create(self,dto:PurchaseItemInDTO,creator_id:int):

        pass