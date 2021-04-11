from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Post
# change to classes

def index(request):
    allPosts = Post.objects.order_by('-date')
    print(allPosts[0].body)
    bodys = []
    for i in range(3):
        bodys.append(allPosts[i].body)
    return render(request, 'posts/baseLine.html', {'name': 'Index', 'bodys1': bodys, "allPosts": allPosts})

def stream(request):
    return render(request, 'posts/stream.html', {'name': 'stream'})

def thread(request, pId):
    post = Post.objects.get(pk = pId)
    return render(request, 'posts/thread.html', {'name': 'thread', 'pId': pId, 'post': post})
