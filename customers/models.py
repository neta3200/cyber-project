from django.db import models

# Create your models here.

class Customer(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    #city=
    #address=
    #internetSpeed=