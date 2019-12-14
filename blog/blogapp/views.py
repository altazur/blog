from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, PostLike, CommentLike, PostDislike, CommentDislike
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['post_likes'] = PostLike.objects.filter(user=self.request.user.id)
        context['post_dislikes'] = PostDislike.objects.filter(user=self.request.user.id)
        return context

def post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comment_set.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    # Receiveing all likes for current user 
    comment_likes = CommentLike.objects.filter(user=request.user.id)
    # Receiving all dislikes for current user
    comment_dislikes = CommentDislike.objects.filter(user=request.user.id)
    if request.method=='POST':
        input_text = request.POST.get('input_text')
        if input_text != "":
            comment = post.comment_set.create(text=input_text, pub_date=timezone.now(), user=request.user)
            comment.save()
            return HttpResponseRedirect('') 
        else:
            messages.add_message(request, messages.WARNING, "Empty comment can't be added")
            return render(request, 'blogapp/post.html', {'post':post, 'comments':comments, 'comment_likes': comment_likes, 'comment_dislikes': comment_dislikes})
    else:
        return render(request, 'blogapp/post.html', {'post':post, 'comments':comments, 'comment_likes':comment_likes, 'comment_dislikes':comment_dislikes})

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

@login_required
def like_post(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        user_id = request.user.id
    if post_id is not None:
        if PostLike.objects.filter(post=post_id, user=user_id):  # Check whether usr is already liked the post
            return
        post = Post.objects.get(pk=post_id)
        user = request.user
        post.likes_add(post.id, 1)
        post.refresh_from_db()
        PostLike.objects.create(post=post, user=user)
    return HttpResponse(post.likes_amount)

@login_required
def dislike_post(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        user_id = request.user.id
    if post_id is not None:
        if PostDislike.objects.filter(post=post_id, user=user_id):  # Check whether user is already dislike that post
            return
        post = Post.objects.get(pk=post_id)
        user = request.user
        post.dislikes_add(post.id, 1)
        post.refresh_from_db()
        PostDislike.objects.create(post=post, user=user)
    return HttpResponse(post.dislikes_amount)

@login_required
def like_comment(request):
    if request.method == 'GET':
        comment_id = request.GET['comment_id']
        user_id = request.user.id
    if comment_id is not None:
        if CommentLike.objects.filter(comment=comment_id, user=user_id):  # Check whether user is already liked the comment
            return
        comment = Comment.objects.get(pk=comment_id)
        user = request.user
        comment.likes_add(comment.id, 1)
        comment.refresh_from_db()
        CommentLike.objects.create(comment=comment, user=user)
    return HttpResponse(comment.likes_amount)

@login_required
def dislike_comment(request):
    if request.method == 'GET':
        comment_id = request.GET['comment_id']
        user_id = request.user.id
    if comment_id is not None:
        if CommentDislike.objects.filter(comment=comment_id, user=user_id):  # Chech whether user is already disliked the comment
            return
        comment = Comment.objects.get(pk=comment_id)
        user = request.user
        comment.dislikes_add(comment.id, 1)
        comment.refresh_from_db()
        CommentDislike.objects.create(comment=comment, user=user)
    return HttpResponse(comment.dislikes_amount)
