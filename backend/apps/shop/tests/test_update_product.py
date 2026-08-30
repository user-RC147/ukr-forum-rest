import pytest
from rest_framework.test import APIClient

from apps.users.tests.factories import UserFactory

from .factories import ProductFactory, ProductPostFactory


@pytest.mark.django_db
def test_update_unauth():
    """patch"""

    client = APIClient()
    route = "/api/shop/products/"
    product = ProductFactory()

    data = ProductPostFactory()

    response = client.patch(route + f"{product.id}/", data)

    assert response.status_code == 401


@pytest.mark.django_db
def test_update():
    """patch"""

    client = APIClient()
    route = "/api/shop/products/"
    user = UserFactory()
    other_user = UserFactory()
    product1 = ProductFactory(owner_id=user.id)
    product2 = ProductFactory(owner_id=other_user.id)
    data = ProductPostFactory()

    client.force_authenticate(user=user)
    response = client.patch(route + f"{product1.id}/", data)
    assert response.status_code == 200

    assert response.data["id"] == product1.id
    product1.refresh_from_db()
    assert product1.title == data["title"]
    assert product1.description == data["description"]
    assert product1.status == data["status"]
    assert product1.category_id == data["category_id"]
    assert product1.city_id == data["city_id"]

    response = client.patch(route + f"{product2.id}/", data)
    assert response.status_code == 403
