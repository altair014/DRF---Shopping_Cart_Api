from django.urls import path

from shop_app.views import UserLogin, UserLogup, SellerCreate, ProductCreate, CartCreate, CartList, ProductList

app_name = 'shop_app_name'

urlpatterns = [
    path(route='user_login/', view=UserLogin.as_view(), name='login_name'),
    path(route='user_logup/', view=UserLogup.as_view(), name='logup_name'),
    path(route='seller_create/', view=SellerCreate.as_view(), name='seller_create_name'),
    path(route='product_create/', view=ProductCreate.as_view(), name='product_create_name'),
    path(route='product_list/', view=ProductList.as_view(), name='product_list_name'),
    path(route='cart_create/', view=CartCreate.as_view(), name='cart_create_name'),
    path(route='cart_list/', view=CartList.as_view(), name='cart_list_name'),
]