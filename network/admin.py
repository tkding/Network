from django.contrib import admin

# Register your models here.
from .models import User, Post, UserProfile, Like

admin.site.register(User)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Like)