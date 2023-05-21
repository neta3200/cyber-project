from .forms import UserForm, RegisterForm, LoginForm, ChangePwdForm

from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout

from .models import UsersData

import os
import json

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
    context = { 
        'pageName': 'forget',
        'pageTitle': 'Forget Password',
    }
    return render(request, template_name="../templates/forget-pass.html",context=context)

def user_change_pwd_view(request):
    form = ChangePwdForm(request.POST or None)
    context = {
        'form' : form,
        'page_name': 'change-pwd',
    }
    if form.is_valid():
        if not is_difference_password(form.cleaned_data['new_password'], form.cleaned_data['verify_password']):
            messages.info(request, "The passwords do not match, please try again.")
            return render(request, "../templates/user_change_pwd.html", context = context)
        if not is_valid_password(form.cleaned_data['new_password']):
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

def is_valid_password(password):
    count_digit = sum(c.isdigit() for c in password)
    count_alpha = sum(c.isalpha() for c in password)
    count_lower = sum(c.islower() for c in password)
    count_upper = sum(c.isupper() for c in password)
    count_special_char = 0
    req = load_user_create_requierments("cyberProject/pass_req.json")
    for special_char in req['password_content']['special_characters']:
        count_special_char += password.count(special_char)

    if req['min_length'] == len(password):
        return False
    if count_digit < req['password_content']['min_length_digit']:
        return False
    if count_alpha < req['password_content']['min_length_alpha']:
        return False
    if count_lower < req['password_content']['min_length_lower']:
        return False
    if count_upper < req['password_content']['min_length_upper']:
        return False
    if count_special_char < req['password_content']['min_length_special']:
        return False
    return True

def load_user_create_requierments(path_to_req):
    with open(os.path.join(BASE_DIR, path_to_req)) as file:
        data = json.load(file)
    return data

def passwordNotInLasts(user, new_password):
    policy = load_user_create_requierments("cyberProject/pass_req.json")
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

def user_changed_pwd_successfully_view(request):
    context = {
        'title': 'Password changed successfully',
        'page_name': 'done',
    }
    return render(request, '../templates/password-reset-done.html', context = context)