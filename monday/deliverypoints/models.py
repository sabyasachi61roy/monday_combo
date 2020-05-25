from django.db import models
from django.conf import settings
from billing.models import BillingProfile

User = settings.AUTH_USER_MODEL

# Create your models here.
class DeliveryPointQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class DeliveryPointManager(models.Manager):
    def get_queryset(self):
        return DeliveryPointQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs =  self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()

class DeliveryPoint(models.Model):
    shopn_name = models.CharField(max_length=120, blank=True, null=True)
    address_line1 = models.CharField(max_length=120)
    address_line2 = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=120, default="India")
    state = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)
    active = models.BooleanField(default=True)

    objects = DeliveryPointManager()

    def __str__(self):
        return self.shopn_name

# class SelectDeliveryPointManager(models.Manager):
#     # creating a new cart or getting the current one
#     def new_or_get(self, request):
#         select_delivery_point_id = request.session.get("select_delivery_point_id", None)
#         qs = self.get_queryset().filter(id=select_delivery_point_id)
#         if qs.count() == 1:
#             select_delivery_point_obj = qs.first()
#             if request.user.is_authenticated and select_delivery_point_obj.user is None:
#                 select_delivery_point_obj.user = request.user
#                 select_delivery_point_obj.save()
#         else:
#             select_delivery_point_obj = SelectDeliveryPoint.objects.new(user=request.user)
#             new_obj = True
#             request.session['select_delivery_point_id'] = select_delivery_point_obj.id
#         return select_delivery_point_obj, new_obj

#     def new(self, user=None):
#         user_obj = None
#         if user is not None:
#             if user.is_authenticated:
#                 user_obj = user
#         return self.model.objects.create(user=user_obj)
    
class SelectDeliveryPoint(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    delivery_point = models.ForeignKey(DeliveryPoint, blank=True, null=True, on_delete=models.CASCADE)

    # objects = SelectDeliveryPointManager()

    def __str__(self):
        return str(self.delivery_point)