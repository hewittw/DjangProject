from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Profile
import datetime
from django.template import loader

#------------------------------------------------------------------------------#

def index(request):
    """
    Purpose: This is the user login in page. This view is the default view, ie it loads
    with 'post/'. This view can only be accessed if the user is logged out - this was
    done on purpose and models instagrams login theory that only a logged-in user
    can use the site.
    Parameters: Request (django parameter for view)
    Returns: An HttpResponse
    """

    # if post method is called
    if request.POST:
        # checking to see if user attempted to login
        if 'inputUsername' in request.POST.keys():
            # authenticate the user using built in django user functions (so helpful)
            user = authenticate(username=request.POST['inputUsername'],
                   password=request.POST['inputPassword'])
            if user is not None:
                # if authenticate worked then login
                login(request, user)

        else:
            # If nothing, means user is logging out
            logout(request)


    # if user logged-in/is logged-in go to stream view
    if request.user.is_authenticated:
        return redirect('/posts/stream')
    # Find the template
    template = loader.get_template('posts/baseLine.html')
    # The home page will show *all* posts for now.
    context = {}

    return HttpResponse(template.render(context, request))

#------------------------------------------------------------------------------#

def createProfile(request):
    """
    Purpose: This view allows a new user to create a profile so they can access
    the site.
    Parameters: request (django parameter)
    Returns: A render call that is passed the createProfile.html
    """
    # see if user is logged-in
    if request.user.is_authenticated:
        return redirect('/posts/stream')

    # if post method is called
    if request.POST:
        # create new user using the data entered
        try:
            newUser = User.objects.create_user(username = request.POST['username'],
                                email = request.POST['email'],
                                password = request.POST['password'],)

            # create profile that corresponds to user - have a 1:1 relationship
            newProfile = Profile(user = newUser,
                                 bio = request.POST['bio'], )
            newProfile.save()

            login(request, newUser) # automatic login
            return redirect('/posts/') # go to stream because logged-in

        except:
            print("creating a new user did not work")

    return render(request, 'posts/createProfile.html', {'name': 'Create Profile'})

#------------------------------------------------------------------------------#

def stream(request):
    """
    Purpose: This is the main page of Hewdit. Think of it like a for you page
    or main stream of posts. Also, let the user create posts.
    Parameters: Request (django parameter for view)
    Returns: A render call that is passed the stream.html template and all the post
    and user information needed to generate the stream page.
    """
    # if user is not logged-in, go to index
    if request.user.is_authenticated != True:
        return redirect('/posts/')

    # if post method is called
    if request.method == 'POST':
        allProfiles = Profile.objects.all()
        try:
            # create a new post using UTC time and data that the user inputted
            newPost = Post( title = request.POST['postTitle'],
                          body = request.POST['text'],
                          date = datetime.datetime.today(),
                          parent = None,
                          userPosted = request.user,
                          likes = 0, )
            newPost.save()
        except:
            # in case some error occurs so program doesn't crash - for debugging
            print("An exception occurred")

        # reload the page after post is added so if the user refreshes the page the post is not added to the database twice
        return redirect('/posts/stream')

    # get user so the go-to-profile button can be generated in view
    currentUser = request.user

    # get all top level posts for stream view
    allPosts = Post.objects.filter(parent=None).order_by('-date') # making sure only posts, not comments displayed
    return render(request, 'posts/stream.html', {'name': 'stream', "allPosts": allPosts, 'currentUser': currentUser})

#------------------------------------------------------------------------------#

def traverseComments(pId, lvl):
    """
    Purpose: Using a recursive function, create a master list of comments where
    each index in the list is a dictionary. Each dictionary has two keys and corresponding
    values: a comment object and its corresponding level - how deep in the sub-comment
    threat it is.
    Parameters: The post Id from the top level post that is currently being used in
    thread view and the lvl (int) of the current post (lvl = position in the layers of comments)
    Returns: commentLst, a master list of dictionries of all the comments for one
    particular top-level post.
    """
    # get the current top level post (changes as the function gets deeper into the comment thread)
    post = Post.objects.get(pk = pId)
    allComments = Post.objects.filter(parent=post).order_by('-date') # get all subcomments for post
    commentLst = []
    for comment in allComments:
        # add all comments in allComments to commentLst in dictionary form
        commentLst.append({'comment': comment,
                            'lvl': lvl, })
        # make a recursive call to find more subcomments on comments
        commentLst += (traverseComments(comment.id, lvl+1))

    return commentLst

def thread(request, pId):
    """
    Purpose: This is the view in which a user can examine a single post and all the comments
    associated with that top level post. Also, let the user post comments.
    Parameters: request (django parameter) and pId (the post Id of the top level post)
    Returns: A render call that is passed the thread.html template, the top level post,
    and a master list of all the comments from traverseComments.
    """

    # make sure user is logged-in
    if request.user.is_authenticated != True:
        return redirect('/posts/')

    # get the top level post
    post = Post.objects.get(pk = pId)

    # if post method called
    if request.method == 'POST':

        if 'pId' in request.POST:
            # user is commenting direclty onto post (top level comment)
            parent = Post.objects.get(pk = request.POST['pId'])
        else:
            # user is commenting onto another comment
            parent = post

        # create new comment using the information provided by user
        newComment = Post( title = "comment",
                      body = request.POST['text'],
                      date = datetime.datetime.today(),
                      #date = request.POST['date'],
                      parent = parent,
                      userPosted = request.user,
                      likes = 0)
        newComment.save()

        # reload the page so if the user refreshes the page a new comment is not added to the database twice
        return redirect('/posts/thread/' + str(pId))

    # get master list of all comments
    commentLst = traverseComments(pId, 1) # the 1 stands for the subcomment lvl starting at 1 - because 1 comment deep (thought 1 made more sense than 0)

    # get user so the go-to-profile button can be generated in view
    currentUser = request.user

    return render(request, 'posts/thread.html', {'name': 'thread', 'pId': pId, 'pst': post, 'commentLst': commentLst, 'currentUser': currentUser})

#------------------------------------------------------------------------------#

def profile(request, profileId):
    """
    Purpose: This view acts as the profile home page for any user's profile. If
    the user is logged-in and viewing their profile, extra functionlity is unlocked,
    like being able to edit their bio.
    Parameters: request (django parameter) and profileId (so that the profile can
    be grabbed from the database)
    Returns: A render call that is passed the profile.html template, the profile being viewed,
    and all the top level posts posted by the user that corresponds to this profile.
    """
    # check user is logged-in
    if request.user.is_authenticated != True:
        return redirect('/posts/')

    # get the profile
    profile = Profile.objects.get(pk = profileId)
    # get all the top level posts for this profile
    allPosts = Post.objects.filter(userPosted=profile.user).filter(parent=None).order_by('-date')

    # if post method called
    if request.POST:
        if profile.user == request.user: # checked this is the profile of the logged in user
            profile.bio = request.POST['bio'] # update the user's bio

    # determine if the user is looking at their own profile or not (boolean)
    showEditButton = profile.user == request.user

    return render(request, 'posts/profile.html', {'name': 'profile', 'pId': profileId, 'profile': profile, 'allPosts': allPosts, 'showEditButton': showEditButton,})

#------------------------------------------------------------------------------#
