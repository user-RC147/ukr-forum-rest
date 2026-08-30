import pytest
from rest_framework.test import APIClient

from apps.users.tests.factories import UserFactory

from .factories import ProductFactory


@pytest.mark.django_db
def test_delete_unauth():
    client = APIClient()
    route = "/api/shop/products/"

    product = ProductFactory()

    response = client.delete(route + f"{product.id}/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_delete():
    client = APIClient()
    route = "/api/shop/products/"
    user = UserFactory()
    other_user = UserFactory()
    product1 = ProductFactory(owner_id=user.id)
    product2 = ProductFactory(owner_id=other_user.id)

    client.force_authenticate(user=user)
    response = client.delete(route + f"{product1.id}/")
    assert response.status_code == 204

    check = client.get(route + f"{product1.id}/")

    assert check.status_code == 404

    response = client.delete(route + f"{product2.id}/")
    assert response.status_code == 403
