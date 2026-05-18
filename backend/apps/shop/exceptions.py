class ShopException(Exception):
    pass


class ProductNotFound(ShopException):
    pass

class GeoNotFound(Exception):
    pass


class ProductOutOfStock(ShopException):
    pass


class UnauthorizedException(Exception):
    pass
