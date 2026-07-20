class AppError(Exception):
    """Base exception for service
    Extra logging in custom_exception_handler.py.
    """

    default_message = "Application error occurred"
    default_code = "app_error"

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
        extra: dict | None = None,
    ):
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.extra = extra or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    '''Auto logging in custom_exception_handler.py'''
    default_message = "Resource not found"
    default_code = "not_found"


class ValidationError(AppError):
    '''Auto logging in custom_exception_handler.py'''
    default_message = "Validation failed"
    default_code = "validation_error"

    def __init__(
        self, message=None, *, errors: dict[str, list[str]] | None = None, **kwargs
    ):
        super().__init__(message, **kwargs)
        self.errors = errors or {}


class PermissionDeniedError(AppError):
    '''Auto logging in custom_exception_handler.py'''
    default_message = "Permission denied"
    default_code = "permission_denied"


class ConflictError(AppError):
    '''Auto logging in custom_exception_handler.py'''
    default_message = "Conflict with current state"
    default_code = "conflict"
