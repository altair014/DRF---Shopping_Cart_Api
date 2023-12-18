from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)