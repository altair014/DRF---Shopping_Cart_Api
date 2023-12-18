from random import randrange, randint, choice

from shop_site.settings import SESSION_COOKIE_AGE

from django.contrib.auth import logout, get_user_model

from rest_framework.response import Response

from shop_auth.models import ShopUser


def _keys():
    _admin_key = randrange(999999,2147483646,(randint(1,9))) #for now later will be replaced by o-auth or jwt-auth
    _staff_key = randrange(999999,2147483646,(randint(1,9)))
    _seller_key = randrange(999999,2147483646,(randint(1,9))) #for now later will be replaced by o-auth or jwt-auth
       
    if _admin_key == _staff_key or _admin_key == _seller_key or _staff_key == _seller_key or _admin_key == _staff_key or _admin_key == _seller_key:
        _keys()
   
    return _admin_key, _staff_key, _seller_key

def get_user(request):
    try:
        user = ShopUser.objects.get(email=request.user)
    except ShopUser.DoesNotExist:
        user == None
    return user

def user_object(email, password, model, email_error, password_error, validator):
    try:
        user = model.objects.get(email=email)
    except model.DoesNotExist:
        raise validator(email_error)
    else:
        if user.check_password(raw_password=password):             
            return user 
        else:
            raise validator(password_error)
                
def set_expir(req, timer=SESSION_COOKIE_AGE):
    if req.user.is_authenticated:
        req.session.set_expiry(timer)
    return timer


def cred_auth(req):
    if req.user.is_authenticated:
        user = get_user(request=req)
        logout(request=req)
        cred_data ={'msg':'You have been successfully logged out. Please provide your credentials again to login.'}
    else:
        cred_data={'msg':'Please provide your credentials.'}
    return Response(data = cred_data)

from django.db import connection

def table_exists(table_name):
    existing_tables = connection.introspection.table_names()
    return table_name in existing_tables
