import random

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, PhoneOTP
from .forms import VerifyPhoneForm, VerifyOTPForm, RegisterForm
from .serializers import CreateUserSerializer


class ValidatePhoneSendOTP(View):
    form_class = VerifyPhoneForm
    model = User
    template_name = 'account/validate_phone.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        
        phone_number = request.POST.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return HttpResponse("<h1>Phone number already exists</h1>")

            else:
                key = send_otp(phone)
                print(phone_number)
                print('The OTP is: ', key)

                if key:
                    PhoneOTP.objects.create(
                        phone=phone,
                        otp=key,
                    )
                    return HttpResponse("<h1>success</h1>")

                else:
                    return HttpResponse("<h1>Error in sending OTP</h1>")

            return HttpResponse("<h1>success</h1>")


        else:
            return HttpResponse("<h1>Phone number is not given in post request</h1>")



def send_otp(phone):
    if phone:
        key = random.randint(999, 9999)
        return key

    else:
        return False


class ValidateOTP(View):
    form_class = VerifyOTPForm
    model = PhoneOTP
    template_name = 'account/validate_otp.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        phone = request.POST.get('phone', False)
        otp_sent = request.POST.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validate = True
                    old.save()
                    return HttpResponse("<h1>OTP MATCHED!!, kindly proceed for registration</h1>")

                else:
                    return HttpResponse("<h1>OTP incorrect, please try again</h1>")
                    
            else:
                return HttpResponse("<h1>Phone not recognised. Kindly request a new otp with this number</h1>")

        else:
            return HttpResponse("<h1>Either phone or otp was not recieved in Post request</h1>")


class Register(View):
    form_class = RegisterForm
    model = User
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone', False)
        password = request.POST.get('password', False)

        if phone and password:
            old_phn = PhoneOTP.objects.filter(phone__iexact = phone)
            if old_phn.exists():
                old_phn = old_phn.first()
                validated = old_phn.validate

                if validated:
                    user = User.objects.create_user(phone=phone, password=password)

                    user.save()
                    '''
                    serializer = CreateUserSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    old_phn.delete()
                    serializer.save()
                    '''
                    return HttpResponse("<h1>Accont Created</h1>")

                else:
                    return HttpResponse("<h1>OTP have not verified yet.</h1>")
                    
            else:
                return HttpResponse("<h1>Please verify phone first</h1>")
                

        else:
            return HttpResponse("<h1>Phone and password are not sent</h1>")
           