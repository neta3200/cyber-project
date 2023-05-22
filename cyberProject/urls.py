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
from django.contrib import admin
from django.urls import path
from users import views
from customers import views
from users.views import (loginPageReq, aboutPageReq, forgetPageReq, logoutReq,
                        user_change_pwd_view, user_changed_pwd_successfully_view, sendEmail, 
                        sha1_code_verification, user_create_view )  #registerPageReq
from customers.views import customersPageReq


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginPageReq),
    path('login/', loginPageReq),
    path('register/', user_create_view),
    path('about/', aboutPageReq),
    path('forget/', forgetPageReq),
    path('customers/', customersPageReq),
    path('logout/', logoutReq),
    path('forget/sendEmail', sendEmail),
    path('change-pwd/', user_change_pwd_view),
    path('change-pwd/done', user_changed_pwd_successfully_view),
    path('verification-key-password/', sha1_code_verification),
 ]
