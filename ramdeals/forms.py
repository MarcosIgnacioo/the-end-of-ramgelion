from django.forms import ModelForm
from .models import Producto
from .models import OrderedProducts


class ProductForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['product_name', 'category', 'description',
                  'price', 'stock', 'discount', 'stars', 'image_url']


class OrderProductForm(ModelForm):
    class Meta:
        model = OrderedProducts
        fields = ['product', 'quantity']
