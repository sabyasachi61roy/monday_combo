from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from billing.models import BillingProfile
from .models import Order

# Create your views here.
class OrderList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Order.objects.by_request(self.request)

class OrderDetail(LoginRequiredMixin, DetailView):
    def get_object(self):
        qs = Order.objects.by_request(self.request).filter(order_id = self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        return Http404


    # def get_object(self):
    #     qs = self.get_queryset().filter(order_id = self.kwargs.get('order_id'))
    #     if qs.count() == 1:
    #         return qs.frst()
    #     return Http404

    # def get_queryset(self):
    #     return Order.objects.by_request(self.request)


    # def get_object(self):
    #     return Order.objects.get(id=self.kwargs.get('id'))
    #     return Order.objects.get(slug=self.kwargs.get('slug'))
