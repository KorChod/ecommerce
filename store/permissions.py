from rest_framework import permissions

from .models import Role


def is_authenticated_and_has_role(request, role):
    return (request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name=role).exists())


class IsAuthenticatedSellerOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or
                    is_authenticated_and_has_role(request, Role.SELLER.value))


class IsAuthenticatedCustomerOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or
                    is_authenticated_and_has_role(request, Role.CUSTOMER.value))


class IsAuthenticatedSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(is_authenticated_and_has_role(request, Role.SELLER.value))
