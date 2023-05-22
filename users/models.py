from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class UsersData(AbstractUser):
    resetCode = models.CharField(max_length=40, blank=True, default='', null=True)
    lastPasswords = models.JSONField(blank=True, default=dict)
 #     #Specify the required fields for user creation and management
    REQUIRED_FIELDS = ['email']