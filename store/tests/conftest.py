from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client: APIClient):
    def do_auth(is_staff=False) -> None:
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_auth
