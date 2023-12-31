"""
URL configuration for venysanamidolorcrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ramdeals import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create-product/', views.create_products, name='create-product'),
    path('create-order/', views.create_orders, name='create-order'),
    path('profile/', views.profile, name='profile'),
    path('product-details/<uuid:product_id>/',
         views.product_details, name='product-details'),
    path('shopping-cart/', views.cart, name='shopping-cart'),
    path('purchase-history/', views.purchase_history, name='purchase-history'),
    path('search/', views.search, name='search'),
]
