from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer, ValidationError

from shop_auth.models import ShopUser

from shop_app.models import Product, Seller, Cart, Orders

# from django.contrib.auth import authenticate


class UserLoginSerilaizer(Serializer):
    email = serializers.EmailField(max_length=20)
    password = serializers.CharField(max_length=20, style={'input_type': 'password'})

    def validate_email(self, value):                                 
        try:
            user = ShopUser.objects.get(email=value)
        except ShopUser.DoesNotExist:
            raise ValidationError(f'User account {value} not found.')
        else:
            return value

        
class UserCreateModelSerilaizer(ModelSerializer):
    key = serializers.IntegerField(initial=0)
    
    class Meta:
        model = ShopUser
        fields = ['name','phone','email', 'password','date_of_birth','key']
        extra_kwargs = {
                        'date_of_birth': {'label': 'Date of Birth'},
                        'password': {
                                        'style':{'input_type': 'password'}
                                    }
                        }

class SellerModelSerializer(ModelSerializer):
    class Meta:
        model = Seller
        exclude = ('s_no','seller_id')

class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ('s_no', 'product_id')

class CartModelSerializer(ModelSerializer):
    class Meta:
        model = Cart
        exclude = ('s_no', 'product_id')

class ActionSerializer(Serializer):
    FIELDNAME = serializers.BooleanField()
