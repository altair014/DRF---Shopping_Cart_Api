from django.db import models
from django.db.models import Model

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

from django.contrib.auth.hashers import make_password


class ShopManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('Please provide a valid and unique email.')
        email = self.normalize_email(email=email)

        shop_user = self.model(email=email,**extra_fields)
        shop_user.password = make_password(password)
        shop_user.save(using=self._db)
        return shop_user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_seller", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_seller", True)
        return self._create_user(email, password, **extra_fields)