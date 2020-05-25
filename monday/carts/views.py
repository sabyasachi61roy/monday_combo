from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, ComboCartItem, AddonCartItem
from products.models import Combo, Addon
from deliverypoints.forms import SelectDeliveryPointForm
from billing.models import BillingProfile
from deliverypoints.models import SelectDeliveryPoint, DeliveryPoint
from orders.models import Order
from address.forms import AddressForm
from address.models import Address

# Create your views here.

def cart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        'cart': cart_obj
    }
    return render(request, 'carts/cart-view.html', context)

def combo_add_to_cart(request, slug):
    combo = get_object_or_404(Combo, slug=slug)
    cart_item, created = ComboCartItem.objects.get_or_create(
        combo=combo,
        user=request.user,
        ordered=False
    )
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if cart_obj.combo_item.filter(combo__slug=combo.slug).exists():
        cart_item.quantity += 1
        cart_item.save()
        print("Cart Item Updated")
        return redirect("carts:cart")
    else:
        cart_obj.combo_item.add(cart_item)
        print("Combo Added")
        return redirect("carts:cart")
    return redirect("carts:cart")

def combo_remove_single_to_cart(request, slug):
    combo = get_object_or_404(Combo, slug=slug)
    cart_obj = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if cart_obj.exists():
        cart = cart_obj[0]
        if cart.combo_item.filter(combo__slug=combo.slug).exists():
            item = ComboCartItem.objects.filter(
                combo=combo,
                user=request.user,
                ordered=False
            )[0]
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                print("Combo Decreased")
            else:
                cart.combo_item.remove(item)
                item.delete()
                print("Combo Removed")
            return redirect("carts:cart")
        else:
            print("Redirecting to Home")
            return redirect("/")
    else:
        print("Home")
        return redirect("/")

def combo_remove_from_cart(request, slug):
    combo = get_object_or_404(Combo, slug=slug)
    cart_obj = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if cart_obj.exists():
        cart = cart_obj[0]
        if cart.combo_item.filter(combo__slug=combo.slug).exists():
            item = ComboCartItem.objects.filter(
                combo=combo,
                user=request.user,
                ordered=False
            )[0]
            cart.combo_item.remove(item)
            item.delete()
            print("Combo deleted")
            return redirect("carts:cart")
        else:
            print("Redirecting to Home")
            return redirect("/")
    else:
        print("Home")
        return redirect("/")

def addon_add_to_cart(request, slug):
    addon = get_object_or_404(Addon, slug=slug)
    cart_item, created = AddonCartItem.objects.get_or_create(
        addon=addon,
        user=request.user,
        ordered=False
    )
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if cart_obj.addon_item.filter(addon__slug=addon.slug).exists():
        cart_item.quantity += 1
        cart_item.save()
        print("Cart Item Updated")
        return redirect("carts:cart")
    else:
        cart_obj.addon_item.add(cart_item)
        print("Addon Added")
        return redirect("carts:cart")
    return redirect("carts:cart")

def addon_remove_single_to_cart(request, slug):
    addon = get_object_or_404(Addon, slug=slug)
    cart_obj = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if cart_obj.exists():
        cart = cart_obj[0]
        if cart.addon_item.filter(addon__slug=addon.slug).exists():
            item = AddonCartItem.objects.filter(
                addon=addon,
                user=request.user,
                ordered=False
            )[0]
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                print("Addon Decreased")
            else:
                cart.addon_item.remove(item)
                item.delete()
                print("Addon Removed")
            return redirect("carts:cart")
        else:
            print("Redirecting to Home")
            return redirect("/")
    else:
        print("Home")
        return redirect("/")

    # cart_item, created = AddonCartItem.objects.get_or_create(
    #     addon=addon,
    #     user=request.user,
    #     ordered=False
    # )
    # # cart_obj, new_obj = Cart.objects.new_or_get(request)
    # if cart_obj.addon_item.filter(addon__slug=addon.slug).exists():
    #     cart_item.quantity += 1
    #     cart_item.save()
    #     print("Cart Item Updated")
    #     return redirect("carts:cart")
    # else:
    #     cart_obj.addon_item.add(cart_item)
    #     print("Addon Added")
    #     return redirect("carts:cart")
    # return redirect("carts:cart")

def addon_remove_from_cart(request, slug):
    addon = get_object_or_404(Addon, slug=slug)
    cart_obj = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if cart_obj.exists():
        cart = cart_obj[0]
        if cart.addon_item.filter(addon__slug=addon.slug).exists():
            item = AddonCartItem.objects.filter(
                addon=addon,
                user=request.user,
                ordered=False
            )[0]
            cart.addon_item.remove(item)
            item.delete()
            print("Addon deleted")
            return redirect("carts:cart")
        else:
            print("Redirecting to Home")
            return redirect("/")
    else:
        print("Home")
        return redirect("/")

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
