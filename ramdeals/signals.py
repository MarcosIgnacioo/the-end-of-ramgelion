from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import CartsItems, Producto, PurchasedProducts, Carts
from django.db.models import Sum


@receiver(post_save, sender=CartsItems)
def set_final_price_on_product_purchase(sender, instance, **kwargs):
    cart = Carts.objects.get(pk=instance.cart.id)
    instance.total = instance.quantity * instance.product.final_price
    cart.total = CartsItems.objects.filter(cart=cart).aggregate(Sum('total'))[
        'total__sum']
    cart.save()


@receiver(pre_save, sender=Producto)
def set_final_price_on_product(sender, instance, **kwargs):
    instance.final_price = (instance.price * ((100-instance.discount)/100))


@receiver(pre_save, sender=PurchasedProducts)
def set_final_price_on_product(sender, instance, **kwargs):
    product = instance.product
    product.stock = product.stock - instance.quantity
    product.save()
