# Generated by Django 3.0.7 on 2020-06-08 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopn_name', models.CharField(blank=True, max_length=120, null=True)),
                ('address_line1', models.CharField(max_length=120)),
                ('address_line2', models.CharField(blank=True, max_length=120, null=True)),
                ('country', models.CharField(default='India', max_length=120)),
                ('state', models.CharField(max_length=120)),
                ('city', models.CharField(max_length=120)),
                ('postal_code', models.CharField(max_length=120)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SelectDeliveryPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile')),
                ('delivery_point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deliverypoints.DeliveryPoint')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
