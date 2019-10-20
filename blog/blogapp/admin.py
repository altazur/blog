from django.contrib import admin
from .models import User, Post, Comment

# Register your models here.
admin.site.register(User)
#For test purposes only
admin.site.register(Post)
#For test purposed only
admin.site.register(Comment)
