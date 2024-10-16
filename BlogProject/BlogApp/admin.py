from django.contrib import admin
from .models import Profile, Post
from django.db import models
from django.contrib.auth.models import User


# Customizing Post model in the Django admin panel
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'created_date']
    list_filter = ['author', 'created_date']
    search_fields = ['title']
    ordering = ['-created_date']
    list_per_page = 5

# Registering the models in admin
admin.site.register(Profile)
admin.site.register(Post, PostAdmin)