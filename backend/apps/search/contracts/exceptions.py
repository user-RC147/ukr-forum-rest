class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class ValidationError(AppError):
    pass


class PermissionAppError(AppError):
    pass


class CategoryNotFoundError(NotFoundError):
    pass


class TagNotFoundError(NotFoundError):
    pass
