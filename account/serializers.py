from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TokenObtainSerializer(TokenObtainPairSerializer):
    keep_me_signed_in = serializers.BooleanField(
        default=False, write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        keep_me_signed_in = attrs.get('keep_me_signed_in')

        if keep_me_signed_in is not None:
            data['keep_me_signed_in'] = keep_me_signed_in
        return data


class TokenRefreshWithCookieSerializer(TokenRefreshSerializer):
    refresh = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        request: Request = self.context['request']
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token is None:
            raise TokenError('Refresh token cookie not provided.')

        try:
            refresh = RefreshToken(refresh_token)  # type: ignore
            data = {'access': str(refresh.access_token)}

            if api_settings.ROTATE_REFRESH_TOKENS:
                if self.context['view'].api_settings.BLACKLIST_AFTER_ROTATION:
                    try:
                        refresh.blacklist()
                    except AttributeError:
                        pass

                refresh.set_jti()
                refresh.set_exp()
                data['refresh'] = str(refresh)

            return data
        except TokenError as e:
            raise ValidationError(e.args[0])


class MergeAnonymousCartSerializer(serializers.Serializer):
    anonymous_cart_id = serializers.UUIDField(default=None, allow_null=True)

    def validate(self, attrs):
        return attrs
