from django.contrib import admin
from .models import *

class MarketingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'subscribed', 'updated']
    readonly_fields = ['mailchimp_subscribed', 'mailchimp_msg','timestamp', 'updated']
    class Meta:
        model = Marketing
        fields = ['user', 'subscribed', 'mailchimp_subscribed', 'mailchimp_msg', 'timestamp', 'updated']

# Register your models here.
admin.site.register(Marketing, MarketingAdmin)