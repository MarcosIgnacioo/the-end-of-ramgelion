from ramdeals.models import PurchasedProducts
from django.shortcuts import get_object_or_404, render, redirect
from .managers import get_current_cart
from .models import CartsItems


def buy_now(request, product, quantity, stock, user):
    print(type(product))
    print("///////////////////////////////////////////////////////")
    print("///////////////////////////////////////////////////////")
    print("///////////////////////////////////////////////////////")
    print("///////////////////////////////////////////////////////")
    print("///////////////////////////////////////////////////////")
    print("///////////////////////////////////////////////////////")
    print(round(product.final_price*float(quantity), 4))
    purchases = [
        {
            'product': product,
            'quantity': quantity,
            'subtotal': round(product.final_price*float(quantity), 4)
        },
    ]
    try:
        if (quantity > stock):
            quantity = stock
        new_purchase = PurchasedProducts(
            user=user, product=product, quantity=quantity, total=quantity*product.final_price*float(quantity))
        new_purchase.save()
    except Exception as e:
        print("De seguro esto no sale mal")
        print(e)
    return render(request, 'purchase-confirmation.html', {
        'purchases': purchases,
        'subtotal': product.final_price*quantity
    })


def add_to_the_cart(user, product, quantity):
    cart = get_current_cart(user)
    new_cart_addition = CartsItems(cart_id=cart.id, product_id=product.id, quantity=quantity, total=round(
        product.final_price*float(quantity), 4))
    new_cart_addition.save()
    return redirect('home')
