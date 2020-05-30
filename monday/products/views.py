from django.shortcuts import render
from django.views.generic import ListView

from .models import Prodcut, Combo, Addon
from carts.models import Cart

# Create your views here.
class ComboList(ListView):
    template_name = 'products/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ComboList, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['addons'] = Addon.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        combo = Combo.objects.all()
        return combo
    
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ComboList, self).get_context_data(*args, **kwargs)
    #     cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    #     context['cart'] = cart_obj
    #     return context
    
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     addon = Addon.objects.all()
    #     return addon 

class AllCombo(ListView):
    template_name = 'products/combo_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AllCombo, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        combo = Combo.objects.all()
        return combo

class AllAddon(ListView):
    template_name = 'products/addon_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AllAddon, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        addon = Addon.objects.all()
        return addon