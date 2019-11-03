from django.test import TestCase
import datetime
from .models import Post, Comment
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your tests here.
# Utils methods
def create_user(name="Test"):
    """Create user with given name. 'Test' is the default one"""
    return User.objects.create(username=name)

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
    post.comment_set.create(text=comment_text, post=post, pub_date=time, user=user)

class HomePageTests(TestCase):
    
    def test_no_posts(self):
        """If there is no posts 'There is no posts' should be displayed"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no posts")
        self.assertQuerysetEqual(response.context['latest_post_list'],[])

    def test_future_post(self):
        """Login and create a post with future time. It should'nt be visible"""
        create_post("FuturePost", 2, create_user(), tags=['test', 'test'])
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "There is no posts")
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_past_post(self):
        """Login and create normal post with past date. It should be visible"""
        post_id=create_post("PastPost", -2, create_user(), ['test', 'test']).id
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PastPost")
        self.assertQuerysetEqual(response.context['latest_post_list'], ['<Post: '+str(post_id)+'>']) 

    def test_twelve_posts(self):
        """Login and write 12 posts. 10 of them should be displayed"""
        post_ids = [0]*12
        user = create_user()
        for i in range(0,11):
            post = create_post("Post"+str(i), -1, user, ['test', 'test'])
            post_ids[i] = post.id
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        #TODO: somehow test founds the 11 Posts on the page. Maybe a bug
        self.assertContains(response, "Post", count=10)
        #TODOL as expected this assert is shit. Fails everytime. IDK why
        self.assertQuerysetEqual(response.context['latest_post_list'], ['<Post: '+str(post_ids[0])+'>','<Post: '+str(post_ids[1])+'>','<Post: '+str(post_ids[2])+'>','<Post: '+str(post_ids[3])+'>','<Post: '+str(post_ids[4])+'>','<Post: '+str(post_ids[5])+'>','<Post: '+str(post_ids[6])+'>','<Post: '+str(post_ids[7])+'>','<Post: '+str(post_ids[8])+'>','<Post: '+str(post_ids[9])+'>'])

    def test_tags(self):
        """Test that tags are presents on the page"""
        create_post("Test", -2, create_user(), tags=['testtag',])
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testtag")
