from config.exceptions import NotFoundError, PermissionDeniedError


class ProductNotFoundError(NotFoundError):
    default_message = "Product not found"
    default_code = "product_not_found"


class ProductPermissionError(PermissionDeniedError):
    default_message = "Product permission denied"
    default_code = "product_permission_denied"
