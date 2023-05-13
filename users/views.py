from .forms import UserForm, RegisterForm, LoginForm ,ForgotPasswordForm,Sha1VerificationCodeForm,ResetPasswordForm


from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
import hashlib, random, smtplib, ssl
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

import hashlib, binascii, os

def loginPageReq(request):
    if request.method == 'GET':
        form = LoginForm()
        #return redirect('/login')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('/customers')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
    context = {
        'form': form, 
        'pageName': 'login',
        'pageTitle': 'Login',
        }
    return render(request, template_name="../templates/login.html", context=context)

def logoutReq(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('/login')


def registerPageReq(request):
    if request.method == 'GET':
        form = RegisterForm()
    
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST) 
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, 'You have singed up successfully.')
                login(request, user)
                #return redirect('posts')

    context = {
        'form': form,
        'pageName': 'register',
        'pageTitle': 'Register',

        }
    return render(request, template_name="../templates/register.html", context=context)

def aboutPageReq(request):
    context = {
        'pageName': 'about',
        'pageTitle': 'About',
        }
    return render(request, template_name="../templates/about.html", context=context)














def forgetPageReq(request):
    if request.method == 'GET':
        form = ForgotPasswordForm()
    else:
        if request.method == 'POST':
            form = ForgotPasswordForm(request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                randon_digits=random.getrandbits(10)
                sha1_encoded = hashlib.sha1(str(randon_digits).encode('utf-8')).hexdigest()
                # Send the random value to the user's email
                subject = 'Reset Password - Communication LTD'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                message = render_to_string('../templates/password-reset-sent.html', 
                {
                'hashed_code' : sha1_encoded,
                'protocol' : 'http',
                'domain' : '127.0.0.1:8000',
                'url' : '/verification-key-password',
                })
                send_mail(subject, message, email_from, recipient_list)
                return redirect('./sendEmail')

    context = { 
        'form':form,
        'pageName': 'forget',
        'pageTitle': 'Forget Password',
    }
    #auth_views.PasswordResetView.as_view(template_name="../templates/forget-pass.html")

    return render(request, template_name="../templates/forget-pass.html", context=context)


def sendEmail(request):
    context = {
        'pageName': 'sendEmail',
        'pageTitle': 'Email Sent',
        # 'title': 'email sent to the user',
        # 'page_name': 'sendEmail',
    }
    return render(request, template_name="../templates/reset_password_done.html", context = context)



def sha1_code_verification(request):

    form = Sha1VerificationCodeForm(request.POST)
    if form.is_valid():
        input_username = form.cleaned_data.get('username')
        input_code = form.cleaned_data.get('reset_code')
        #found_user = UsersData.objects.filter(username = input_username, resetCode = input_code)
        #if found_user.exists():
        #login(request)
        response = redirect('/reset-password/')
        response.set_cookie("isAuthenticated", "true")
        #found_user = UsersData.objects.get(username = input_username)
        #found_user.resetCode = None
        #found_user.save() 
        return response
    else:
        form = Sha1VerificationCodeForm()
        context = {
        'form': form,
        'page_name': 'Verify Reset Code',
        'pageTitle': 'Verify Reset Code',

        }
        return render(request, "verification-key-password.html", context = context)
    context = {
        'form': form,
        'page_name': 'Verify Reset Code',
        'pageTitle': 'Verify Reset Code',

    }
    return render(request, "verification-key-password.html", context = context)

def resetPassword(request):
    if request.method == 'GET':
        form = ResetPasswordForm()
    
    else:
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST) 
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                messages.success(request, 'You have changes password successfully.')
                login(request, user)
                #return redirect('posts')

        
   
    context = {
        'form': form,
        #'page_name': 'reset password',
        'pageName': 'reset password',
        'pageTitle': 'change password',
        }
    return render(request, "reset_password.html", context = context)
