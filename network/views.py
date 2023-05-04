import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import *
from .forms import *

def index(request):

    user = request.user
    follows = []

    if user.is_authenticated:
        follow_filter = Follow.objects.filter(user=user).values()
        for follow in follow_filter:
            follows.append(follow['followed_user_id'])


    posts = Post.objects.all().order_by('-date_posted')

    pages = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page = pages.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": posts,
        "page": page,
        "user": user,
        "follows": follows
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
        name = request.POST["name"]

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
            user.name = name
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required(login_url="auctions/login.html")
def post_hiss(request):
    # If method is post, post the hiss
    if request.method == "POST":

        # Get the current user
        poster = request.user

        if len(request.POST["body"]) < 1:
            posts = Post.objects.all().order_by('-date_posted')

            if len(posts) < 11:
                return render(request, "network/index.html", {
                    "posts": posts,
                    "onepage": True
                })

            pages = Paginator(posts, 10)

            page_number = request.GET.get('page')
            page = pages.get_page(page_number)

            return render(request, "network/index.html", {
                "posts": posts,
                "page": page,
                "alert": "Cannot post empty Hiss"
            })

        # Create the new post
        new_post = Post()
        new_post.poster = poster
        new_post.body = request.POST["body"]
        new_post.save()

        # Return user to home page whene the new hiss is
        return HttpResponseRedirect(reverse("index"))

    # If method is get, return index where the hiss form is
    return render(request, "network/index.html")


def users(request, username):

    user = request.user

    # Get the user that was clicked on
    try:
        profile = User.objects.get(username=username)
    except:
        return HttpResponse(status=400)

    # Get their posts
    profile_posts = Post.objects.filter(poster=profile).order_by('-date_posted')

    pages = Paginator(profile_posts, 10)

    page_number = request.GET.get('page')
    page = pages.get_page(page_number)

    # Get the follow info
    profile_following = Follow.objects.filter(user=profile)
    profile_followers = Follow.objects.filter(followed_user=profile)

    try:
        follows = Follow.objects.get(user=user, followed_user=profile)
        follows = True
    except:
        follows = False

    if request.method == "POST":

        if follows and user.is_authenticated :
            unfollow = Follow.objects.get(user=user, followed_user=profile)
            unfollow.delete()
            follows = False

        elif user.is_authenticated:
            new_follow = Follow(user=user, followed_user=profile)
            new_follow.save()
            follows = True
        else:
            return HttpResponseRedirect(f"/login")

        return HttpResponseRedirect(f"/users/{profile}")

    return render(request, "network/profile.html", {
        "profile": profile,
        "page": page,
        "form": ProfilePicForm(),
        "profile_following": profile_following,
        "profile_followers": profile_followers,
        "follows": follows,
        "posts": profile_posts,
        "user": user
    })

@login_required(login_url="auctions/login.html")
def following_posts(request):
    user = request.user

    followed = Follow.objects.filter(user=user)

    followed_users = []

    for follow in followed:
        followed_users.append(follow.followed_user)

    posts = []

    for profile in followed_users:
        profile_posts = Post.objects.filter(poster=profile)

        for post in profile_posts:
            posts.append(post)

    pages = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page = pages.get_page(page_number)

    return render(request, "network/index.html", {
        "page": page,
        "user": user
    })

@csrf_exempt
@login_required(login_url="auctions/login.html")
def like(request, postid):
    user = request.user

    try:
        post = Post.objects.get(id=postid)
    except:
        return JsonResponse({"error": "Hiss not found"}, status=404)

    if request.method == "GET":
        return JsonResponse([post.serialize()], safe=False)

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("user_liked") == False:
            post.like_users.add(user)
        elif data.get("user_liked") == True:
            post.like_users.remove(user)
        post.likes_count = post.like_users.count()
        post.save()
        return HttpResponse(status=204)

@csrf_exempt
@login_required(login_url="auctions/login.html")
def edit_info(request, username):
    try:
        profile = User.objects.get(username=username)
    except:
        return JsonResponse({"error": "User not found"}, status=404)

    if request.method == "GET":
        return JsonResponse([profile.serialize(), str(profile.pfp)], safe=False)
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("name") != "":
            profile.name = data.get("name")
        if data.get("bio") != "":
            profile.bio = data.get("bio")
        if data.get("location") != "":
            profile.location = data.get("location")
        if data.get("website") != "":
            profile.website = data.get("website")
        profile.save()
        return HttpResponse(status=204)
    elif request.method == "POST":
        if request.FILES:
            profile.pfp = request.FILES["profile-image"]
            profile.save()
        return HttpResponse(status=204)


@csrf_exempt
@login_required(login_url="auctions/login.html")
def follow_info(request, followed):
    user = request.user

    try:
        followed_user = User.objects.get(username=followed)
        followed_exists = True
    except:
        followed_exists = False

    if followed_exists:
        try:
            follow = Follow.objects.get(user=user, followed_user=followed_user)
            follows = True
        except:
            follows = False
    else:
        follows = False

    if request.method == "GET":
        if follows:
            return JsonResponse({"followed": followed_user.username, "follows": True})
        return JsonResponse({"followed": followed_user.username, "follows": False})
    elif request.method == "PUT":
        if (follows):
            unfollow = Follow.objects.get(user=user, followed_user=followed_user)
            unfollow.delete()
            return HttpResponse(status=204)
        else:
            new_follow = Follow(user=user, followed_user=followed_user)
            new_follow.save()
            return HttpResponse(status=204)
    return HttpResponse(status=404)


@csrf_exempt
@login_required(login_url="auctions/login.html")
def edit_post(request, postid):
    try:
        post = Post.objects.get(id=postid)
    except:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.method == "GET":
        return JsonResponse([post.serialize()], safe=False)
    elif request.method == "PUT":
        data = json.loads(request.body)
        new_body = str(data.get("new_body")).strip()
        if new_body != "" and new_body != post.body:
            post.body = new_body
            post.edited = True
            post.save()
        return HttpResponse(status=204)