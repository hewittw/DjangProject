from django.db import models

# Create your models here.
class Post(models.Model):
    body = models.CharField(max_length=2000)
    #image = models.ImageField()
    date = models.DateTimeField('date posted')
    #parent = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

# using built in user - ask dr. j if need to add?
