from django.shortcuts import render, redirect
from .models import DeliveryPoint, SelectDeliveryPoint
from .forms import SelectDeliveryPointForm
from billing.models import BillingProfile
from django.utils.http import is_safe_url

# Create your views here.
# def delivery_points(request):
#     form = SelectDeliveryPointForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         instance = form.save(commit=False)
#         billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
#         if billing_profile is not None:
#             d_point = request.POST.get('delivery_point', 'delivery_pont_id')
#             print(d_point)
#             instance.user= request.user
#             instance.billing_profile = billing_profile
#             instance.delivery_point = DeliveryPoint.objects.get(id=d_point)
#             instance.save()
#             request.session["delivery_point_id"] = instance.id
#             print(d_point, 'shop1')
#         else:
#             return redirect("carts:checkout")
#         if is_safe_url(redirect_path, request.get_host()):
#             return redirect(redirect_path)
#         else:
#             return redirect("carts:checkout")
#     return redirect("carts:checkout")

def delivery_points(request):
    if request.user.is_authenticated:
        context = {}
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == 'POST':
            print(request.POST, "POST")
            print("I am here")
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            delivery_point = request.POST.get('delivery_point', None)
            print(delivery_point, "POINT")
            if delivery_point is not None:
                user = request.user
                instance = SelectDeliveryPoint.objects.get_or_create(user=user, billing_profile=billing_profile, delivery_point=DeliveryPoint.objects.get(id=delivery_point))
                # instance.billing_profile = billing_profile
                # instance.delivery_point = DeliveryPoint.objects.get(id=delivery_point)
                # instance.save()
                request.session["delivery_point_id"] = delivery_point
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("carts:checkout")
