from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
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
                print(type(post_info['password']))
                print()
                user = User.objects.create_user(
                    username=post_info['name'],first_name=post_info['name'], password=post_info['password'])
                user.save()
                login(request,user)
                return redirect('home')
            except Exception as e:
                return render(request, "registro.html",{ "error":e })
        return render(request, "registro.html", { "error":'Las contraseñas no coinciden' })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    return render(request, 'login.html')