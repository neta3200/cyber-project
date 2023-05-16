
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .models import Customer

def customersPageReq(request):
    result = None
    lastCustomer= None
    if request.method == 'GET':
        customerFirstName = request.GET.get('fname', None)
        customerLastName = request.GET.get('lname', None) 
    else:
        customerFirstName = request.POST.get('fname')
        customerLastName = request.POST.get('lname')


    
    context = {
    'pageName': 'customers',
    'customerFirstName': customerFirstName,
    'customerLastName': customerLastName,
    'pageTitle': 'Customers',
    #'secureMod': request.COOKIES['secureMod'],
    'c': result
    }
    return render(request, template_name="../templates/customers.html", context=context)
