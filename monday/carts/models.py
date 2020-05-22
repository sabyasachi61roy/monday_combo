from django.db import models
from django.conf import settings

from products.models import Combo

User = settings.AUTH_USER_MODEL

# Create your models here.
# class CartItemManager(models.Manager):
#     def new_or_get(self, request):
#         cart_id = request.session.get("cart_id", None)
#         qs = self.get_queryset().filter(id=cart_id)
#         if qs.count() == 1:
#             new_obj = False
#             cart_obj = qs.first()
#             if request.user.is_authenticated and cart_obj.user is None:
#                 cart_obj.user = request.user
#                 cart_obj.save()
#         else:
#             cart_obj = CartItem.objects.new(user=request.user)
#             new_obj = True
#             request.session['cart_id'] = cart_obj.id
#         return cart_obj, new_obj
    
#     def new(self, user=None):
#         user_obj = None
#         if user is not None:
#             if user.is_authenticated:
#                 user_obj = user
#         return self.model.objects.create(user=user_obj)

# class CartItemManager(models.Manager):
#     def new(self, user=None):
#         user_obj = None
#         if user is not None:
#             if user.is_authenticated:
#                 user_obj = user
#         return self.model.objects.create(user=user_obj)

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
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

class CartItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    # objects = CartItemManager()

    def __str__(self):
        return f"{self.quantity} of {self.combo.title}"
        # return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    item = models.ManyToManyField(CartItem, blank=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)