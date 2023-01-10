from api.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserBasicAuthSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        max_length=100, write_only=True, allow_blank=False, allow_null=False
    )


class UserAuthResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
