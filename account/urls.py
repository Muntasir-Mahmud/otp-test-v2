from django.contrib import admin
from django.urls import path

from .views import ValidatePhoneSendOTP, ValidateOTP, Register

app_name = 'account'

urlpatterns = [
    path('validate_phone/', ValidatePhoneSendOTP.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('register/', Register.as_view()),
]
