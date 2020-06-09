import math
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from billing.models import BillingProfile
from deliverypoints.models import SelectDeliveryPoint, DeliveryPoint
from carts.models import Cart
from main.utils import unique_order_id_generator
from django.conf import settings
from address.models import Address

User = settings.AUTH_USER_MODEL

ORDER_STATUS_CHOICES = (
    ('Created', 'Created'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    ('Refunded', 'Refunded'),
)

ORDER_PAYMENT_METHOD = (
    ('COD', "COD"),
    ("PREPAID", "PREPAID"),
)

class OderManagerQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='Created')

# Create your models here.
class OrderManager(models.Manager):
    def get_queryset(self):
        return OderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

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
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    billing_profile = models.ForeignKey(BillingProfile, blank=True, null=True, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True, on_delete=models.CASCADE)
    delivery_point = models.ForeignKey(DeliveryPoint, blank=True, null=True, on_delete=models.CASCADE)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2) 
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    payment_method = models.CharField(max_length=120, choices=ORDER_PAYMENT_METHOD)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    active = models.BooleanField(default=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp', '-updated']

    def get_absolute_url(self):
        return reverse("orders:order-detail", kwargs={"order_id": self.order_id})

    def get_status(self):
        if self.status == 'Created':
            return "Processing"
        elif self.status == 'Processing':
            return "Sipping soon"
        elif self.status == 'Shipped':
            return 'On it way'
        elif self.status == 'Cancelled':
            return "Cancelled"
        elif self.status == 'Refunded':
            return "Refunded"
        else:
            return 'Completed'

    def update_total(self):
        c_total = self.cart.cart_total
        shipping_total = self.shipping_total
        new_total = math.fsum([c_total, shipping_total])
        formatted_total = format(new_total,'.2f')
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile=self.billing_profile
        delivery_point = self.delivery_point
        total = self.total
        if self.total < 0:
            return False
        elif delivery_point and total > 0:
            return True
        return False
    
    def check_d(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if self.total < 0:
            return False
        elif billing_address and shipping_address and billing_address and total > 0:
            return True
        return False

    def mark_cod(self):
        if self.check_done() or self.check_d():
            self.payment_method = "COD"
            self.save()
        return self.status

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