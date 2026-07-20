from config.exceptions import NotFoundError, ValidationError


class AppValidationError(ValidationError):
    default_message = "Validation failed"
    default_code = "file_validation_error"


class FileValidationError(ValidationError):
    pass


class FileExtensionError(FileValidationError):
    default_message = "Invalid file extension"
    default_code = "file_validation_error"


class FileSizeError(FileValidationError):
    default_message = "Invalid file size"
    default_code = "file_validation_error"


class FileNameError(FileValidationError):
    default_message = "Invalid file name"
    default_code = "file_validation_error"


class FileNotFoundError(NotFoundError):
    default_message = "File not found"
    default_code = "file_not_found"
