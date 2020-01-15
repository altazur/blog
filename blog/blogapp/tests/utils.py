from blogapp.models import Post, Comment
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Utils function for testing the blogapp

def create_user(name="Test", password="test"):
    """Create user with given name. 'Test' is the default one"""
    user = User.objects.create(username=name)
    user.set_password(password)
    user.save()
    return user

def create_post(post_text, days, user, tags):
    """Create post with given text, date and tags for user
    Negative days stands for past from now
    Positive dats is the future from now question"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(text=post_text, user=user, tag=tags, pub_date=time)

def create_comment(comment_text, post, days, user):
    """Create comment with given text for given post and with given date by given user
    Negative days stands for past from now comments
    Positive days is future from now"""
    time = timezone.now() + datetime.timedelta(days=days)
    return post.comment_set.create(text=comment_text, post=post, pub_date=time, user=user)
