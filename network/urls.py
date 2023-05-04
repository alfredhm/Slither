from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/", views.post_hiss, name="hiss"),
    path("following", views.following_posts, name="following"),
    path("users/<str:username>", views.users, name="users"),

    # API Routes
    path("posts/<int:postid>", views.like, name="like_post"),
    path("profiles/<str:username>", views.edit_info, name="edit_info"),
    path("follow/<str:followed>", views.follow_info, name="follow_info"),
    path("edit/<int:postid>", views.edit_post, name="edit_post")

]
