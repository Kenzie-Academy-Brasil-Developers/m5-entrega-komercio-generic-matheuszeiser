from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "password",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]
        read_only_fields = ["is_superuser", "updated_at", "date_joined", "is_active"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class SoftDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
        ]
        read_only_fields = [
            "is_superuser",
            "updated_at",
            "date_joined",
            "username",
            "first_name",
            "last_name",
            "is_seller",
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
