from django.urls import path

from .views import delivery_points

app_name = 'deliverypoints'

urlpatterns = [
    path('checkout-delivery/point/select/', delivery_points, name='delivery_points_select'),
]