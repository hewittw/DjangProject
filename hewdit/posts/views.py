from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Profile

def index(request):
    """
    This will the be the home page view where the user signs in. Currently
    displays little data as I have not created the forms for the user to login with.
    """
    allPosts = Post.objects.order_by('-date')
    print(allPosts[0].body)
    bodys = []
    for i in range(3):
        bodys.append(allPosts[i].body)
    return render(request, 'posts/baseLine.html', {'name': 'Index', 'bodys1': bodys, "allPosts": allPosts})

def stream(request):
    """
    This is the main page of Hewdit. Think of it like a for you page or main stream of posts.
    """
    allPosts = Post.objects.order_by('-date')
    return render(request, 'posts/stream.html', {'name': 'stream', "allPosts": allPosts})

def thread(request, pId):
    """
    This view allows the user to specifically view just one post. Does not display comments yet.
    """
    post = Post.objects.get(pk = pId)
    return render(request, 'posts/thread.html', {'name': 'thread', 'pId': pId, 'pst': post})

def profile(request, profileId):
    """
    This view is like a user's profile page. Right now it just displays their profile pic and bio
    """
    profile = Profile.objects.get(pk = profileId)
    return render(request, 'posts/profile.html', {'name': 'profile', 'pId': profileId, 'profile': profile})
