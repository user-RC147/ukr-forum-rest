from apps.geo.models import Country, Region, City


class GeoRepository:

    def get_or_create_country(self, api_data: dict) -> Country:
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

    def get_or_create_region(self, api_data: dict, country: Country) -> Region:
        region, _ = Region.objects.get_or_create(
            api_id=api_data['id'],
            defaults={
                'name':    api_data['name'],
                'name_ua': api_data.get('name_ua', ''),
                'country': country,
            }
        )
        return region

    def get_or_create_city(self, api_data: dict, country: Country, region: Region) -> City:
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


geo_repository = GeoRepository()