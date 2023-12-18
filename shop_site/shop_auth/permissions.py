from rest_framework.permissions import BasePermission

from shop_auth.models import ShopUser

from django.contrib.auth import get_user_model

User = get_user_model()

class IsSeller(BasePermission):

    def has_permission(self, request, view):
        try:
            u = ShopUser.objects.get(email=request.user)
        except ShopUser.DoesNotExist:
            return False
        return bool(request.user and u.is_seller)

class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)