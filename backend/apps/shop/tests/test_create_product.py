import pytest
from rest_framework.test import APIClient

from apps.users.tests.factories import UserFactory

from .factories import ProductPostFactory


@pytest.mark.django_db
def test_create_unauth():
    client = APIClient()
    route = "/api/shop/products/"

    product = ProductPostFactory()

    response = client.post(route, product)

    assert response.status_code == 401


@pytest.mark.django_db
def test_create():
    client = APIClient()
    route = "/api/shop/products/"
    user = UserFactory()
    product = ProductPostFactory()

    client.force_authenticate(user=user)
    response = client.post(route, product)
    assert response.status_code == 201

    assert response.data["title"] == product["title"]
