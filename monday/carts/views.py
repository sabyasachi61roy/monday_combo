from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Cart, ComboCartItem, AddonCartItem

from products.models import Combo, Addon

from deliverypoints.forms import SelectDeliveryPointForm
from deliverypoints.models import SelectDeliveryPoint, DeliveryPoint

from billing.models import BillingProfile

from orders.models import Order

from address.forms import AddressForm
from address.models import Address

# Create your views here.

def cart_api(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    
    combos = [
        {
        "id": x.combo.id,
        # "url": x.combo.get_absolute_url(),
        "title": x.combo.title, 
        "price": x.combo.combo_regular_price, 
        "sale": x.combo.combo_sale_price, 
        "quantity": x.quantity, 
        "combo_total": x.get_total_combo_sale_price(), 
        "saved": x.get_amount_saved()
        }
        for x in cart_obj.combo_item.all()
    ]
    
    addons = [
        {
        "id": y.combo.id,
        # "url": y.combo.get_absolute_url(),
        "name": y.addon.name,
        "price": y.addon.price,
        "quantity": y.quantity,
        "addon_total": y.get_total_addon_price()
        }
        for y in cart_obj.addon_item.all()
    ]
    
    cart_data = {"combo":combos, "addon": addons, "total": cart_obj.get_total()}
    
    return JsonResponse(cart_data)


def cart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        'cart': cart_obj
    }
    return render(request, 'carts/cart-view.html', context)

def combo_add_to_cart(request):
    combo_id = request.POST.get('combo_id')

    if combo_id is not None:
        try:
            combo_obj = Combo.objects.get(id=combo_id)
        except Combo.DoesNotExist:
            return("carts:cart")
    
        combo = combo_obj
    
        cart_item, created = ComboCartItem.objects.get_or_create(
            combo=combo,
            user=request.user,
            ordered=False
        )
    
        cart_obj, new_obj = Cart.objects.new_or_get(request)
    
        if cart_obj.combo_item.filter(combo__id=combo.id).exists():
            cart_item.quantity += 1
            cart_item.save()
            print("Cart Item Updated")
            added = False
            updated = True
            # return redirect("carts:cart")
        else:
            cart_obj.combo_item.add(cart_item)
            print("Combo Added")
            added = True
            updated = False
            # return redirect("carts:cart")

        # print(combo_id)
        cartCount = cart_obj.get_cartItems()
        print(cartCount)
        if request.is_ajax():
            print("Ajax Request")
            json_data = {
            "added": added,
            # "not_added": not added,
            "updated": updated,
            # "not_updated": not updated
            "ItemCount": cartCount
            }   
            return JsonResponse(json_data)

    return redirect("carts:cart")

def combo_remove_from_cart(request):
    combo_id = request.POST.get('combo_id')
    
    if combo_id is not None:
        try:
            combo_obj = Combo.objects.get(id=combo_id)
        except Combo.DoesNotExist:
            return("carts:cart")
    
        combo = combo_obj
        cart_obj = Cart.objects.filter(
            user=request.user,
            ordered=False
        )
        if cart_obj.exists():
            cart = cart_obj[0]
            if cart.combo_item.filter(combo__id=combo.id).exists():
                item = ComboCartItem.objects.filter(
                    combo=combo,
                    user=request.user,
                    ordered=False
                )[0]
                cart.combo_item.remove(item)
                item.delete()
                print("Combo deleted")
                # return redirect("carts:cart")
                updated = True
                added = False

                cartCount = cart.get_cartItems()
                print(cartCount)
                
                if request.is_ajax():
                    print("Ajax Request")
                    json_data = {
                    "added": added,
                    # "not_added": not added,
                    "updated": updated,
                    # "not_updated": not updated
                    "ItemCount": cartCount,
                    }   
                    return JsonResponse(json_data)
            else:
                print("Redirecting to Home")
                return redirect("/")
        else:
            print("Home")
            return redirect("/")

def combo_remove_single_to_cart(request):
    combo_id = request.POST.get('combo_id')
    
    if combo_id is not None:
        try:
            combo_obj = Combo.objects.get(id=combo_id)
        except Combo.DoesNotExist:
            return("carts:cart")
    
        combo = combo_obj

        cart_obj = Cart.objects.filter(
            user=request.user,
            ordered=False
        )
        if cart_obj.exists():
            cart = cart_obj[0]
            if cart.combo_item.filter(combo__id=combo.id).exists():
                item = ComboCartItem.objects.filter(
                    combo=combo,
                    user=request.user,
                    ordered=False
                )[0]
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                    print("Combo Decreased")
                    added=False
                    updated=True
                else:
                    cart.combo_item.remove(item)
                    item.delete()
                    print("Combo Removed")
                    added=False
                    updated=True
                # return redirect("carts:cart")
                cartCount = cart.get_cartItems()
                print(cartCount)
                if request.is_ajax():
                    print("Ajax Request")
                    json_data = {
                    "added": added,
                    # "not_added": not added,
                    "updated": updated,
                    # "not_updated": not updated
                    "ItemCount": cartCount,
                    }   
                    return JsonResponse(json_data)
            else:
                print("Redirecting to Home")
                return redirect("/")
        else:
            print("Home")
            return redirect("/")

def addon_add_to_cart(request):
    addon_id = request.POST.get('addon_id')

    if addon_id is not None:
        try:
            addon_obj = Addon.objects.get(id=addon_id)
        except Addon.DoesNotExist:
            return("carts:cart")
    
        addon = addon_obj
        cart_item, created = AddonCartItem.objects.get_or_create(
            addon=addon,
            user=request.user,
            ordered=False
        )
        
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        
        if cart_obj.addon_item.filter(addon__id=addon.id).exists():
            cart_item.quantity += 1
            cart_item.save()
            print("Cart Item Updated")
            added = False
            updated = True
            # return redirect("carts:cart")
        else:
            cart_obj.addon_item.add(cart_item)
            print("Addon Added")
            added = True
            updated = False
            # return redirect("carts:cart")

        cartCount = cart_obj.get_cartItems()
        print(cartCount)
        if request.is_ajax():
            print("Ajax Request")
            json_data = {
            "added": added,
            # "not_added": not added,
            "updated": updated,
            # "not_updated": not updated
            "ItemCount": cartCount,
            }   
            return JsonResponse(json_data)
    return redirect("carts:cart")

def addon_remove_from_cart(request):
    addon_id = request.POST.get('addon_id')
    
    if addon_id is not None:
        try:
            addon_obj = Addon.objects.get(id=addon_id)
        except Addon.DoesNotExist:
            return("carts:cart")
    
        addon = addon_obj
        cart_obj = Cart.objects.filter(
            user=request.user,
            ordered=False
        )
        if cart_obj.exists():
            cart = cart_obj[0]
            if cart.addon_item.filter(addon__id=addon.id).exists():
                item = AddonCartItem.objects.filter(
                    addon=addon,
                    user=request.user,
                    ordered=False
                )[0]
                cart.addon_item.remove(item)
                item.delete()
                print("Addon deleted")
                # return redirect("carts:cart")
                updated = True
                added = False

                cartCount = cart.get_cartItems()
                print(cartCount)
                
                if request.is_ajax():
                    print("Ajax Request")
                    json_data = {
                    "added": added,
                    # "not_added": not added,
                    "updated": updated,
                    # "not_updated": not updated
                    "ItemCount": cartCount,
                    }   
                    return JsonResponse(json_data)
            else:
                print("Redirecting to Home")
                return redirect("/")
        else:
            print("Home")
            return redirect("/")

def addon_remove_single_to_cart(request):
    addon_id = request.POST.get('addon_id')
    
    if addon_id is not None:
        try:
            addon_obj = Addon.objects.get(id=addon_id)
        except Addon.DoesNotExist:
            return("carts:cart")
    
        addon = addon_obj
        
        cart_obj = Cart.objects.filter(
            user=request.user,
            ordered=False
        )
        if cart_obj.exists():
            cart = cart_obj[0]
            if cart.addon_item.filter(addon__id=addon.id).exists():
                item = AddonCartItem.objects.filter(
                    addon=addon,
                    user=request.user,
                    ordered=False
                )[0]
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                    # print("Addon Decreased")
                    updated = True
                    added = False
                else:
                    cart.addon_item.remove(item)
                    item.delete()
                    print("Addon Removed")
                    updated = True
                    added = False
                # return redirect("carts:cart")

                cartCount = cart.get_cartItems()
                print(cartCount)
                if request.is_ajax():
                    print("Ajax Request")
                    json_data = {
                    "added": added,
                    # "not_added": not added,
                    "updated": updated,
                    # "not_updated": not updated
                    "ItemCount": cartCount,
                    }   
                    return JsonResponse(json_data)
            else:
                print("Redirecting to Home")
                return redirect("/")
        else:
            print("Home")
            return redirect("/")

# def combo_add_to_cart(request, slug):
#     combo = get_object_or_404(Combo, slug=slug)
#     cart_item, created = ComboCartItem.objects.get_or_create(
#         combo=combo,
#         user=request.user,
#         ordered=False
#     )
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     if cart_obj.combo_item.filter(combo__slug=combo.slug).exists():
#         cart_item.quantity += 1
#         cart_item.save()
#         print("Cart Item Updated")
#         return redirect("carts:cart")
#     else:
#         cart_obj.combo_item.add(cart_item)
#         print("Combo Added")
#         return redirect("carts:cart")
#     return redirect("carts:cart")

# def combo_remove_single_to_cart(request, slug):
#     combo = get_object_or_404(Combo, slug=slug)
#     cart_obj = Cart.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if cart_obj.exists():
#         cart = cart_obj[0]
#         if cart.combo_item.filter(combo__slug=combo.slug).exists():
#             item = ComboCartItem.objects.filter(
#                 combo=combo,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             if item.quantity > 1:
#                 item.quantity -= 1
#                 item.save()
#                 print("Combo Decreased")
#             else:
#                 cart.combo_item.remove(item)
#                 item.delete()
#                 print("Combo Removed")
#             return redirect("carts:cart")
#         else:
#             print("Redirecting to Home")
#             return redirect("/")
#     else:
#         print("Home")
#         return redirect("/")

# def combo_remove_from_cart(request, slug):
#     combo = get_object_or_404(Combo, slug=slug)
#     cart_obj = Cart.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if cart_obj.exists():
#         cart = cart_obj[0]
#         if cart.combo_item.filter(combo__slug=combo.slug).exists():
#             item = ComboCartItem.objects.filter(
#                 combo=combo,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             cart.combo_item.remove(item)
#             item.delete()
#             print("Combo deleted")
#             return redirect("carts:cart")
#         else:
#             print("Redirecting to Home")
#             return redirect("/")
#     else:
#         print("Home")
#         return redirect("/")

# def addon_add_to_cart(request, slug):
#     addon = get_object_or_404(Addon, slug=slug)
#     cart_item, created = AddonCartItem.objects.get_or_create(
#         addon=addon,
#         user=request.user,
#         ordered=False
#     )
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     if cart_obj.addon_item.filter(addon__slug=addon.slug).exists():
#         cart_item.quantity += 1
#         cart_item.save()
#         print("Cart Item Updated")
#         return redirect("carts:cart")
#     else:
#         cart_obj.addon_item.add(cart_item)
#         print("Addon Added")
#         return redirect("carts:cart")
#     return redirect("carts:cart")

# def addon_remove_single_to_cart(request, slug):
#     addon = get_object_or_404(Addon, slug=slug)
#     cart_obj = Cart.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if cart_obj.exists():
#         cart = cart_obj[0]
#         if cart.addon_item.filter(addon__slug=addon.slug).exists():
#             item = AddonCartItem.objects.filter(
#                 addon=addon,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             if item.quantity > 1:
#                 item.quantity -= 1
#                 item.save()
#                 print("Addon Decreased")
#             else:
#                 cart.addon_item.remove(item)
#                 item.delete()
#                 print("Addon Removed")
#             return redirect("carts:cart")
#         else:
#             print("Redirecting to Home")
#             return redirect("/")
#     else:
#         print("Home")
#         return redirect("/")

#     # cart_item, created = AddonCartItem.objects.get_or_create(
#     #     addon=addon,
#     #     user=request.user,
#     #     ordered=False
#     # )
#     # # cart_obj, new_obj = Cart.objects.new_or_get(request)
#     # if cart_obj.addon_item.filter(addon__slug=addon.slug).exists():
#     #     cart_item.quantity += 1
#     #     cart_item.save()
#     #     print("Cart Item Updated")
#     #     return redirect("carts:cart")
#     # else:
#     #     cart_obj.addon_item.add(cart_item)
#     #     print("Addon Added")
#     #     return redirect("carts:cart")
#     # return redirect("carts:cart")

# def addon_remove_from_cart(request, slug):
#     addon = get_object_or_404(Addon, slug=slug)
#     cart_obj = Cart.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if cart_obj.exists():
#         cart = cart_obj[0]
#         if cart.addon_item.filter(addon__slug=addon.slug).exists():
#             item = AddonCartItem.objects.filter(
#                 addon=addon,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             cart.addon_item.remove(item)
#             item.delete()
#             print("Addon deleted")
#             return redirect("carts:cart")
#         else:
#             print("Redirecting to Home")
#             return redirect("/")
#     else:
#         print("Home")
#         return redirect("/")

def checkout(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.combo_item.count() == 0:
        return redirect('carts:cart')
    address_form = AddressForm()
    dpointform = SelectDeliveryPointForm()
    delivery_point = request.session.get("delivery_point_id", None)
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    print(billing_profile)
    dpoint_qs = None
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            dpoint_qs = DeliveryPoint.objects.all()
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(cart_obj, billing_profile)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if delivery_point:
            order_obj.user = request.user
            order_obj.delivery_point = DeliveryPoint.objects.get(id=delivery_point)
            # del request.session['delivery_point_id']
            order_obj.save()
        elif billing_address_id or shipping_address_id:
            order_obj.user = request.user
            order_obj.save()
    if order_obj.delivery_point is not None:
        if request.method == "POST":
            is_done = order_obj.check_done()
            if is_done:
                order_obj.mark_cod()
                cart_obj.ordered=True
                c = cart_obj.combo_item.all()
                c.update(ordered=True)
                a = cart_obj.addon_item.all()
                a.update(ordered=True)
                for ci in c:
                    ci.save()
                for ai in a:
                    ai.save()
                cart_obj.save()
                del request.session['cart_id']
                return redirect("carts:success")
        del request.session['delivery_point_id']
    else:
        if request.method == "POST":
            is_done = order_obj.check_d()
            if is_done:
                order_obj.mark_cod()
                cart_obj.ordered=True
                c = cart_obj.combo_item.all()
                c.update(ordered=True)
                a = cart_obj.addon_item.all()
                a.update(ordered=True)
                for ci in c:
                    ci.save()
                for ai in a:
                    ai.save()
                cart_obj.save()
                del request.session['cart_id']
                return redirect("carts:success")
    # if request.method == "POST":
    #     is_done = order_obj.check_done()
    #     if is_done:
    #         order_obj.mark_cod()
    #         cart_obj.ordered=True
    #         c = cart_obj.combo_item.all()
    #         c.update(ordered=True)
    #         a = cart_obj.addon_item.all()
    #         a.update(ordered=True)
    #         for ci in c:
    #             ci.save()
    #         for ai in a:
    #             ai.save()
    #         cart_obj.save()
    #         del request.session['cart_id']
    #         return redirect("carts:success")

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'dpointform': dpointform,
        'dpointqs': dpoint_qs,
        'address_form':address_form,
        'address_qs': address_qs,
    }
    return render(request, 'carts/checkout.html', context)

def success(request):
    if request.user.is_authenticated:
        obj = request.user.order_set.last()
        context = {
            'obj': obj
        }
    return render(request, "carts/success.html", context)
