
from django.contrib import messages
from django.http import response
from django.shortcuts import render, redirect
from django.http import Http404
from .models import Customer

def customersPageReq(request):
    result = None
    lastCustomer= None
    if request.method == 'GET':
        customerFirstName = request.GET.get('fname', None)
        customerLastName = request.GET.get('lname', None)
        customerCity = request.GET.get('city', None)
        #customerAddress = request.GET.get('address', None) 
        customerInternetSpeed = request.GET.get('speed', None)
    else:
        customerFirstName = request.POST.get('fname')
        customerLastName = request.POST.get('lname')
        customerCity = request.POST.get('city')
        #customerAddress = request.POST.get('address') 
        customerInternetSpeed = request.POST.get('speed')
        if not (customerFirstName.replace(' ', '').isalpha()) or not (customerFirstName.replace(' ', '').isalpha()): 
            return render (request, '../templates/http404.html')

    if  customerFirstName and customerLastName and customerCity and customerAddress and customerInternetSpeed:
        savecustomer = Customer(firstName= customerFirstName,lastName= customerLastName, city= customerCity, address= customerAddress, internetSpeed= customerInternetSpeed)
        savecustomer.save()
        get_last_client_query = "SELECT * FROM clients_client order by id DESC LIMIT 1;"
        res = Customer.objects.raw(get_last_client_query)
    
    context = {
    'pageName': 'customers',
    'customerFirstName': customerFirstName,
    'customerLastName': customerLastName,
    'customerCity': customerCity,
    #'customerAddress': customerAddress,
    'customerInternetSpeed': customerInternetSpeed,
    'pageTitle': 'Customers',
    #'secureMod': request.COOKIES['secureMod'],
    'c': result
    }
    return render(request, template_name="../templates/customers.html", context=context)