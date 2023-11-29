from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import ProductForm
from .forms import OrderProductForm
# Create your views here.


def home(request):
    return render(request, "index.html")


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
                    first_name=post_info['name'],
                    password=post_info['password'])
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
