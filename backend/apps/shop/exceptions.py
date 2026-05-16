class ShopException(Exception):
    pass


class ProductNotFound(ShopException):
    pass


class ProductOutOfStock(ShopException):
    pass


class UnauthorizedException(Exception):
    pass
