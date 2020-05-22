from django.urls import path
from .views import cart, add_to_cart


app_name = 'carts'

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('cart/add-to-cart/<slug>', add_to_cart, name='add_to_cart')
]