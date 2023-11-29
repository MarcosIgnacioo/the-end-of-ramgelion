from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser

# Create your models here.
class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=300)
    category = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    stock = models.BigIntegerField()
    discount = models.FloatField()
    stars = models.FloatField()

    def __str__(self):
        return self.id
    
class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    names = models.CharField(max_length=300)
    last_names = models.CharField(max_length=300)
    email = models.EmailField()
    names = models.CharField(max_length=300)
 