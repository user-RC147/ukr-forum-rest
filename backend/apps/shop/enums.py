from enum import StrEnum


class ProductStatus(StrEnum):
    NEW = "new"
    USED = "used"


PRODUCT_STATUS_LABELS: dict[ProductStatus, str] = {
    ProductStatus.NEW: "Новий",
    ProductStatus.USED: "Б/В",
}
