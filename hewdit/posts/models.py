from django.db import models

# Create your models here.

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
