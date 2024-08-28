from django.db import models

from users.models import User


# Create your models here.

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
