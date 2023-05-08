from django.db import models

# Create your models here.

class Customer(models.Model):
    firstName=models.CharField(max_length=200)
    lastName=models.CharField(max_length=200)
    city=models.CharField(max_length=200)

    def __str__(self):
        return self.firstName, self.lastName, self.city