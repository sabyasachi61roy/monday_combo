from datetime import timedelta
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import pre_save, post_save

from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone

from main.utils import random_string_generator, unique_key_generator
from random import randint

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 2)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError("Users must have a password")
        # if not full_name:
        #     raise ValueError("Users must have fullname")
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email, full_name=full_name, password=password, is_staff=True
        )
        return user
    
    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email, full_name=full_name, password=password, is_staff=True, is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [] #['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.is_active

class EmailActivationQuerySet(models.query.QuerySet):       #EmailActivation.objects.all().confirmable()
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated = False,
            forced_expired = False
        ).filter(
            timestamp__get=start_range,
            timestamp__lte=end_range
        )

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)
    
    def confirmable(self):
        return self.get_queryset().confirmable()

class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False
    
    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, "BASE_URL", None)
                key_path = self.key 
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    "emai": self.email
                }
                txt_ = get_template("registration/emais/verify.txt").render(context)
                html_ = get_template("registration/emais/verify.html").render(context)
                subject = "One Click Email Veriication"
                from_email = ""
                recipient_list = [self.email]
                send_mail = send_mail(
                    subject,
                    txt_,
                    from_email.
                    recipient_list,
                    html_mesage=html_,
                    fail_silently=False,
                )
                return send_mail
        return False

def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            # size = randint(30,45)
            # key = random_string_generator(size=size)
            # qs = EmailActivation.objects.filter(key__iexact=key)
            # if qs.exists():
            #     key = random_string_generator(size=size)
            # instance.key = key
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation, sender=EmailActivation)

def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_receiver, sender=User)        