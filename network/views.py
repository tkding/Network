from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
import traceback
import json
from django.contrib import messages

from .models import User, Post, UserProfile, Like


def index(request):
    # Fetch all posts from the database, sorted by timestamp in reverse order
    posts = Post.objects.all().order_by("-timestamp")

    # Paginate the posts (show 10 posts per page)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "title": "All Posts",
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


@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Post.objects.create(user=user, content=content)
        # new stuff for new post msg
        messages.success(request, 'Post created successfully.')
        return redirect('index') # redirect to index page
    
        # return HttpResponseRedirect(reverse("index"), {
        #     "message": "Post created successfully."
        # })
    else:
        return render(request, "network/new_post.html")


def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=profile_user)
    followers_count = user_profile.followers.count()
    following_count = profile_user.following.count()
    posts = Post.objects.filter(user=profile_user).order_by("-timestamp")
    
    # Paginate the posts (show 10 posts per page)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    is_following = False
    if request.user != profile_user:
        is_following = request.user in user_profile.followers.all()

    
    context = {
        'profile_user': profile_user,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts': page_obj, # pass the paginated posts
        'is_following': is_following
    }
    
    return render(request, 'network/profile.html', context)

@login_required
@require_http_methods(["GET"])
def check_follow(request, user_id):
    try: 
        profile_user = get_object_or_404(User, pk=user_id)
        user_profile, _ = UserProfile.objects.get_or_create(user=profile_user)
        is_following = request.user in user_profile.followers.all()
        return JsonResponse({"success": True, "is_following": is_following}, status=200)
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return JsonResponse({"success": False}, status=400)
    
@login_required
@require_http_methods(["PUT"])
def toggle_follow(request, user_id):
    try: 
        profile_user = get_object_or_404(User, pk=user_id)
        user_profile, _ = UserProfile.objects.get_or_create(user=profile_user)

        profile_user_request = get_object_or_404(User, pk=request.user.id)
        user_profile_request, _ = UserProfile.objects.get_or_create(user=profile_user_request)
        
        if request.user in user_profile.followers.all():
            user_profile.followers.remove(request.user)
            user_profile_request.following.remove(profile_user)
            is_following = False
        else:
            user_profile.followers.add(request.user)
            user_profile_request.following.add(profile_user)
            is_following = True
        
        followers_count = user_profile.followers.count()  # Update the followers count
         
        return JsonResponse({"success": True, "is_following": is_following, "followers_count": followers_count}, status=200)
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return JsonResponse({"success": False}, status=400)
    #return JsonResponse({"success": False}, status=400)
        
@login_required
def following_posts(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Get users followed by the current user using the UserProfile model
    following_users = user_profile.following.all()
    
    # Get posts made by users that the current user follows
    following_posts = Post.objects.filter(user__in=following_users).order_by("-timestamp")

    
    # Paginate the following posts (show 10 posts per page)
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "title": "Following Posts",
    })

@login_required
@require_http_methods(["PUT"])
def edit_post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
        if request.user != post.user:
            return JsonResponse({"success": False}, status=403)
        data = json.loads(request.body)
        new_content = data.get("content")

        if new_content:
            post.content = new_content
            post.save()
            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"success": False, "message": "Invalid content."}, status=400)
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return JsonResponse({"success": False}, status=400)


@login_required
@require_http_methods(["PUT"])
def like_post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        liked = False
        
        if Like.objects.filter(user=user, post=post).exists():
            Like.objects.filter(user=user, post=post).delete()
            
        else:
            Like.objects.create(user=user, post=post)
            liked = True
        
        like_count = post.likes.count()
        return JsonResponse({"success": True, "liked": liked, "like_count": like_count}, status=200)
    
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return JsonResponse({"success": False}, status=400)