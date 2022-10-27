from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from . import views

urlpatterns = [
    path("accounts/", views.UserView.as_view()),
    path("login/", views.CustomLogin.as_view()),
    path("accounts/newest/<int:num>/", views.UserView.as_view()),
    path("accounts/<pk>/", views.UpdateUserView.as_view()),
    path("accounts/<pk>/management/", views.SoftDeleteUserView.as_view()),
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView().as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
