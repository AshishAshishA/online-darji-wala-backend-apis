from django.db import models
from django.contrib.auth.hashers import make_password
from django.conf import settings
# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=250)
    mobile_num = models.CharField(max_length=15 , unique=True, null=False, blank=False)
    is_mob_num_verified = models.BooleanField(default=False)
    address = models.TextField()
    pincode = models.CharField(max_length=10, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=128 ,blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('$'):
            secret_key = settings.SECRET_KEY
            self.password = make_password(self.password + secret_key + self.pincode)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    Item_Choices = [
        ('shirt', 'SHIRT'),
        ('pant', 'PANT'),
    ]
    Status_Choices = [
        ('new','NEW'),
        ('inprogress','IN PROGRESS'),
        ('completed','COMPLETED'),
        ('delivered','DELIVERED'),
    ]
    item = models.CharField(choices=Item_Choices, max_length=5)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='customer_order')
    status = models.CharField(choices=Status_Choices,default="NEW",max_length=50)

    def __str__(self):
        return f'{self.item} ordered by {self.customer.name}'

class Clothes(models.Model):
    photo = models.CharField(max_length=255)
    type = models.CharField(max_length=200)
    price = models.FloatField(default=100)
    order = models.ManyToManyField(Order, related_name='cloth_order')

    def __str__(self):
        return f'{self.type}'
