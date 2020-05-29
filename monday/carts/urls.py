from django.urls import path
from .views import cart, checkout, success, combo_add_to_cart, addon_add_to_cart, addon_remove_single_to_cart, combo_remove_single_to_cart, combo_remove_from_cart, addon_remove_from_cart


app_name = 'carts'

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('cart/checkout/', checkout, name='checkout'),
    path('orders/', success, name='success'),
    path('cart/combo/add-to-cart/<slug>', combo_add_to_cart, name='combo_add_to_cart'),
    path('cart/addon/add-to-cart/<slug>', addon_add_to_cart, name='addon_add_to_cart'),
    path('cart/combo/quantity/deacrease-from-cart/<slug>', combo_remove_single_to_cart, name='combo_remove_single_to_cart'),
    path('cart/addon/quantity/deacrease-from-cart/<slug>', addon_remove_single_to_cart, name='addon_remove_single_to_cart'),
    path('cart/combo/remove-from-cart/<slug>', combo_remove_from_cart, name='combo_remove_from_cart'),
    path('cart/addon/remove-from-cart/<slug>', addon_remove_from_cart, name='addon_remove_from_cart'),
]