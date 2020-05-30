# Generated by Django 3.0.6 on 2020-05-24 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
        ('deliverypoints', '0003_deliverypoint_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectdeliverypoint',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile'),
        ),
    ]