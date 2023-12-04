from django.db import models
import uuid
from django.contrib.auth.models import User


class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=300)
    category = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    discount = models.FloatField()
    final_price = models.FloatField(default=0.0)
    stock = models.BigIntegerField()
    stars = models.IntegerField()
    image_url = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.product_name


class Carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)


class CartsItems(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.FloatField(default=0)


class PurchasedProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.FloatField()


class OrderedProducts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)


class ProductsCarts(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    amount = models.FloatField()


class RamsesUsers(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    adress = models.CharField(max_length=300)
    cellphone_number = models.CharField(max_length=300)
