from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    ROLE = (("User", "User"),
                ("Seller", "Seller"),
                ("Admin", "Admin"),
                
                )
    role = models.CharField(max_length=120, choices=ROLE, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    


    def __str__(self):
        return self.username
    