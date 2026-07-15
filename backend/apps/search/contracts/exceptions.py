from config.exceptions import NotFoundError, PermissionDeniedError


class PermissionAppError(PermissionDeniedError):
    pass


class CategoryNotFoundError(NotFoundError):
    default_message = "Category not found"
    default_code = "category_not_found"


class TagNotFoundError(NotFoundError):
    default_message = "Tag not found"
    default_code = "tag_not_found"
