# Generated by Django 3.0.6 on 2020-05-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_auto_20200529_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addoncartitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='combocartitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
