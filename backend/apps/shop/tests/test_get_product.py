import pytest
from rest_framework.test import APIClient

from apps.users.tests.factories import UserFactory

from .factories import ProductFactory


@pytest.mark.django_db
def test_get_many_unauth():
    client = APIClient()
    route = "/api/shop/products/"
    user = UserFactory()
    product1 = ProductFactory()
    product2 = ProductFactory()

    response = client.get(route)
    assert response.status_code == 200
    assert response.data["count"] == 2
    assert response.data["items"][0]["id"] == product1.id
    assert response.data["items"][1]["id"] == product2.id

    response = client.get(route + f"?user_id={user.id}")
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_many():
    client = APIClient()
    route = "/api/shop/products/"
    user = UserFactory()
    other_user = UserFactory()
    product1 = ProductFactory(owner_id=user.id)
    ProductFactory(owner_id=other_user.id)

    client.force_authenticate(user=user)
    response = client.get(route + f"?user_id={user.id}")
    assert response.status_code == 200

    assert response.data["count"] == 1
    assert response.data["items"][0]["id"] == product1.id

    response = client.get(route + f"?user_id={other_user.id}")
    assert response.status_code == 403
