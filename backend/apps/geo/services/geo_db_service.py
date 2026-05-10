# apps/geo/services/geo_db_service.py

from apps.geo.models import Country, Region, City


def get_or_create_country(api_data: dict) -> Country:
    """
    Знаходить або створює країну в локальній БД.
    api_data — дані з зовнішнього API.
    """
    country, _ = Country.objects.get_or_create(
        code=api_data['code'],
        defaults={
            'name':       api_data['name'],
            'name_ua':    api_data.get('name_ua', ''),
            'flag_emoji': api_data.get('flag_emoji', ''),
            'currency':   api_data.get('currency'),
        }
    )
    return country


def get_or_create_region(api_data: dict, country: Country) -> Region:
    region, _ = Region.objects.get_or_create(
        api_id=api_data['id'],
        defaults={
            'name':    api_data['name'],
            'name_ua': api_data.get('name_ua', ''),
            'country': country,
        }
    )
    return region


def get_or_create_city(api_data: dict, country: Country, region: Region) -> City:
    city, _ = City.objects.get_or_create(
        api_id=api_data['id'],
        defaults={
            'name':      api_data['name'],
            'name_ua':   api_data.get('name_ua', ''),
            'country':   country,
            'region':    region,
            'latitude':  api_data.get('latitude'),
            'longitude': api_data.get('longitude'),
        }
    )
    return city