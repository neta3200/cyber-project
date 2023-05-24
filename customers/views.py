
from .models import Customer
from django.contrib import messages
from django.shortcuts import render
#from django.http import Http404


# def customersPageReq(request):
#     result = []

#     if request.method == 'POST':

#         customerFirstName = request.POST.get('firstName')
#         customerLastName = request.POST.get('lastName')
#         customerCity = request.POST.get('city')
#         #customerAddress = request.POST.get('address') 
#         #customerInternetSpeed = request.POST.get('speed')
#         if not (customerFirstName.replace(' ', '').isalpha()) or not (customerFirstName.replace(' ', '').isalpha()): 
#             #return render (request, '../templates/http404.html')
#             messages.error(request, "not found.")

#         print("customerFirstName POST:",customerFirstName)
#     else:
#         customerFirstName = request.GET.get('firstName', None)
#         customerLastName = request.GET.get('lastName', None)
#         customerCity = request.GET.get('city', None)
#         #customerAddress = request.GET.get('address', None) 
#         #customerInternetSpeed = request.GET.get('speed', None)
#         print("customerFirstName GET:",customerFirstName)


#     #check if the costumer is not empty value than add costumer to DB:
#     #if customerFirstName==True then...
#     if  customerFirstName and customerLastName and customerCity and (request.COOKIES['secureMod'] == 'true'):
#         print("customerFirstName secureMod is true: ",customerFirstName)
#         print("customerLastName secureMod is true: ",customerLastName)
#         print("customerCity secureMod is true: ",customerCity)

#         customer_in_DB = Customer(firstName= customerFirstName,lastName= customerLastName, city= customerCity)
#         print("customer_in_DB secureMod is true:",customer_in_DB)
#         customer_in_DB.save()
#         print("customer_in_DB after save secureMod is true:",customer_in_DB)
#         sql_query_fetch_customer = "SELECT * FROM customers_customer order by id DESC;"
#         result = Customer.objects.raw(sql_query_fetch_customer)
#         print("result secureMod is true: ", result)
#     elif customerFirstName and customerLastName and customerCity and (request.COOKIES['secureMod'] != 'true'):
#         print("customerFirstName secureMod is FALSE: ",customerFirstName)
#         print("customerLastName secureMod is FALSE: ",customerLastName)
#         print("customerCity secureMod is FALSE: ",customerCity)

#         customer_in_DB = Customer(firstName= customerFirstName,lastName= customerLastName, city= customerCity)
#         print("customer_in_DB secureMod is FALSE:",customer_in_DB)
#         customer_in_DB.save()
#         print("customer_in_DB after save secureMod is FALSE:",customer_in_DB)
#         sql_query_fetch_customer = f"SELECT * FROM customers_customer WHERE firstName = '%s'  AND lastName = '%s' AND city = '%s';" % (customerFirstName,
#              customerLastName,customerCity)
#         result = Customer.objects.raw(sql_query_fetch_customer)
#         print("result secureMod is FALSE: ", result)
#     else:
#         sql_query_fetch_customer = "SELECT * FROM customers_customer order by id DESC;"
#         result = Customer.objects.raw(sql_query_fetch_customer)
#         print("result costumer empty value or another...: ", result)

#     context = {
#     'pageName': 'customers',
#     'customerFirstName': customerFirstName,
#     'customerLastName': customerLastName,
#     'customerCity': customerCity,
#     #'customerAddress': customerAddress,
#     #'customerInternetSpeed': customerInternetSpeed,
#     'pageTitle': 'Customers',
#     'secureMod': request.COOKIES['secureMod'],
#     'customers': result
#     }
#     return render(request, template_name="../templates/customers.html", context=context)



def customersPageReq(request):
    result = []
    

    if request.method == 'POST':
        customerFirstName = request.POST.get('firstName')
        customerLastName = request.POST.get('lastName')
        customerCity = request.POST.get('city')
        #customerAddress = request.POST.get('address') 
        #customerInternetSpeed = request.POST.get('speed')
        #secure STORED XSS
        if not (customerFirstName.replace(' ', '').isalpha()) or not (customerLastName.replace(' ', '').isalpha()) or not (customerLastName.replace(' ', '').isalpha()): 
            print("customerFirstName in POST replace:", customerFirstName)
            return render (request, 'history-error.html')

        print("customerFirstName in POST:", customerFirstName)
        
    else:
        customerFirstName = request.GET.get('firstName', None)
        customerLastName = request.GET.get('lastName', None)
        customerCity = request.GET.get('city', None)
        #customerAddress = request.GET.get('address',None) 
        #customerInternetSpeed = request.GET.get('speed',None)
        print("customerFirstName in GET:", customerFirstName)
        


    if customerFirstName and customerLastName and customerCity:
        customer_in_DB = Customer(firstName= customerFirstName,lastName= customerLastName, city= customerCity)
        customer_in_DB.save()
        if request.COOKIES['secureMod'] == 'true':
            sqlQuery = "SELECT * FROM customers_customer order by id DESC LIMIT 1;"
            result = Customer.objects.raw(sqlQuery)
            print("secureMod TRUE inside IF: ")
        else:
            #SQL vulnerability
            sqlQuery = f"SELECT * FROM customers_customer WHERE firstName = '%s' AND lastName = '%s' AND city = '%s';" % (customerFirstName,
                                 customerLastName,customerCity)
            result = Customer.objects.raw(sqlQuery, [customerFirstName, customerLastName, customerCity])
            print("secureMod FALSE inside IF: ")


    else:
        sqlQuery = "SELECT * FROM customers_customer order by id DESC LIMIT 1;"
        result = Customer.objects.raw(sqlQuery)
        print("secureMod FALSE inside ELSE: ")

            


    context = { 
        'pageName': 'customers',
        'customerFirstName': customerFirstName,
        'customerLastName': customerLastName,
        'customerCity': customerCity,
        #'customerAddress': customerAddress,
        #'customerInternetSpeed': customerInternetSpeed,
        'pageTitle': 'Customers',
        'secureMod': request.COOKIES['secureMod'],
        'customers': result
    }
    return render(request, template_name="../templates/customers.html", context=context)