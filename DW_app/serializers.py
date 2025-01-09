from rest_framework import serializers
from .models import Customer, Clothes, Order
from django.contrib.auth.hashers import make_password
from django.conf import settings

class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ["id","photo","type","price"]

class OrderSerializer(serializers.ModelSerializer):
    clothes = ClothesSerializer(many=True , read_only = True)

    class Meta:
        model = Order
        fields = ["customer_id","item","status","clothes"]


class CustomerSerializer(serializers.ModelSerializer):
    customer_order = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["mobile_num", "password"]

       

    def validate(self, attrs):
        mobile_num = attrs.get("mobile_num")
        password = attrs.get("password")
        secret_key = settings.SECRET_KEY
        

        try:
            customer = Customer.objects.get(mobile_num=mobile_num)

        except Customer.DoesNotExist:
            attrs["message"] = "Invalid credentials"
            return attrs
        
        hashed_password = make_password(password+secret_key+customer.pincode)

        if customer.password == hashed_password:
            customer_data = CustomerSerializer(customer).data
            attrs["customer"] = customer_data
            return attrs
        else:
            attrs["message"] = "Invalid credentials"
            return attrs
