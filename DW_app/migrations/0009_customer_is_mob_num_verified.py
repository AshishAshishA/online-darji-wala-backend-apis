# Generated by Django 5.1.4 on 2025-01-09 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DW_app', '0008_remove_clothes_order_clothes_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_mob_num_verified',
            field=models.BooleanField(default=False),
        ),
    ]
