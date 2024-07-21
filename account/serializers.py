from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TokenObtainSerializer(TokenObtainPairSerializer):
    keep_me_signed_in = serializers.BooleanField(default=False, write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        keep_me_signed_in = attrs.get('keep_me_signed_in')

        if keep_me_signed_in is not None:
            data['keep_me_signed_in'] = keep_me_signed_in
        return data
