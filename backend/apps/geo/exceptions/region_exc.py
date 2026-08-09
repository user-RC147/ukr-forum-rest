from config.exceptions import NotFoundError, PermissionDeniedError, ValidationError


class RegionNotFoundError(NotFoundError):
    default_message = "Region not found"
    default_code = "region_not_found"


class RegionValidationError(ValidationError):
    default_message = "Region validation failed"
    default_code = "region_validation_error"


class RegionPermissionError(PermissionDeniedError):
    default_message = "Region permission denied"
    default_code = "region_permission_denied"
