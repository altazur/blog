from django.shortcuts import render
from .models import User, Post, Comment
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
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

def create_post(request):
    """In the future this view should receive user_id"""
    selected_text = request.POST.get('text', "")
    tags = request.POST.get('tags', "").split(',') 
    if selected_text is not "":
        new_post = Post.objects.create(text=selected_text, pub_date=timezone.now(), likes_amount=0, dislikes_amount=0, tag=tags, user=User.objects.get(pk=1))
        new_post.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, "blogapp/createpost.html", {'error_message':"You cannot write empty post"})
