import factory
from factory.django import DjangoModelFactory
from apps.users.models.user import CustomUser

class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ("username",)
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Faker("email")
    display_name = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")