# Generated by Django 3.0.7 on 2020-06-07 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
    ]