from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField('Email Address', unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
