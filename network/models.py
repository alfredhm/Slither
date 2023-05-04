from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

class User(AbstractUser):
    pfp = models.ImageField(null=True, blank=True, upload_to="images/")
    name = models.CharField(max_length=50, default="", null=True, blank=True)
    bio = models.CharField(max_length=150, default="", null=True, blank=True)
    location = models.CharField(max_length=30, default="", null=True, blank=True)
    website = models.CharField(max_length=100, default="", null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "bio": self.bio,
            "location": self.location,
            "website": self.website,
        }
    def __str__(self):
        return f"{self.username}"

class Follow(models.Model):
    user = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE, blank=True, null=True)
    followed_user = models.ForeignKey(User, related_name="followed", on_delete=models.CASCADE, blank=True, null=True)

    def serialize(self):
        return {
            "user": self.user,
            "followed_user": self.followed_user,
        }

    def __str__(self):
        return f"{self.user} follows {self.followed_user}"

class Post(models.Model):
    body = models.CharField(max_length=250)
    like_users = models.ManyToManyField("User", related_name="liked_posts", blank=True)
    likes_count = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    edited = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.email,
            "body": self.body,
            "likes_count": self.likes_count,
            "like_users": [user.email for user in self.like_users.all()],
            "date_posted": self.date_posted
        }

    def __str__(self):
        return f"{self.body} posted by {self.poster}"
