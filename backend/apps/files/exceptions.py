class FileValidationError(Exception):
    pass


class FileExtensionError(FileValidationError):
    pass


class FileSizeError(FileValidationError):
    pass


class FileNameError(FileValidationError):
    pass
