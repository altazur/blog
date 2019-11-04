from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.contrib import messages
# Create your views here.

class HomeView(generic.ListView):
    template_name = 'blogapp/home.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]

def post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method=='POST':
        input_text = request.POST.get('input_text')
        if input_text != "":
            comment = post.comment_set.create(text=input_text, pub_date=timezone.now(), user=request.user)
            comment.save()
            return HttpResponseRedirect('') 
        else:
            messages.add_message(request, messages.WARNING, "Empty comment can't be added")
            return render(request, 'blogapp/post.html', {'post':post})
    else:
        return render(request, 'blogapp/post.html', {'post':post})

def create_post(request):
    if request.method=='POST':
        selected_text = request.POST.get('input_text') 
        tags = request.POST.get('tags', "").split(',') 
        if selected_text != "" and tags != "":
            try:
                new_post = Post.objects.create(text=selected_text, pub_date=timezone.now(), likes_amount=0, dislikes_amount=0, tag=tags, user=request.user)
            except IntegrityError:
                return render(request, 'blogapp/createpost.html', {'error_message':"Post can't be empty"}) 
            except (ValueError, User.DoesNotExist):
                messages.add_message(request, messages.ERROR, "You must be logged in in order to write\comment posts")
                return HttpResponseRedirect(reverse('home'))
            else:
                new_post.save()
                return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'blogapp/createpost.html', {'error_message':"Post can't be empty"}) 
    else:
        return render(request, 'blogapp/createpost.html') 

class Register(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'
