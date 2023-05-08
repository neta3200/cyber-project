from .forms import UserForm, RegisterForm, LoginForm ,ForgotPasswordForm, ChangePasswordForm


from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
<<<<<<< HEAD
import hashlib, random, smtplib, ssl
=======
from django.contrib.auth import views as auth_views
>>>>>>> 65c62c4afb9607dacdf90ed713649dcc9f8900e9


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
        form=ForgotPasswordForm()
    else:
        if request.method == 'POST':
            form = ForgotPasswordForm(request.POST) 
            if form.is_valid(): 
                reset_email_key=hashlib.sha1(str(random.getrandbits(160)).encode('utf-8')).hexdigest()
                #smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
                #email_context=ssl.create_default_context()
                #smtp.starttls(context=email_context)
                #smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                #smtp.sendmail(EMAIL_HOST_USER, form.email_address, reset_email_key)
                smtp = smtplib.SMTP('smtp.gmail.com', 587)
                email_context=ssl.create_default_context()
                smtp.starttls(context=email_context)
                smtp.login('cybernmmd@gmail.com', 'zxcasdqwe1!')
                smtp.sendmail('cybernmmd@gmail.com', form.email_address, reset_email_key)
                return redirect(url_for('auth.verify', messages = message , user_email = form.email_address))

    context = { 
        'form':form,
        'pageName': 'forget',
        'pageTitle': 'Forget Password',
    }
    auth_views.PasswordResetView.as_view(template_name="../templates/forget-pass.html")
    return render(request, template_name="../templates/forget-pass.html", context=context)

def changePwdPageReq(request):

    if request.method == 'GET':
        form=ChangePasswordForm()
    else:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST) 
            #if form.is_valid(): 
    context = { 
        'form':form,
        'pageName': 'forget',
        'pageTitle': 'Forget Password',
    }
    return render(request, template_name="../templates/change-pass.html",context=context)
