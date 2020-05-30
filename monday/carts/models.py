import math
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save, m2m_changed

from products.models import Combo, Addon

User = settings.AUTH_USER_MODEL

# Create your models here.
class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id, ordered=False)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj
    
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class ComboCartItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.combo}"
        # return str(self.id)

    def combo_quantity(self):
        return self.quantity

    def get_total_combo_price(self):
        return self.quantity * self.combo.combo_regular_price
    
    def get_total_combo_sale_price(self):
        return self.quantity * self.combo.combo_sale_price
    
    def get_amount_saved(self):
        return self.get_total_combo_price() - self.get_total_combo_sale_price()

    def get_final_price(self):
        if self.combo.combo_sale_price:
            return self.get_total_combo_sale_price()
        return self.get_total_combo_price

class AddonCartItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    addon = models.ForeignKey(Addon, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    addon_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.addon.name}"
        # return str(self.id)
    
    def addon_quantity(self):
        return self.quantity

    def get_total_addon_price(self):
        addon_total = 0
        addon_total = self.quantity * self.addon.price
        self.addon_total = addon_total
        self.save()
        return self.quantity * self.addon.price

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    combo_item = models.ManyToManyField(ComboCartItem, blank=True, null=True)
    addon_item = models.ManyToManyField(AddonCartItem, blank=True, null=True)
    ordered = models.BooleanField(default=False)

    cart_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def get_total(self):
        c_cart_item = 0
        a_cart_item = 0
        cart_total = 0
        if self.addon_item.all().exists():
            for a in self.combo_item.all():
                c_cart_item += a.get_final_price()
            for b in self.addon_item.all():
                a_cart_item += b.get_total_addon_price()
            cart_total = a_cart_item + c_cart_item
            self.cart_total = cart_total
            self.save()
            return cart_total 
        else:
            for cart_item in self.combo_item.all():
                cart_total += cart_item.get_final_price()
            self.cart_total = cart_total
            self.save()
            return cart_total

    def get_cartItems(self):
        c = 0
        a = 0

        if self.addon_item.all().exists():
            for combo in self.combo_item.all():
                c += combo.combo_quantity()
            for addon in self.addon_item.all():
                a += addon.addon_quantity()
        else:
            for combo in self.combo_item.all():
                c += combo.combo_quantity()
        
        total = c + a
        
        return total
