from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestCollectionCreate:
    def test_if_user_is_anonymous_returns_401(self, api_client: APIClient):
        request = api_client.post('/api/store/collections/', {'title': 'a'})

        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client: APIClient, authenticate):
        authenticate()

        request = api_client.post('/api/store/collections/', {'title': 'a'})

        assert request.status_code == status.HTTP_403_FORBIDDEN
