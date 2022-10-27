from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    seller = UserSerializer(read_only=True)


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
