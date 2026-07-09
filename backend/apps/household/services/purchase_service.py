from apps.household.dto.purchase_dto import CreatePurchaseInDTO

# ПОЯСНЕННЯ ДІЇ: Використовуємо створені нами точки входу (__init__.py -> __all__)
# Тепер нам не треба писати довжелезні шляхи до кожного окремого файлу.
from apps.household.repositories.purchase_repo import PurchaseRepo
from apps.household.selectors.group_selector import GroupSelector

# Моделі залишаємо через пряме посилання, щоб уникнути циклічних імпортів Django
from apps.household.models.purchase import Purchase


class PurchaseService:
    """
    Сервіс для управління бізнес-логікою чеків.
    Об'єднує перевірку прав доступу групи та запис чека в базу даних.
    """

    def __init__(self,*args, **kwargs):
        super().__init__(**kwargs)       
        self._repository=PurchaseRepo()
        self._group_selector=GroupSelector()


    def create_purchase(self,dto:CreatePurchaseInDTO,user)->Purchase:
        """
        Бізнес-процес створення чека з попередньою перевіркою ролей учасника.
        """
        # Звертаємося через self._group_selector
        has_write_access=self._group_selector.has_write_access_to_asset(
            user_id=user.id,
            asset_id=dto.asset_id
        )

        if not has_write_access:
            raise PermissionError(
                "У вас немає прав для внесення витрат до цього Об'єкта. "
                "Користувачі з роллю Глядач (VIEWER) не можуть створювати чеки."
            )
        
        # Звертаємося через self._repo
        return self._repository.create_with_items(dto=dto,user_id=user.id)