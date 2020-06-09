from django.urls import path, re_path
from .views import OrderDetail, OrderList


app_name = 'orders'

urlpatterns = [
    path('order/list/', OrderList.as_view(), name='order-list'),
    re_path(r'^order/detail/(?P<order_id>[0-9A-Za-z]+)/$', OrderDetail.as_view(), name="order-detail") 
]