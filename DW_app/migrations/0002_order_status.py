# Generated by Django 5.1.4 on 2025-01-06 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DW_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'NEW'), ('inprogress', 'IN PROGRESS'), ('completed', 'COMPLETED'), ('delivered', 'DELIVERED')], default='NEW', max_length=50),
        ),
    ]
