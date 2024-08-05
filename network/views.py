from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from .models import User, Post, Follow, Liked



def remove_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Liked.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"message": "Like removed!"})


def add_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Liked.objects.filter(user=user, post=post)
    if like.exists():
       like.delete()
    else:
        newLike = Liked(user=user, post=post)
        newLike.save()
        return JsonResponse({"message": "Like adicionado!"})

                        
def index(request):
    allPosts = Post.objects.all().order_by("id").reverse()
    paginator = Paginator(allPosts, 10)
    allPosts = paginator.get_page(request.GET.get('page'))

    allLikes = Liked.objects.all()

    whoYouLiked = []
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked = []

    return render(request, "network/index.html",{
        "allPosts": allPosts,
        "whoYouLiked":whoYouLiked
    })
def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    followingP = Follow.objects.filter(user=currentUser)
    allPosts = Post.objects.all().order_by('id').reverse()
    
    following_posts=[]
    for post in allPosts:
        for follow in followingP:
            if follow.user_follow == post.author:
                following_posts.append(post)

    paginator = Paginator(following_posts, 10)
    following_posts = paginator.get_page(request.GET.get('page'))


    return render(request, "network/following.html",{
        "allPosts": following_posts,
    })

def edit_post(request, post_id):
    if request.method == 'POST':
        data= json.loads(request.body)
        edit = Post.objects.get(pk= post_id)
        edit.content = data["content"]
        edit.save()
        return JsonResponse({"message":"Change succesful", "data": data["content"]})

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