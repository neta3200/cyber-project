from django import forms
 

#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)

class ChangePwdForm(forms.Form):
    existing_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    verify_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class ForgotPwdForm(forms.Form):
    email_address = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class VerifyCodeForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    reset_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class ResetPwdForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    verify_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))





#myClasses:



class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())


class ChangePasswordForm(forms.Form,PasswordResetView):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    verify_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        #model=User
        fields = ['old password','new password','verify new password',]

class Sha1VerificationCodeForm(forms.Form):
    reset_code = forms.CharField(widget=forms.TextInput())



# class ResetPasswordForm(forms.Form):
#     new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     verify_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     class Meta:
#         model=User
#         fields = ['old password','new password','verify new password',]

