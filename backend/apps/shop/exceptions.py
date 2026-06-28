class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class ValidationError(AppError):
    pass


class PermissionAppError(AppError):
    pass


class ProductNotFoundError(NotFoundError):
    pass


class GeoNotFound(Exception):
    pass


class ProductPermissionError(PermissionAppError):
    pass
