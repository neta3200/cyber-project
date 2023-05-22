
from django.contrib import messages
from django.http import response
from django.shortcuts import render, redirect
from django.http import Http404
from .models import Customer

def customersPageReq(request):
    result = []

    if request.method == 'POST':

        customerFirstName = request.POST.get('firstName')
        customerLastName = request.POST.get('lastName')
        customerCity = request.POST.get('city')
        #customerAddress = request.POST.get('address') 
        #customerInternetSpeed = request.POST.get('speed')
        if not (customerFirstName.replace(' ', '').isalpha()) or not (customerFirstName.replace(' ', '').isalpha()): 
            #return render (request, '../templates/http404.html')
            messages.error(request, "not found.")

        print("customerFirstName post:",customerFirstName)
    else:
        customerFirstName = request.GET.get('firstName', None)
        customerLastName = request.GET.get('lastName', None)
        customerCity = request.GET.get('city', None)
        #customerAddress = request.GET.get('address', None) 
        #customerInternetSpeed = request.GET.get('speed', None)
        print("customerFirstName get:",customerFirstName)


    #check if the costumer is not empty value than add costumer to DB:
    if  customerFirstName and customerLastName and customerCity:
      
        customer_in_DB = Customer(firstName= customerFirstName,lastName= customerLastName, city= customerCity)
        print("customer_in_DB:",customer_in_DB)
        customer_in_DB.save()
        sql_query_fetch_customer = "SELECT * FROM customers_customer order by id DESC;"
        result = Customer.objects.raw(sql_query_fetch_customer)
        print("result: ", result)



    context = {
    'pageName': 'customers',
    'customerFirstName': customerFirstName,
    'customerLastName': customerLastName,
    'customerCity': customerCity,
    #'customerAddress': customerAddress,
    #'customerInternetSpeed': customerInternetSpeed,
    'pageTitle': 'Customers',
    #'secureMod': request.COOKIES['secureMod'],
    'customers': result
    }
    return render(request, template_name="../templates/customers.html", context=context)