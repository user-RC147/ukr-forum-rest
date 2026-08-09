from config.exceptions import NotFoundError, PermissionDeniedError, ValidationError


class CountryNotFoundError(NotFoundError):
    default_message = "Country not found"
    default_code = "country_not_found"


class CountryValidationError(ValidationError):
    default_message = "Country validation failed"
    default_code = "country_validation_error"


class CountryPermissionError(PermissionDeniedError):
    default_message = "Country permission denied"
    default_code = "country_permission_denied"
