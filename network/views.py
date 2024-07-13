from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    allPosts = Post.objects.all().order_by("id").reverse()
    paginator = Paginator(allPosts, 10)
    allPosts = paginator.get_page(request.GET.get('page'))


    return render(request, "network/index.html",{
        "allPosts": allPosts,
    })
def following(request):
    return
def profile_page(request,user_id):
    author = User.objects.get(pk=user_id)
    myPosts = Post.objects.filter(author=user_id).order_by("id").reverse()
    following = Follow.objects.filter(user=author)
    followers = Follow.objects.filter(user_follow=author)
    
    
    paginator = Paginator(myPosts, 1)
    myPosts = paginator.get_page(request.GET.get('page'))

    try:
        checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) !=0:
            isFollow = True
        else:
            isFollow = False
    except:
        isFollow = False

    return render(request, "network/profile.html",{
        "myPosts": myPosts,
        "username": author.username,
        "following": following,
        "followers": followers,	
        "isFollow": isFollow,
        "user_profile": author
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, author=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    

def follow(request):
    user= request.POST.get('userfollow')
    current_user = User.objects.get(pk=request.user.id)
    userFollowData=User.objects.get(username=user)
    f= Follow(user=current_user, user_follow=userFollowData)
    f.save()
    return HttpResponseRedirect(reverse("profile", kwargs={"user_id": userFollowData.id}))

def unfollow(request):
    user= request.POST.get('userfollow')
    current_user = User.objects.get(pk=request.user.id)
    userFollowData=User.objects.get(username=user)
    f= Follow.objects.get(user=current_user, user_follow=userFollowData)
    f.delete()
    return HttpResponseRedirect(reverse("profile", kwargs={"user_id": userFollowData.id}))