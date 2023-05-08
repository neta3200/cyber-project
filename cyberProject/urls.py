"""
URL configuration for cyberProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
"""from projectLogic.views import loginPageReq, registerPageReq, aboutPageReq, forgetPageReq
from projectLogic import views"""
from users import views
from customers import views
from users.views import loginPageReq, registerPageReq, aboutPageReq, forgetPageReq, changePwdPageReq, logoutReq, sendEmail
from customers.views import customersPageReq


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginPageReq),
    path('login/', loginPageReq),
    path('register/', registerPageReq),
    path('about/', aboutPageReq),
    path('forget/', forgetPageReq),
    path('password-reset-sent/', sendEmail),
    path('customers/', customersPageReq),
    path('changepwd/', changePwdPageReq),
    path('logout/', logoutReq),
    
    #Reset password
    #path('reset_password/', 
    #auth_views.PasswordResetView.as_view(template_name="password-reset-form.html"),
    #name='password_reset'),

    #path('reset_password/done', 
    #auth_views.PasswordResetDoneView.as_view(template_name="password-reset-sent.html"),
    #name='password_reset_done'),

    #path('reset/<uidb64>/<token>/',
    #auth_views.PasswordResetConfirmView.as_view(template_name="reset_password_done.html"),
    #name='password_reset_confirm'),

    #path('reset_password/complete/', 
    #auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
    #name='password_reset_complete'),
    
 ]
