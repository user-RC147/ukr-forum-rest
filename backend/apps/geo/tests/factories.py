import factory
from factory.django import DjangoModelFactory

from apps.geo.models.city_model import CityModel
from apps.geo.models.country_model import CountryModel
from apps.geo.models.region_model import RegionModel


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = CountryModel

    name = factory.Faker("sentence")
    name_ua = factory.Faker("sentence")
    code = factory.Faker("pystr", min_chars=2, max_chars=5)


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = RegionModel

    name = factory.Faker("sentence")

    country = factory.SubFactory(CountryFactory)


class CityFactory(DjangoModelFactory):
    class Meta:
        model = CityModel

    name = factory.Faker("sentence")

    country = factory.SubFactory(CountryFactory)
    region = factory.SubFactory(
        RegionFactory,
        country=factory.SelfAttribute("..country"),
    )

    latitude = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=6,
        positive=True,
    )
    longitude = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=6,
        positive=True,
    )
