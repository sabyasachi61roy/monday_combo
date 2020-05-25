import math
from django.db import models
from django.db.models.signals import pre_save, post_save
from billing.models import BillingProfile
from deliverypoints.models import SelectDeliveryPoint, DeliveryPoint
from carts.models import Cart
from main.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
    ('Created', 'Created'),
    ('Paid', 'Paid'),
    ('Shipped', 'Shipped'),
    ('Refunded', 'Refunded'),
)

# Create your models here.
class OrderManager(models.Manager):
    def new_or_get(self, cart_obj, billing_profile):
        created = False
        qs = self.get_queryset().filter(cart=cart_obj, billing_profile=billing_profile, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(cart=cart_obj, billing_profile=billing_profile)
            created = True
        return obj, created

class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, blank=True, null=True, on_delete=models.CASCADE)
    delivery_point = models.ForeignKey(DeliveryPoint, blank=True, null=True, on_delete=models.CASCADE)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2) 
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    active = models.BooleanField(default=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        c_total = self.cart.cart_total
        shipping_total = self.shipping_total
        new_total = math.fsum([c_total, shipping_total])
        formatted_total = format(new_total,'.2f')
        self.total = formatted_total
        self.save()
        return new_total

def pre_save_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_order_id, sender=Order)

def post_save_cart_total(sender, created, instance, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.cart_total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)