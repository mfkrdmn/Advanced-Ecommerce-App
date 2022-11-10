from django.shortcuts import render
from .models import *
# Create your views here.

def store(request):

    products = Product.objects.all().filter(is_available=True)

    context = {
        "products" : products
    }

    return render(request, 'store.html', context)