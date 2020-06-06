from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from .utils import Mailchimp

User = settings.AUTH_USER_MODEL

# Create your models here.
class Marketing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)
    mailchimp_subscribed = models.NullBooleanField(blank=True)
    mailchimp_msg = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

def marketing_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print("Add user to mailchimp")
        status_code, reponse_data = Mailchimp().subscribe(instance.user.email)

post_save.connect(marketing_create_receiver, sender=Marketing)

def marketing_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            print("Update user to mailchimp")
            status_code, reponse_data = Mailchimp().subscribe(instance.user.email)
        else:
            status_code, reponse_data = Mailchimp().unsubscribe(instance.user.email)
        
        if reponse_data['status'] == 'subscribed':      # status != 200
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = reponse_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = reponse_data

pre_save.connect(marketing_update_receiver, sender=Marketing)

def marketing_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Marketing.objects.get_or_create(user=instance)

post_save.connect(marketing_receiver, sender=User)