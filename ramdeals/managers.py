from django.db.models import QuerySet, Q
from .models import Carts, Producto


def get_current_cart(user_id):
    return Carts.objects.filter(Q(is_finished=False) & Q(user=user_id)).first()


def finish_cart_purchase(user_id):
    current_cart = get_current_cart(user_id)
    current_cart.is_finished = True
    current_cart.save


def get_product_price(product_id):
    product = Producto.objects.get(product_id)
    price = product.price
    discount = (100-(product.discount))/100
    return price*discount
