from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

from .helpers import send_otp_to_phone

from .models import Clothes, Customer, Order
from .serializers import ClothesSerializer, CustomerSerializer, OrderSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Access the raw request data without going through serializer validation
        raw_data = request.data
        # print("Raw Request Data:", raw_data)

        # Manually process the raw data
        item = raw_data.get('item')
        status = raw_data.get('status', 'new')
        customer_data = raw_data.get('customer_id')
        clothes_data = raw_data.get('clothes')

        # Create the customer object
        customer_obj = Customer.objects.get(id=customer_data)  # Assuming customer ID is valid

        # Create the order manually (bypassing validation)
        orderObj = Order.objects.create(item=item, status=status, customer=customer_obj)

        # Create and associate clothes items with the order
        for cloth_data in clothes_data:
            cloth_obj = Clothes.objects.get(id=cloth_data['id'])
            cloth_obj.order.add(orderObj)
            cloth_obj.save()

        # Return a response with the created order data
        return Response(OrderSerializer(orderObj).data, status=HTTP_201_CREATED)
    

@api_view(['POST'])
def send_otp(request):
    data = request.data

    if data.get('mobile_num') is None:
        return Response({
            'status' : 400,
            'message': 'key mobile number is required'
        })
    
    
    
    phone_number = data.get('mobile_num')

    otp = send_otp_to_phone(phone_number)

    return Response({
        'status' : 200,
        'message': 'Otp Sent',
        'otp':otp
    })

@api_view(["POST"])
def changePassword(request):
    data = request.data

    if data.get('mobile_num') is None:
        return Response({
            'status': 400,
            'message': 'key mobile number is required'
        })
    
    if data.get('password') is None:
        return Response({
            'status': 400,
            'message': 'password is required'
        })
    
    mobile_num = data.get('mobile_num')
    password = data.get('password')

    secret_key = settings.SECRET_KEY
    
    try:
        customer = Customer.objects.get(mobile_num=mobile_num)
        # Rehash the password using the same method as in the save() method
        hashed_password = make_password(password)
        customer.password = hashed_password
        customer.save()
    except Exception as e:
        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'mobile number is not registered'
        })
    
    return Response({
        'status': status.HTTP_201_CREATED,
        'message': 'password changed successfully'
    })



@api_view(["POST"])
def login_view(request):
    data = request.data

    # Ensure both mobile_num and password are provided
    if data.get('mobile_num') is None:
        return Response({
            'status': 400,
            'message': 'mobile number is required'
        })
    
    if data.get('password') is None:
        return Response({
            'status': 400,
            'message': 'password is required'
        })
    
    mobile_num = data.get('mobile_num')
    password = data.get('password')

    secret_key = settings.SECRET_KEY

    try:
        # Fetch the customer
        customer = Customer.objects.get(mobile_num=mobile_num)
    except Customer.DoesNotExist:
        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'mobile number is not registered'
        })
    
    # Concatenate the password, secret_key, and pincode (handle pincode being null or empty)
    
    # Compare the password using check_password, which safely compares hashes
    if check_password(password, customer.password):
        return Response({
            'status': status.HTTP_201_CREATED,
            'message': 'logged in successfully'
        })
    else:
        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'Invalid credentials'
        })