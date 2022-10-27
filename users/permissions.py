from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, user):
        return request.user == user


class IsAdm(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
