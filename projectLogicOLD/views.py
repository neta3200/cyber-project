from .forms import UserForm, RegisterForm, LoginForm

from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout



def loginPageReq(request):
    form = LoginForm()
    context = {
        'form': form, 
        'pageName': 'login',
        'pageTitle': 'Login',
        }
    return render(request, template_name="../templates/login.html", context=context)


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
    return render(request, template_name="../templates/forgetpw.html",context=context)