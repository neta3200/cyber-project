from django import forms

from .models import Customers

class ClientForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'First Name',
            'Last Name',
        ]
