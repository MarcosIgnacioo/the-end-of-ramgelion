from django.db.models import QuerySet, Q
from .models import Carts, Producto


def get_current_cart(user):
    user_id = user.id
    user_carts = Carts.objects.filter(Q(user=user_id))
    print("//////////////////////////////////////")
    print(user_carts)
    if (user_carts.filter(Q(is_finished=False)).first() != None):
        return user_carts.filter(Q(is_finished=False)).first()
    else:
        newCart = Carts(user=user, total=0.0)
        newCart.save()
        return newCart


def finish_cart_purchase(user):
    current_cart = get_current_cart(user)
    current_cart.is_finished = True
    current_cart.save()


def get_product_price(product_id):
    product = Producto.objects.get(product_id)
    price = product.price
    discount = (100-(product.discount))/100
    return price*discount
