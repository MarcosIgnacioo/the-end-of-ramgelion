from django.db import models
import uuid

from django.contrib.auth.models import User

# Create your models here.


class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=300)
    category = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    stock = models.BigIntegerField()
    discount = models.FloatField()
    stars = models.IntegerField()
    image_url = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.product_name


class OrderedProducts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)


class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    names = models.CharField(max_length=300)
    last_names = models.CharField(max_length=300)
    email = models.EmailField()
    names = models.CharField(max_length=300)
