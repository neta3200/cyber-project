from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser

# class UsersData(AbstractUser):
#     resetCode = models.CharField(max_length=40, blank=True, default='', null=True)
#     lastPasswords = models.JSONField(blank=True, default=dict)
    