from django.db import models
from django.db.models import Model

# Create your models here.

from random import randrange, randint

from shop_app.utils import table_exists

class Seller(Model):
    s_no = models.BigAutoField(primary_key=True, auto_created=True)
    seller_name = models.CharField(max_length=32)
    seller_email = models.EmailField(max_length=32)
    seller_phone = models.SmallIntegerField()
    seller_address = models.TextField(max_length=300)
    seller_id = models.PositiveSmallIntegerField(unique=True, default=randrange(10000,999999,randint(1,9)))

    def __str__(self):
        return f"{self.seller_id}"

class Product(Model):
    s_no = models.BigAutoField(primary_key=True, auto_created=True)
    product_name = models.CharField(max_length=10)
    brand = models.CharField(max_length=10, help_text='Classmate, Levis, etc.')
    category = models.CharField(max_length=50, help_text='soap, oil, etc.')
    quantity = models.PositiveSmallIntegerField(default=1)
    product_id = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.product_name} by {self.product_id}"

class Cart(Model):
    product_choices = []
    if table_exists('shop_app_product'):
        if len(Product.objects.all()) != 0:
            print('if',product_choices)
            products = Product.objects.all()
            for item in products:
                product_choices.append((item.product_id,item.product_name.lower().capitalize()))
        else:
            print('else',product_choices)
            product_choices.append(('---','---'))
    s_no = models.BigAutoField(primary_key=True, auto_created=True)
    product_name = models.CharField(max_length=10, choices=product_choices)
    product_id = models.PositiveSmallIntegerField(unique=True)
    quantity = models.PositiveSmallIntegerField(default=1)

class Orders(Model):
    s_no = models.BigAutoField(primary_key=True, auto_created=True)
    order_id = models.CharField(max_length=12, unique=True)
    invoice_no = models.CharField(max_length=32, unique=True)
    date_of_purchase = models.DateField(auto_created=True,auto_now_add=True)
    return_status = models.BooleanField(default=False)
    product_name = models.CharField(max_length=10)
    seller_id = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveSmallIntegerField(default=1)    

