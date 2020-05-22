from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from products.models import Combo

# Create your views here.

def cart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        'cart': cart_obj
    }
    return render(request, 'carts/cart-view.html', context)

def add_to_cart(request, slug):
    combo = get_object_or_404(Combo, slug=slug)
    cart_item, created = CartItem.objects.get_or_create(
        combo=combo,
        user=request.user,
    )
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if cart_obj.item.filter(combo__slug=combo.slug).exists():
            cart_item.quantity += 1
            cart_item.save()
            print("Cart Item Updated")
            return redirect("carts:cart")
    else:
        cart_obj.item.add(cart_item)
        print("Combo Added")
        return redirect("carts:cart")
    return redirect("carts:cart")
    # if cart_obj.exists():
    #     cart = cart_obj[0]
    #     if cart.filter(combo__slug=combo.slug).exists():
    #         cart_item.quantity += 1
    #         cart_item.save()
    #         print("Cart Item Updated")
    #         return redirect("carts:cart")
    #     else:
    #         cart.item.add(cart_item)
    #         print("Combo Added")
    #         return redirect("carts:cart")

    # cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
    #         product_added = True