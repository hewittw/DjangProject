from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Profile
import datetime
from django.template import loader

# swtich to class based views

def index(request):
    """
    This will the be the home page view where the user signs in. Currently
    displays little data as I have not created the forms for the user to login with.
    """
    # allPosts = Post.objects.order_by('-date')
    # print(allPosts[0].body)
    # bodys = []
    # for i in range(3):
    #     bodys.append(allPosts[i].body)
    # return render(request, 'posts/baseLine.html', {'name': 'Index', 'bodys1': bodys, "allPosts": allPosts})
# It has forms that redirect to itself, so check if this form data is present
    if request.POST:
        # This tests if the form is the log *in* form
        if 'inputUsername' in request.POST.keys():
            # IF so, try to authentircate
            user = authenticate(username=request.POST['inputUsername'],
                password=request.POST['inputPassword'])
            if user is not None:
                # IF success, then use the login function so the session persists.
                login(request, user)
            else:
                pass
                # Message for failed login.
        # This tests if the form is the log *out* form
        else:
            # If so, don't need to check anything else, just kill the session.
            logout(request)


    # After we chec the forms, set a flag for use in the template.
    if request.user.is_authenticated:
        return redirect('/posts/stream')
    # Find the template
    template = loader.get_template('posts/baseLine.html')
    # The home page will show *all* posts for now.
    context = {}

    return HttpResponse(template.render(context, request))


def stream(request):
    """
    This is the main page of Hewdit. Think of it like a for you page or main stream of posts.
    """
    if request.method == 'POST':
        allProfiles = Profile.objects.all()
        print(request.POST)
        print("here")
        newPost = Post( title = request.POST['postTitle'],
                        body = request.POST['text'],
                        date = datetime.datetime.today(),
                        parent = None,
                        userPosted = request.user,
                        likes = 0)
        newPost.save()
    # get is used naturally
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
