from rest_framework import permissions

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_seller


class IsProductOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, product):
        return request.method in SAFE_METHODS or product.seller == request.user
