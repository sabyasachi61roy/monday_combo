# Generated by Django 3.0.7 on 2020-06-06 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='activeasdasda',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
    ]
