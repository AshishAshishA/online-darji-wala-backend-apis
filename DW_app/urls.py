from django.urls import path,include

from .views import CustomerViewSet, changePassword,ClothesViewSet,OrderViewSet,login_view,send_otp

from rest_framework import routers

router = routers.DefaultRouter()
router.register('customers', CustomerViewSet, basename='customer_details')
# router.register('login', LoginViewSet, basename="login-view")
router.register('register', CustomerViewSet, basename="register")
router.register('clothes', ClothesViewSet, basename='clothes_list')
router.register('order',OrderViewSet,basename="order")

urlpatterns = [
    path('change/password/',changePassword, name='change-password' ),
    path('login/', login_view, name="login"),
    path('send_otp/',send_otp, name="send-otp"),
    path('', include(router.urls)),
]