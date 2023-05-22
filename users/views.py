from .forms import UserForm, RegisterForm, LoginForm, ChangePwdForm, ForgotPasswordForm, Sha1VerificationCodeForm
from .models import UsersData 

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

import hashlib, binascii, os, json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
                user_exist_in_DB = UsersData.objects.filter(email = email).exists()
                if user_exist_in_DB:

                    randon_digits=random.getrandbits(10)
                    sha1_encoded = hashlib.sha1(str(randon_digits).encode('utf-8')).hexdigest()
                    # Send the random value to the user's email
                    subject = 'Reset Password - Communication LTD'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    message = render_to_string('../templates/password-reset-sent.html', 
                    {
                    #'user': user,
                    'hashed_code' : sha1_encoded,
                    'protocol' : 'http',
                    'domain' : '127.0.0.1:8000',
                    'url' : '/verification-key-password',
                    })
                    send_mail(subject, message, email_from, recipient_list)
                    user_in_DB=UsersData.objects.get(email = email)
                    user_in_DB.resetCode=sha1_encoded
                    user_in_DB.save()
                    return redirect('./sendEmail')
                else:
                    context = { 
                         'form':form,
                        }
                    messages.error(request, "Wrong Email try again.")
                    #return render(request, template_name="../templates/forget-pass.html", context=context)

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


def passwordNotInLasts(user, new_password):
    policy = load_user_create_requierments("cyberProject/passwordRequirements.json")
    if(policy['password_history'] <= 0):
        return True
    # First change (exisiting users before code change)
    if (user.lastPasswords == ''):
        pass_obj = [
            {
                "passwords": [new_password]
            }
        ]
        user.lastPasswords = json.dumps(pass_obj)
        user.save()
        return True
    else:
        pass_obj = json.loads(user.lastPasswords)
        pass_obj = pass_obj[0]['passwords']
        for password in pass_obj:
            if (password == new_password):
                return False
        # delete first saved password
        if(len(pass_obj) == policy['password_history']):
            del pass_obj[0]
        pass_obj.append(new_password)
        pass_obj = [
            {
                "passwords": pass_obj
            }
        ]
        user.lastPasswords = json.dumps(pass_obj)
        user.save()
        return True
    

def sha1_code_verification(request):
    form = Sha1VerificationCodeForm(request.POST)
    if form.is_valid():
        #code enter in form
        user_reset_code_entered = form.cleaned_data.get('reset_code')
        print("reset_code_in_DB: ",user_reset_code_entered)
        #check if the entered code is in the DB of the user
        user_reset_code_in_DB = UsersData.objects.filter(resetCode = user_reset_code_entered).exists()
        print("user_exist_in_DB: ",user_reset_code_in_DB)

        if user_reset_code_in_DB:
            user_in_DB = UsersData.objects.get(resetCode = user_reset_code_entered)
            #the actual code in the DB
            print("user_in_DB.resetCode: ",user_in_DB.resetCode)
            print("user_in_DB: ",user_in_DB)
            user_in_DB.resetCode = None
            user_in_DB.save() 
            #return redirect('./sendEmail')
            context = {
                'page_name': 'changePass',
                'pageTitle': 'Change password',
            }
            return render(request, "../templates/user_change_pwd.html", context = context)

        else:
            messages.error(request, "You entered an incorrect code, please try again")

    else:
        form = Sha1VerificationCodeForm()
        context = {
        'form': form,
        'page_name': 'Verify Reset Code',
        'pageTitle': 'Verify Reset Code',
        }
        #messages.error(request, "NOT RIGHT CODE.")
        #return render(request, "verification-key-password.html", context = context)
    context = {
        'form': form,
        'page_name': 'Verify Reset Code',
        'pageTitle': 'Verify Reset Code',
    }
    return render(request, "verification-key-password.html", context = context)

def user_change_pwd_view(request):

    form = ChangePwdForm(request.POST or None)
    context = {
        'form' : form,
        'pageName': 'changePassword',
        'pageTitle': 'Change Password',
    }
    if form.is_valid():
        if not is_difference_password(form.cleaned_data['new_password'], form.cleaned_data['verify_password']):
            messages.info(request, "The passwords do not match, please try again.")
            return render(request, "../templates/user_change_pwd.html", context = context)
        if not passwordVaildation(form.cleaned_data['new_password']):
            messages.info(request, "The password you entered does not meet the requirements, please try again.")
            return render(request, "../templates/user_change_pwd.html", context = context)
        u = UsersData.objects.get(username = request.user)
        if(u is not None):
            if(u.check_password(form.cleaned_data['existing_password'])):
                if(passwordNotInLasts(u, form.cleaned_data['new_password'])):
                    u.set_password(form.cleaned_data['new_password'])
                    u.save()
                    response = redirect('/change-pwd/done')
                    response.set_cookie("isAuthenticated", "false")
                    return response
                else:
                    messages.info(request, "You have used this password before, please try again.")
                    return render(request, "../templates/user_change_pwd.html", context = context)
            else:
                messages.info(request, "The exising password is not correct, please try again.")
                return render(request, "../templates/user_change_pwd.html", context = context)
        else:
            messages.info(request, "Error, please try again.")
            return render(request, "../templates/user_change_pwd.html", context = context)
    return render(request, "../templates/user_change_pwd.html", context = context)

def is_difference_password(password, password_repeat):
    return password == password_repeat

def passwordVaildation(password):
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(dir,"cyberProject/passwordRequirements.json")) as file:
        requiredmentsData = json.load(file)

    for s in requiredmentsData['password']['specialCharacters']:
        speical+=password.count(s)
    
    numbers = sum(c.isdigit() for c in password)
    letters = sum(c.isalpha() for c in password)
    lowers  = sum(c.islower() for c in password)
    uppers  = sum(c.isupper() for c in password)
    
    if requiredmentsData['password']['minLen'] > len(password):
        return False
    if requiredmentsData['password']['minLenLowerLetter'] > lowers:
        return False
    if requiredmentsData['password']['minLenUpperLetter'] > uppers:
        return False
    if requiredmentsData['password']['minAlphaLetters'] > letters:
        return False
    if requiredmentsData['password']['minLenSpeical'] > speical:
        return False
    
    return True


def load_user_create_requierments(path_to_req):
    with open(os.path.join(BASE_DIR, path_to_req)) as file:
        data = json.load(file)
    return data


def user_changed_pwd_successfully_view(request):
    context = {
        'title': 'Password changed successfully',
        'page_name': 'done',
    }
    return render(request, '../templates/password-reset-done.html', context = context)    
