from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import Request, Response, status
from rest_framework.authentication import TokenAuthentication
from users.permissions import IsAccountOwner, IsAdm

from users.serializers import UserSerializer, LoginSerializer, SoftDeleteSerializer

from .models import User


class CustomLogin(ObtainAuthToken):
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if not user:
            return Response(
                {"detail": "invalid username or password"}, status.HTTP_403_FORBIDDEN
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects

    def get_queryset(self):
        if self.kwargs:
            list_users = self.kwargs["num"]
            return self.queryset.order_by("-date_joined")[:list_users]
        return User.objects.all()


class UpdateUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAccountOwner]

    serializer_class = UserSerializer
    queryset = User.objects

    def perform_update(self, serializer):

        user = get_object_or_404(User, id=self.kwargs[self.lookup_field])
        self.check_object_permissions(self.request, user)
        serializer.save()


class SoftDeleteUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdm]

    serializer_class = SoftDeleteSerializer
    queryset = User.objects.all()
