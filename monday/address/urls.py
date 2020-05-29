from django.urls import path

from .views import checkout_address, checkout_address_reuse

app_name = 'address'

urlpatterns = [
    path('checkout-address/create/', checkout_address, name='checkout_address_create'),
    path('checkout-address/reuse/', checkout_address_reuse, name='checkout_address_reuse'),
]