from django.contrib import admin
from .models import ComboCartItem, AddonCartItem, Cart
# Register your models here.
admin.site.register(ComboCartItem)
admin.site.register(AddonCartItem)
admin.site.register(Cart)