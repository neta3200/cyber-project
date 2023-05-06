
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

def customersPageReq(request):
    context = {
    'pageName': 'customers',
    'pageTitle': 'Customers',
    }
    return render(request, template_name="../templates/customers.html", context=context)
