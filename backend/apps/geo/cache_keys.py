def country_cache_key():
    return "country:all"


def region_by_country_cache_key(country_id: int) -> str:
    return f"region:country:{country_id}"


def city_by_region_cache_key(region_id: int) -> str:
    return f"city:region:{region_id}"
