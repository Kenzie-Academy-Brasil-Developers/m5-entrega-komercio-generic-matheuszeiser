from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product
from .permissions import IsProductOwnerOrReadOnly, IsSellerOrReadOnly
from .serializers import ListProductSerializer, ProductSerializer


class ListCreateProductView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductSerializer
        return ListProductSerializer


class UpdateRetrieveProductView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProductOwnerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
