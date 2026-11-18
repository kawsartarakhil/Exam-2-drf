from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    roles = [
        ('school_admin', 'School Administrator'),
        ('regional_admin', 'Regional Administrator'),
        ('super_admin', 'Super Administrator'),
    ]

    role = models.CharField(max_length=20,choices=roles)
    institution = models.ForeignKey("library.Institution",on_delete=models.SET_NULL,null=True,blank=True)
    region = models.ForeignKey("library.Region", on_delete=models.SET_NULL,null=True,blank=True)
