from django.db import models
import datetime
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    text = models.TextField(max_length=512, blank=False)
    pub_date = models.DateTimeField('date published')
    likes_amount = models.IntegerField(default=0)
    dislikes_amount = models.IntegerField(default=0)
    tag = ArrayField(models.CharField(max_length=200), blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def was_published_recently(self):
        """Return true if the pub_date isn't more than 1 day"""
        return timezone.now()-datetime.timedelta(days=1) <= self.pub_date <= timezone.now() 
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

    def most_liked(self):
        """Returns true if the instance is the most likes_amountd post"""
        pass

    def likes_add(self, post_id, amount):
        """Function changes likes of given amount """
        pass

    def dislikes_add(self, post_id, amount):
        """Function change dislikes of given post with amount"""
        pass

class Comment(models.Model):
    text = models.TextField(max_length=256, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes_amount = models.IntegerField(default=0)
    dislikes_amount = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return str(self.id)

    def was_published_recently(self):
        """Return true if the pub_date isn't more than 1 day"""
        return timezone.now()-datetime.timedelta(days=1) <= self.pub_date <= timezone.now() 
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

    def most_liked(self):
        """Returns true if the instance is the most likes_amountd post"""
        pass

    def likes_add(self, comment_id, amount):
        """Function changes likes of given amount """
        pass

    def dislikes_add(self, post_id, amount):
        """Function change dislikes of given comment with amount"""
        pass
