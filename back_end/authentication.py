from typing import Tuple
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework import HTTP_HEADER_ENCODING


class CustomJWTAuthentication(JWTAuthentication):
    """Custom JWT Auth class

        Override authenticate method to get access token from cookies
    """
    def authenticate(self, request):
        header = self.get_header(request)
        raw_token = None

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
            if raw_token is not None:
                raw_token = raw_token.encode(HTTP_HEADER_ENCODING)
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
