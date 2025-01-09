from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from django.conf import settings

from .helpers import send_otp_to_phone

from .models import Clothes, Customer, Order
from .serializers import ClothesSerializer, CustomerSerializer, OrderSerializer, LoginSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@api_view(['POST'])
def login_view(request):
    # Use the LoginSerializer to validate incoming data
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        if 'message' in serializer.validated_data:
            # If message exists, return it with a 200 OK status
            return Response({"message": serializer.validated_data["message"]}, status=status.HTTP_200_OK)
        else:
            # If no message, return the customer data
            return Response({"curr_user": serializer.validated_data["customer"]}, status=status.HTTP_200_OK)
    else:
        # If validation fails (e.g., missing mobile_num/password), send a 400 error
        return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("curr_user")
            # Do something with the authenticated user (e.g., return a token)
            return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = LoginSerializer

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
    print(data)

    if data.get('mobile_num') is None:
        return Response({
            'status' : 400,
            'message': 'key mobile number is required'
        })
    
    if data.get('password') is None:
        return Response({
            'status' : 400,
            'message': 'password is required'
        })
    
    mobile_num = data.get('mobile_num')
    password = data.get('password')

    secret_key = settings.SECRET_KEY
    
    try:
        customer = Customer.objects.get(mobile_num = mobile_num)
        hashed_password = make_password(password+secret_key+customer.pincode)
        customer.password = hashed_password
        customer.save()
    except Exception as e:
        print(e)
        return Response({
            'status' : status.HTTP_404_NOT_FOUND,
            'message':'mobile number is not registered'
        })
    

    return Response({
        'status': status.HTTP_201_CREATED,
        'message' : 'password changed successfully'
    })
