from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.conf import settings
from django.core.mail import send_mail
import random
import datetime

from auth_app.forms import CustomUserChangeForm, LoginForm, CustomUserCreationForm
from auth_app.models import UserModel

# Handlers

def otpGenerator():
    otp = random.randrange(100000, 999999)
    return str(otp)


def sendMail(otp:str, receivers:list):
    sender = settings.EMAIL_HOST_USER
    receivers = receivers
    msg = f'Your One Time Password (OTP) is {otp}, which expires in 5 minutes.\n\n\n\nPlease ignore if you have not sent it!'
    send_mail("OTP for resetting password", msg, sender, receivers)


# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponsePermanentRedirect(reverse('index'))
    form = LoginForm()  
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_password = form.cleaned_data['password']
            print(user_email, user_password)
            user = authenticate(email=user_email, password = user_password)
            print(user)

            if user is not None:
                login(request, user)

                if request.GET.get('next'):
                    return HttpResponsePermanentRedirect(request.GET.get('next'))

                return HttpResponsePermanentRedirect(reverse('all-blogs'))
             
            return render(request, 'auth_app/login.html', {'form':form, 'error':"Invalid Credentials!"})

        return render(request, 'auth_app/login.html', {'form':form})

    return render(request, 'auth_app/login.html', {'form':form})


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'auth_app/user_email.html')

    def post(self, request):
        if request.POST['user_email'] != "":
            user_email = request.POST.get("user_email")
            try:
                user = UserModel.objects.get(email=user_email)
            except UserModel.DoesNotExist:
                user = None
            if user != None:
                otp = otpGenerator() # generating otp
                user.otp = otp # storing otp in a variable
                user.otp_expiry = timezone.now() + datetime.timedelta(minutes=5) # setting otp expiry
                user.save() # saving all to the database
                request.session['user_email'] = user_email # storing email in session
                request.session['is_redirected'] = True
                sendMail(otp, [user_email]) # sending otp via email to the user
                return redirect(reverse('otp-verify')) # and redirecting to the otp entry page
            else:
                return render(request, 'auth_app/user_email.html', {"message":'Email not found!'})

        print(request.POST)
        return render(request, 'auth_app/user_email.html', {"message": "Please enter an email!"})


class VerifyOTPView(View):
    def get(self, request):
        if request.session.get('is_redirected') == True:
            return render(request, 'auth_app/verify_otp.html')
        return redirect(reverse('login'))
    
    def post(self, request):
        otpText = request.POST.get('otp_text')
        email = request.session.get('user_email')
        user = UserModel.objects.get(email = email)
        currentTime = timezone.now()
        if user.otp == otpText:
            if user.otp_expiry > currentTime: # type: ignore
                user.otp = None
                user.otp_expiry = None
                user.save()
                request.session.pop('user_email')
                login(request, user)
                return redirect(reverse('reset-password'))
            return render(request, 'auth_app/verify_otp.html', {"message":"OTP Expired"})
        return render(request, 'auth_app/verify_otp.html', {'message':"Invalid OTP"})


def user_register(request):
    # return HttpResponse('Register Page')
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'auth_app/register.html', {'form':form})

@login_required()
def accounts_view(request):
    user_id = request.user.id
    user = UserModel.objects.get(id=user_id)
    # print(user.date_joined)
    return render(request, "auth_app/accounts.html", {'user_data':user})


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'auth_app/update_password.html'
    success_url = reverse_lazy('account')
    

# class ResetPasswordView(View):
#     def get(self, request):
#         user = request.user
#         form = SetPasswordForm(user)
#         return render(request, 'auth_app/reset_password.html', {'form':form})

#     def post(self, request):
#         user = request.user
#         form = SetPasswordForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('account'))
#         return render(request, 'auth_app/reset_password.html', {'form':form})

class ResetPasswordView(PasswordChangeView):
    form_class = SetPasswordForm
    template_name = 'auth_app/reset_password.html'
    success_url = reverse_lazy('account')



@login_required()
def update_info_view(request):
    user_id = request.user.id
    user = UserModel.objects.get(id=user_id)
    form = CustomUserChangeForm(instance=user)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account'))
        return render(request, 'auth_app/update.html',{"form":form})
    return render(request, 'auth_app/update.html', {"form":form})


def user_logout(request):
    logout(request)
    return HttpResponsePermanentRedirect(reverse('index'))


def del_user(request):
    user_id = request.user.id
    UserModel.objects.get(id=user_id).delete()
    return HttpResponsePermanentRedirect(reverse('login'))


