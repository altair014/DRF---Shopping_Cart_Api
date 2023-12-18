from django.shortcuts import render, redirect

from django.urls import reverse

# Create your views here.

from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView

from rest_framework.views import APIView

from shop_app.serializers import UserLoginSerilaizer, UserCreateModelSerilaizer, SellerModelSerializer, ProductModelSerializer, CartModelSerializer, ActionSerializer

from shop_auth.models import ShopUser

from rest_framework.response import Response

from django.contrib.auth.hashers import make_password, check_password, get_hasher

from shop_auth.backends import CustomBaseBackend

from random import randrange, randint, choice

from django.contrib.auth import get_user_model, authenticate, logout, user_logged_in, user_logged_out, login

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.authentication import BasicAuthentication

from shop_auth.permissions import IsSeller, IsSuperuser

from shop_app.models import Seller, Cart, Product

from time import sleep

from shop_app.utils import _keys, set_expir, cred_auth, get_user

class UserLogin(APIView):
    serializer_class = UserLoginSerilaizer

    def get(self, request, *args, **kwargs):
        return cred_auth(req=request)

    def post(self, request, *args, **kwargs):       
        serializer = self.serializer_class(data=request.POST)

        if serializer.is_valid():                                              
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                set_expir(req=request)
                login(request=request, user=user)
                if ShopUser.objects.get(email=email).is_seller:
                    return redirect(to=reverse(viewname='shop_app_name:product_create_name'))
                return Response(data = {'msg':'Logged In.'})
            else:
                logout(request=request)
                return Response(data = {'msg':'Invalid Email Address or Password.'})
                
        else:
            return Response(data = serializer.errors)
        
class UserLogup(APIView):
    serializer_class = UserCreateModelSerilaizer

    _sup_key, _stf_key, _sel_key = _keys()
         
    def get(self, request, *args, **kwargs):
        print(f"\nAdmin  : {self._sup_key}\nStaff  : {self._stf_key}\nSeller : {self._sel_key}\n")
        return cred_auth(req=request)
       
    def post(self, request, *args, **kwargs):
        serializer = UserCreateModelSerilaizer(data=request.POST)

        if serializer.is_valid():
            data_name = serializer.validated_data
            User = get_user_model()
            key = data_name.pop('key')
            pass_name = data_name.pop('password')
            email_name = data_name.pop('email')  

            user_perm = User.objects.filter(email=email_name)        

            if key == self._sup_key:                
                User.objects.create_superuser(email= email_name, password= pass_name, **data_name)
            else:
                User.objects.create_user(email= email_name, password= pass_name, **data_name)
                sleep(2)
                if key == self._stf_key:
                    user_perm.update(is_staff=1)
                if key == self._sel_key:
                    user_perm.update(is_seller=1)
            return Response(data = {'msg':'User created successfully.'})
        else:
            return Response(data=serializer.errors)

class SellerCreate(CreateAPIView):
    serializer_class = SellerModelSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser, IsSuperuser]
    # authentication_classes = [BasicAuthentication]

class ProductCreate(APIView):
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    authentication_classes = [BasicAuthentication]
    
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.POST)
        
        if serializer.is_valid():
            data = dict(serializer.validated_data)                                         
                       
            try:
                Product.objects.get(**data)
            except Product.DoesNotExist:
                Product.objects.create(**data)
                return Response(data = {'msg':'New Product Added.'})
            else:
                return Response(data = {'msg':'Product Exists.'})
                 
        else:
            return Response(data = serializer.errors)


class ProductList(ListAPIView):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()

class CartCreate(CreateAPIView):
    serializer_class = CartModelSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]
  
class CartList(ListCreateAPIView):
    serializer_class = CartModelSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]
    queryset = Cart.objects.all()
        
    def get(self, request):
        if len(Seller.objects.all()) > 0:
            print(choice(Seller.objects.all()).seller_id)
        if len(Cart.objects.all()) == 0:
            return Response(data={'msg':'Product Not Added.'})
        