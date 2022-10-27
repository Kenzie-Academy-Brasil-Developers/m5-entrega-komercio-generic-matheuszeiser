from rest_framework import permissions

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller


class IsProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, product):
        return product.seller == request.user
