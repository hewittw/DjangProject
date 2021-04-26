from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



class Post(models.Model):
    """
    This is the main model in my website. Each post can act as a stand-alone post or will
    soon be able to act as a 'comment' type post as well.
    """
    title = models.CharField(max_length=200, default="")
    body = models.TextField(max_length=2000)
    date = models.DateTimeField('date posted')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True,
                                blank=True)
    userPosted = models.ForeignKey(User, on_delete=models.CASCADE) # maybe change this to the profile - need to make this decision
    likes = models.IntegerField(blank=True, null=True) # not using yet in templates - will implement later

    # plan to define a string method that names it correclty in the admin interface - use the pk attribute

class Profile(models.Model):
    """
    This is model extends the built in user model to allow each user to have a profile
    with personal data that is associated to their account.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.CharField(max_length=200, default="")
    profilePic = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    # profile pic does not display correctly yet in the template - another thing I will work on later
