class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class ValidationError(AppError):
    pass


class PermissionAppError(AppError):
    pass


class FileValidationError(ValidationError):
    pass


class FileExtensionError(FileValidationError):
    pass


class FileSizeError(FileValidationError):
    pass


class FileNameError(FileValidationError):
    pass


class FileNotFoundError(NotFoundError):
    pass
