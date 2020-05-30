import os
import random
from django.db.models import Q
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save, pre_save, m2m_changed
# Create your models here.
class AddonQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class AddonManager(models.Manager):
    def get_queryset(self):
        return AddonQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

class Addon(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    objects = AddonManager()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse('products:addon-detail', kwargs={'slug':self.slug})

class Prodcut(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    regular_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name


class ComboQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class ComboManager(models.Manager):
    def get_queryset(self):
        return ComboQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

class Combo(models.Model):
    products = models.ManyToManyField(Prodcut)
    title = models.CharField(max_length=120)
    combo_regular_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    combo_sale_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)

    objects = ComboManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse('products:combo-detail', kwargs={'slug':self.slug})

def m2m_price_changed_receiver(sender, action, instance, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        combo_regular_price = 0
        combo_sale_price = 0
        for x in products:
            combo_regular_price += x.regular_price
            combo_sale_price += x.sale_price
        instance.combo_regular_price = combo_regular_price
        instance.combo_sale_price = combo_sale_price
        instance.save()
        # combo_regular_price.save()
        # combo_sale_price.save()

m2m_changed.connect(m2m_price_changed_receiver, sender=Combo.products.through)