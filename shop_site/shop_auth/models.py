from django.db import models
from django.db.models import Model

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from shop_auth.managers import ShopManager

class ShopUser(AbstractBaseUser, PermissionsMixin):
    s_no = models.BigAutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=15)
    phone = models.SmallIntegerField(null=True)
    date_of_birth = models.DateField(max_length=10, null=True)
    email = models.EmailField(max_length=20, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    
    date_joined = models.DateField(auto_now=True)
    last_login = models.DateField(auto_now=True)

    objects = ShopManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"