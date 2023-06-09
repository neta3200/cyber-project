from django import forms

from .models import Customer

class customerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'First Name',
            'Last Name',
            'City',
            'Street Address',
            'Internet Speed',
        ]