from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
        fields = ['username','first_name','last_name','id_number','email','password1','password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)