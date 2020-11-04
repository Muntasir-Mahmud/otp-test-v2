from django.contrib import admin
from django.urls import path

from .views import ValidatePhoneSendOTP

app_name = 'account'

urlpatterns = [
    path('validate_phone/', ValidatePhoneSendOTP.as_view()),
]
