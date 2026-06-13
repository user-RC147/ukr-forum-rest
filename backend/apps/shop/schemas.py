from drf_spectacular.utils import extend_schema
from apps.shop.serializers import ProductReadSerializer
product_create_schema = extend_schema(
    summary="Створити товар",
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'title':       {'type': 'string'},
                'description': {'type': 'string'},
                'price':       {'type': 'integer'},
                'country_id':  {'type': 'integer'},
                'region_id':   {'type': 'integer'},
                'city_id':     {'type': 'integer'},
                'files': {
                    'type': 'array',
                    'items': {'type': 'string', 'format': 'binary'}
                },
            }
        }
    },
    responses={201: ProductReadSerializer},
)

product_update_schema = extend_schema(
    summary="Редагувати товар",
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'title':       {'type': 'string'},
                'description': {'type': 'string'},
                'price':       {'type': 'integer'},
                'country_id':  {'type': 'integer'},
                'region_id':   {'type': 'integer'},
                'city_id':     {'type': 'integer'},
                'files': {
                    'type': 'array',
                    'items': {'type': 'string', 'format': 'binary'}
                },
            }
        }
    },
    responses={200: ProductReadSerializer},
)

product_list_schema = extend_schema(
    summary="Список продуктів",
    responses={200: ProductReadSerializer(many=True)},
)