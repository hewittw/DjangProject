from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your models here.
# add user model from dr. j's git here

# class Thread(models.Model):
#     body = models.CharField(max_length=2000)
#     date = models.DateTimeField('date posted')
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None)

class Post(models.Model):
    body = models.TextField(max_length=2000) # change to text field
    #image = models.ImageField()
    date = models.DateTimeField('date posted')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True,
                                blank=True)

# using built in user - ask dr. j if need to add?
