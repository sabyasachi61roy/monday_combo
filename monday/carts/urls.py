from django.urls import path
from .views import *


app_name = 'carts'

urlpatterns = [
    path('cart/', cart, name='cart'),
    # path('api/cart/', cart_api, name='cart-api'),
    path('cart/checkout/', checkout, name='checkout'),
    path('orders/', success, name='success'),
    path('cart/combo/add-to-cart/', combo_add_to_cart, name='combo_add_to_cart'),
    path('cart/addon/add-to-cart/', addon_add_to_cart, name='addon_add_to_cart'),
    path('cart/combo/quantity/deacrease-from-cart/', combo_remove_single_to_cart, name='combo_remove_single_to_cart'),
    path('cart/addon/quantity/deacrease-from-cart/', addon_remove_single_to_cart, name='addon_remove_single_to_cart'),
    path('cart/combo/remove-from-cart/', combo_remove_from_cart, name='combo_remove_from_cart'),
    path('cart/addon/remove-from-cart/', addon_remove_from_cart, name='addon_remove_from_cart'),
]