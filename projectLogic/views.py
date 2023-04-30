from django.shortcuts import render, redirect
from django.template.loader import render_to_string

def index(request):
    return render(request, template_name="../templates/login.html")


def login_request(request):
    context = { 
        'pageName': 'login',
        'pageTitle': 'Login',
        }
    return render(request, template_name="../templates/login.html", context=context)


def registerPage(request):
    context = { 
        'pageName': 'register',
        'pageTitle': 'Register',

        }
    return render(request, template_name="../templates/register.html", context=context)

def aboutPage(request):
    context = {
        'pageName': 'about',
        'pageTitle': 'About',
        }
    return render(request, template_name="../templates/about.html", context=context)

def forgetPage(request):
    context = { 
        'pageName': 'forget',
        'pageTitle': 'Forget Password',
    }
    return render(request, template_name="../templates/forgetpw.html",context=context)