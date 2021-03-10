from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'posts/baseLine.html', {'name': 'Index'})

def stream(request):
    return render(request, 'posts/baseLine.html', {'name': 'stream'})

def thread(request):
    return render(request, 'posts/baseLine.html', {'name': 'thread'})
