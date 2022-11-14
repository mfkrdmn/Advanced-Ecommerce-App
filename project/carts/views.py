from django.shortcuts import render, redirect, get_object_or_404
from store.models import *
from .models import *
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    current_user = request.user

    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:

                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
    

#   Hata yakalama, yazdığımız beklenmedik durumlarda karşılaşacağımız hatalarda programın hata vermesi ya da kendini durdurması yerine 
# hataya kendi istediğimiz şekilde cevap vermesini sağlama durumudur. Hata yakalama program yazmanın önemli bir parçasıdır.
# Python’da hata yakalamayı try – except blokları ile yapıyoruz. 
# try: 
#   programın ana kodları
# except:
#   hata olduğunda işletilecek kodlar
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) 
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.create(product=product, quantity = 1, cart=cart)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for cartitem in product_variation:
                cart_item.variations.add(cartitem)
        # cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist: # Django provides a DoesNotExist exception as an attribute of each model class to identify the class 
        #of object that could not be found, allowing you to catch exceptions for a particular model class. 
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for cartitem in product_variation:
                cart_item.variations.add(cartitem)
        cart_item.save()
    return redirect('cart')


#############


def decrement_cart(request, product_id):
    
    cart = Cart.objects.get(cart_id=_cart_id(request)) 
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else :
        cart_item.delete()
    return redirect('cart')


#############


def remove_cart_item(request, product_id):
    
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


#############


def cart(request, total=0, quantity=0, cart_items=None):

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for i in cart_items:
            total += (i.product.price * i.quantity)
            quantity += i.quantity
        tax = (3*total)/100
        grand_total = total+tax
            
    except ObjectDoesNotExist:
        pass

    context ={
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total
    }


    return render(request, 'cart.html', context)