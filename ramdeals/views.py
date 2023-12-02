from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login, logout, authenticate
from .forms import ProductForm
from .forms import OrderProductForm
from .models import Producto, Carts, CartsItems, PurchasedProducts
from django.contrib.auth.hashers import check_password
from .managers import get_current_cart
# Create your views here.


def home(request):
    products = Producto.objects.all()
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
        print("gamers")
        return render(request, 'user.html', {
            'user_first_name': user.first_name,
            'user_email': user.email,
            'user_last_names': user.last_name,
            'user_first_name': user.first_name,
        })
    else:
        try:
            user = request.user
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
                        print('---------------------------')
                        print("entramos aqui")
                        user.set_password(new_password)
            user.save()
            print("porfavor si esto sale vamos masoemnso bien")
            # TODO mandar un response sde que las contrase;as no coinciden
            # TODO mandar un response de que la contras;ea vieja no coincide

            return render(request, 'index.html')
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

        return render(request, 'product-details.html', {
            'is_authenticated': is_authenticated,
            'product_id': product_id,
            'product_name': product_name,
            'price': price,
            'category': category,
            'description': description,
            'stock': stock,
            'discount': discount,
            'stars': stars,
            'image_url': image_url
        })
    else:
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
            print("//////////////////////////////////////////////////////////")
            print(type(stock))
            print(type(quantity))
            print(e)
            print("//////////////////////////////////////////////////////////")
        return render(request, 'purchase-confirmation.html', {
            'purchases': purchases,
            'subtotal': product.final_price*quantity
        })


def buy_product(request):
    return "holaj"
