from .forms import RegisterForm, LoginForm

from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout


import random
import hashlib
import os
import json



def loginPageReq(request):
    
    if request.method == 'GET':
        form = LoginForm()

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
    return redirect('/')
    return response


def registerPageReq(request):
    newUser = None
    users= None
    if request.method == 'GET':
        if(request.GET):
            data = request.GET or None
            user = UsersData.objects.raw(f"SELECT * FROM users_usersdata WHERE username = '%s'" % (data['username']))
            if(len(list(user)) != 0 ):
                messages.info(request, "Are you sure you don't have a user?")
                if(len(list(user)) > 1 ):
                    users = list(user)
            elif (passwordVaildation(data['password1']) == False):
                messages.info(request, "The password does not meet the requirements try again")
            elif(data['password1'] != data['password2']):
                messages.info(request, "The passwords do not match try again")
            else:
                user = UserData.objects.create_user(
                    data['username'],
                    data['email'],
                    data['password1']
                )
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                UserLastPasswords = [
                    {
                        "passwords": [data['password1']]
                    }
                ]
                user.lastPasswords = json.dumps(UserLastPasswords)
                user_new = user
                user.save()
    else:
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            context = { 'form' : form }
            if (passwordVaildation(form.cleaned_data['password1']) == False):
                messages.info(request, "The password does not meet the requirements try again")
                return render(request, '../templates/register.html', context)
            if(form.cleaned_data['password1'] != form.cleaned_data['password2']):
                messages.info(request, "The passwords do not match try again")
                return render(request, '../templates/register.html', context)
            checkUsername = form.cleaned_data['username']
            user = UsersData.objects.raw(f"SELECT * FROM users_usersdata WHERE username = '%s'" % (checkUsername))
            if(len(list(user))!= 0):
                messages.info(request, "The user name is not valid")
                return render(request, '../templates/register.html', context)
            user = UsersData.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password1']
                    )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            passwordsObj = [
                {
                    "passwords": [form.cleaned_data['password']]
                }
            ]
            user.lastPasswords = json.dumps(passwordsObj)
            user.save()
            newUser = user
            messages.success(request, 'You have singed up successfully.')
            #login(request, user)
    form = RegisterForm()
    context = {
        'form': form,
        'pageName': 'register',
        'pageTitle': 'Register',
        'newUser': newUser,
        'users': users,
        }
    return render(request, template_name="../templates/register.html", context=context)
"""

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
"""


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
    return render(request, template_name="../templates/forgetpw.html",context=context)

def changePwdPageReq(request):
    return render(request, template_name="../templates/.html",context=context)

def passwordVaildation(password):
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(dir,"users/passwordRequirements.json")) as file:
        requiredmentsData = json.load(file)

    for s in requiredmentsData['specialCharacters']:
        speical+=password.count(s)
    
    numbers = sum(c.isdigit() for c in password)
    letters = sum(c.isalpha() for c in password)
    lowers  = sum(c.islower() for c in password)
    uppers  = sum(c.isupper() for c in password)
    
    if requiredmentsData['minLen'] > len(password):
        return False
    if requiredmentsData['minLenLowerLetter'] > lowers:
        return False
    if requiredmentsData['minLenUpperLetter'] > uppers:
        return False
    if requiredmentsData['minAlphaLetters'] > letters:
        return False
    if requiredmentsData['minLenSpeical'] > speical:
        return False
    
    return True



