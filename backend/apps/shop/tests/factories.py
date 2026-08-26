import factory
from factory.django import DjangoModelFactory

from apps.users.tests.factories import UserFactory

from ..models import ProductModel


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = ProductModel

    title = factory.Faker("sentence", nb_words=2)
    description = factory.Faker("text")
    price = factory.Sequence(lambda n: n * 10)

    owner_id = factory.LazyFunction(lambda: UserFactory().id)
    category_id = 1

    # country_id = models.PositiveIntegerField(blank=False, null=True)
    # region_id = models.PositiveIntegerField(null=True)
    # city_id = models.PositiveIntegerField(blank=False, null=True)
