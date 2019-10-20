from django.shortcuts import render
from .models import User, Post, Comment
from django.db.models import F
from django.views import generic
from django.utils import timezone
# Create your views here.

class HomeView(generic.ListView):
    template_name = 'blogapp/home.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]

class PostView(generic.DetailView):
    model = Post
    template_name = 'blogapp/post.html'

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
