from config.exceptions import NotFoundError, PermissionDeniedError, ValidationError


class ProductNotFoundError(NotFoundError):
    default_message = "Product not found"
    default_code = "product_not_found"


class ProductValidationError(ValidationError):
    default_message = "Product validation failed"
    default_code = "product_validation_error"


class ProductPermissionError(PermissionDeniedError):
    default_message = "Product permission denied"
    default_code = "product_permission_denied"
