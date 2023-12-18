from django.contrib.admin import ModelAdmin, site

from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.

class UserAdmin(ModelAdmin):
    fields = ['name','phone','email', 'password','date_of_birth','is_staff','is_superuser','is_active','groups','user_permissions']

site.register(model_or_iterable = User, admin_class=UserAdmin)