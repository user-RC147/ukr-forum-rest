import factory
from factory.django import DjangoModelFactory

from ..models import CategoryModel


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = CategoryModel

    name = factory.Faker("sentence")
