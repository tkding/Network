
from django.urls import path

from . import views

urlpatterns = [
    # index == all posts
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="new_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following_posts, name="following_posts"),
    path("check_follow/<int:user_id>", views.check_follow, name="check_follow"),
    path("toggle_follow/<int:user_id>", views.toggle_follow, name="toggle_follow"),   
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"), 
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
]

