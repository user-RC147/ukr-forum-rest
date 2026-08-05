from config.exceptions import NotFoundError, PermissionDeniedError, ValidationError


class CityNotFoundError(NotFoundError):
    default_message = "City not found"
    default_code = "city_not_found"


class CityValidationError(ValidationError):
    default_message = "City validation failed"
    default_code = "city_validation_error"


class CityPermissionError(PermissionDeniedError):
    default_message = "City permission denied"
    default_code = "city_permission_denied"
