from django import forms
 
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

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



"""class RegisterForm(UserCreationForm):
    #first_name = forms.CharField(max_length=30)
    #last_name = forms.CharField(max_length=30)
    #id_number = forms.IntegerField() # id - 10 digits?

    def validate_only_letters(value):
        if not value.isalpha():
            raise forms.ValidationError(f'should only contain letters.')

    first_name = forms.CharField(
        max_length=30,
        validators=[validate_only_letters]
        )

    last_name = forms.CharField(
        max_length=30,
        validators=[validate_only_letters]
        )

    def validate_id_number(value):
        if len(str(value)) != 9:
            raise forms.ValidationError('The ID number must be a 9-digit number.')
    id_number = forms.IntegerField(validators=[validate_id_number])

    class Meta:
        model=User
        fields = ['username','first_name','last_name','id_number','email','password','password_repeat']

"""

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    id_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    


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
