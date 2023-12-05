from django.shortcuts import get_object_or_404, render, redirect
from .utilities import buy_now, add_to_the_cart
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login, logout, authenticate
from .forms import ProductForm
from .forms import OrderProductForm
from .models import Producto, Carts, CartsItems, PurchasedProducts, RamsesUsers
from django.contrib.auth.hashers import check_password
from .managers import get_current_cart, finish_cart_purchase
# Create your views here.


def home(request):
    products = Producto.objects.all()
    user = request.user
    is_authenticated = user.is_authenticated
    post_info = request.POST

    if request.POST.get('shop') == 'add_to_cart':
        product_id = post_info['product-id']
        product = Producto.objects.get(id=product_id)
        try:
            add_to_the_cart(user, product, 1)
        except Exception as e:
            print(e)
    elif request.POST.get('shop') == 'buy_now':
        quantity = 1
        product_id = post_info['product-id']
        stock = int(post_info['product-stock'])
        product = Producto.objects.get(id=product_id)
        try:
            buy_now(request, product, quantity, stock, user)
        except Exception as e:
            print(e)
    for product in products:
        product.final_price = round(product.final_price, 2)
    return render(request, "index.html", {
        'products': products,
        'iterator': 5
    })


def signup(request):
    if request.method == "GET":
        print("i get it")
        return render(request, "registro.html")
    else:
        post_info = request.POST
        if post_info['password'] == post_info['repeat_password']:
            # Registrando al padrino
            try:
                user = User.objects.create_user(
                    username=post_info['email'],
                    email=post_info['email'],
                    first_name=post_info['name'],
                    password=post_info['password'],
                    last_name=post_info['last_names'])
                user.save()
                ramses_user = RamsesUsers.objects.create(
                    auth_user=user, adress=post_info['adress'], cellphone_number=post_info['cellphone_number'])
                ramses_user.save()
                login(request, user)
                return redirect('home')
            except Exception as e:
                return render(request, "registro.html", {"error": e})
        return render(request, "registro.html", {"error": 'Las contraseñas no coinciden'})


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            post_info = request.POST
            user = authenticate(
                request, username=post_info['email'], password=post_info['password'])
            if user is None:
                return render(request, 'login.html', {"error": "Datos invalidos"})
            else:
                login(request, user)
                return redirect('home')
        except Exception as e:
            return render(request, 'login.html', {"error": e})


def create_products(request):
    if request.method == 'GET':
        return render(request, 'create_product.html', {
            'form': ProductForm
        })
    else:
        form = ProductForm(request.POST)
        if form.is_valid():
            new_prod = form.save(commit=False)
            new_prod.user = request.user
            new_prod.save()
            return render(request, 'create_product.html', {
                'form': ProductForm
            })


def create_orders(request):
    if request.method == 'GET':
        return render(request, 'create_order.html', {
            'form': OrderProductForm
        })
    else:
        form = OrderProductForm(request.POST)
        if form.is_valid():
            new_prod = form.save(commit=False)
            new_prod.user = request.user
            new_prod.save()
            return render(request, 'create_order.html', {
                'form': OrderProductForm
            })


def profile(request):
    if request.method == 'GET':
        user = request.user
        ramses_user = RamsesUsers.objects.get(auth_user=user)
        adress = ramses_user.adress
        cellphone_number = ramses_user.cellphone_number
        return render(request, 'user.html', {
            'user_first_name': user.first_name,
            'user_email': user.email,
            'user_last_names': user.last_name,
            'user_first_name': user.first_name,
            'user_cellphone_number': cellphone_number,
            'user_adress': adress,
        })
    else:
        try:
            user = request.user
            ramses_user = RamsesUsers.objects.get(auth_user=user)

            new_info = request.POST
            new_email = new_info['email']
            new_first_names = new_info['names']
            new_last_names = new_info['last_names']
            actual_password = new_info['actual_password']
            new_password = new_info['new_password']
            confirm_new_password = new_info['confirm_new_password']
            adress = new_info['adress']
            cellphone_number = new_info['cellphone_number']

            if len(new_email) != 0:
                user.username = new_email
                user.email = new_email

            if len(new_first_names) != 0:
                user.first_name = new_first_names

            if len(new_last_names) != 0:
                user.last_name = new_last_names

            if len(actual_password) != 0:
                if (check_password(actual_password, user.password)):
                    if (new_password == confirm_new_password):
                        user.set_password(new_password)
            if len(adress) != 0:
                ramses_user.adress = adress
            if len(cellphone_number) != 0:
                ramses_user.cellphone_number = cellphone_number
            user.save()
            login(request, user)
            ramses_user.save()
            print("porfavor si esto sale vamos masoemnso bien")
            # TODO mandar un response sde que las contrase;as no coinciden
            return redirect('home')
            # return render(request, 'index.html')
        except Exception as e:
            return render(request, "user.html", {"error": e})


def product_details(request, product_id):
    user = request.user
    is_authenticated = user.is_authenticated
    product = Producto.objects.get(pk=product_id)
    stock = product.stock

    if request.method == 'GET':
        # Pasar esto a que sea una funcion que tenga de parametro el producto y retorne un arreglo d todas sus propiedades luego aqui hacerle deestructuring para tenerlo mas clean
        price = product.price
        product_name = product.product_name
        category = product.category
        description = product.description
        discount = product.discount
        stars = product.stars
        image_url = product.image_url
        final_price = round(product.final_price, 2)
        stars_array = []
        for i in range(stars):
            stars_array.append("⭐")

        return render(request, 'product-details.html', {
            'final_price': final_price,
            'is_authenticated': is_authenticated,
            'product_id': product_id,
            'product_name': product_name,
            'price': price,
            'category': category,
            'description': description,
            'stock': stock,
            'discount': discount,
            'stars': stars_array,
            'image_url': image_url
        })
    elif request.POST.get('shop') == 'buy_now':
        quantity = float(request.POST['quantity'])
        product = Producto.objects.get(pk=product_id)

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

    elif request.POST.get('shop') == 'add_to_cart':
        quantity = float(request.POST['quantity'])
        cart = get_current_cart(user)
        current_cart_items = CartsItems.objects.filter(cart=cart)
        is_already_in_cart = False
        already_item = ''
        for cart_item in current_cart_items:
            if cart_item.product == product:
                already_item = cart_item
                is_already_in_cart = True
        print(is_already_in_cart)
        if is_already_in_cart:
            already_item.quantity = already_item.quantity + quantity
            already_item.save()
            return redirect('home')
        else:
            new_cart_addition = CartsItems(cart_id=cart.id, product_id=product.id, quantity=quantity, total=round(
                product.final_price*float(quantity), 4))
            new_cart_addition.save()
            return redirect('home')


def cart(request):
    user = request.user
    is_authenticated = user.is_authenticated
    if is_authenticated == False:
        return redirect('signin')
    current_cart = get_current_cart(user)
    products_in_cart = CartsItems.objects.filter(cart=current_cart)
    unwrapped_products = []
    for p in products_in_cart:
        p.product.final_price = round(p.product.final_price, 2)
        p.product.quantity = p.quantity
        unwrapped_products.append(p.product)

    if request.method == 'GET':
        # Pasar esto a que sea una funcion que tenga de parametro el producto y retorne un arreglo d todas sus propiedades luego aqui hacerle deestructuring para tenerlo mas clean

        return render(request, 'shopping-cart.html', {
            'products': unwrapped_products
        })
    else:
        for p in unwrapped_products:
            final_quantity = float(request.POST[p.product_name])
            purchase = PurchasedProducts(
                user=user, product=p, quantity=final_quantity, total=(p.final_price*final_quantity))
            purchase.save()
            finish_cart_purchase(user)
        return render(request, 'purchase-confirmation.html', {
        })


def purchase_history(request):
    purchase_history = PurchasedProducts.objects.all().filter(user_id=request.user)
    purchase_history = purchase_history[::-1]
    for purchase in purchase_history:
        product = Producto.objects.get(id=purchase.product_id)
        purchase.image_url = product.image_url
        purchase.product_name = product.product_name
    return render(request, 'purchase-history.html', {
        'products': purchase_history
    })


def search(request):
    user = request.user
    products = Producto.objects.all()
    if request.method == "GET":
        return render(request, 'search.html', {
            'products': products
        })
    else:
        searched_products = request.POST['product-search']
        if len(searched_products) == 0:
            for p in products:
                p.final_price = round(p.final_price, 2)
            return render(request, 'search.html', {
                'products': products
            })
        else:
            post_info = request.POST
            if request.POST.get('shop') == 'add_to_cart':
                product_id = post_info['product-id']
                product = Producto.objects.get(id=product_id)
                try:
                    add_to_the_cart(user, product, 1)
                except Exception as e:
                    print(e)

            products = Producto.objects.filter(
                product_name__regex=r'^' + searched_products)
            return render(request, 'search.html', {
                'searched_product': searched_products,
                'products': products
            })
