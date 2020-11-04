from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
 
from .models import User

import random


class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'Phone number already exists'
                })

            else:
                key = send_otp(phone)
                if key:
                    pass

                else:
                    return Response({
                        'status': False,
                        'detail': 'Error in sending OTP'
                    })

        else:
            return Response({
                'status': False,
                'details': 'Phone number is not given in post request'
            })


def send_otp(phone):
    if phone:
        key = random.randint(999, 9999)
        return key

    else:
        return False