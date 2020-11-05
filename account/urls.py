from django.contrib import admin
from django.urls import path

from .views import ValidatePhoneSendOTP, ValidateOTP, Register

app_name = 'account'

urlpatterns = [
    path('validate_phone/', ValidatePhoneSendOTP.as_view(), name='validate_phone'),
    path('validate_otp/', ValidateOTP.as_view(), name='validate_otp'),
    path('register/', Register.as_view()),
]
