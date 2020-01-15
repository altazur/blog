from django.test import TestCase
import datetime
from blogapp.models import Post, Comment
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your tests here.
# Utils methods
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

def prepare_quick_post():
    """Quick post function"""
    return create_post("TestLikesPost", -2, create_user(name="QuickPostUser", password="test"), tags=[])

def prepare_quick_comment():
    """Quick comment function"""
    return create_comment("TestLikesComment", prepare_quick_post(), -2, create_user(name="QuickCommentUser", password="test"))

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
        self.assertEqual(response.status_code, 200)
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
        for i in range(0,12):
            post = create_post("Post"+str(i), -i, user, ['test', 'test'])
            post_ids[i] = post.id
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        #Post objects are always +1 because there is some default "Post" even on empty page
        self.assertContains(response, "Post", count=11)
        self.assertQuerysetEqual(response.context['latest_post_list'], ['<Post: '+str(post_ids[0])+'>','<Post: '+str(post_ids[1])+'>','<Post: '+str(post_ids[2])+'>','<Post: '+str(post_ids[3])+'>','<Post: '+str(post_ids[4])+'>','<Post: '+str(post_ids[5])+'>','<Post: '+str(post_ids[6])+'>','<Post: '+str(post_ids[7])+'>','<Post: '+str(post_ids[8])+'>','<Post: '+str(post_ids[9])+'>'])

    def test_tags(self):
        """Test that tags are presents on the page"""
        create_post("Test", -2, create_user(), tags=['testtag',])
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testtag")

class PostViewTest(TestCase):

    def test_no_comments(self):
        """If there is no comments only post text should be seen"""
        post_id = create_post("Post", -1, create_user(), tags=[]).id
        response = self.client.get(reverse('post', args=(post_id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post")
        self.assertEqual(str(response.context['post']), str(post_id)) 

    def test_logged_out_user_comment_warning(self):
        """Test that logged out user doesn't see the comment form and see the message 'Please login to write comment'"""
        test_user = create_user()
        post = create_post("Post", -2, test_user, tags=[]) 
        response = self.client.get(f"/{post.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<form method='post'>")
        self.assertContains(response, "Please login to write comments")

    def test_empty_comment(self):
        """Empty comment can't be send and warning is displayed"""
        test_user = create_user("test", "Qwerty123")
        post = create_post("Post", -2, test_user, tags=[]) 
        self.client.login(username="test", password="Qwerty123")
        response = self.client.post(f"/{post.id}/", {"input_text":""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Empty comment can&#39;t be added")
 
    def test_future_comment(self):
        """If comment is in the future it should'nt be seen"""
        test_user = create_user()
        post = create_post("Post", -2, test_user, tags=[]) 
        future_comment = create_comment("Test comment", post, 2, test_user)
        response = self.client.get(reverse('post', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post")
        self.assertNotContains(response, "Test comment")

    def test_past_comment(self):
        """If comment is in the past it should be seen"""
        test_user = create_user()
        post = create_post("Post", -2, test_user, tags=[]) 
        past_comment = create_comment("Test comment", post, -1, test_user)
        response = self.client.get(reverse('post', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post")
        self.assertContains(response, "Test comment")

    def test_hundred_comments(self):
        """Write 100 comments. All should be displayed"""
        test_user = create_user()
        post = create_post("Post", -2, test_user, tags=[])
        for i in range(100):
            create_comment("Test comment", post, -i, test_user)
        response = self.client.get(reverse('post', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test comment", count=100)

class CreatePostView(TestCase):
    
    def test_create_post(self):
        """Login and write post through POST. Post should be visible on the home page. After POST user is redirected to home page"""
        create_user("test", "Qwerty123")
        self.client.login(username="test", password="Qwerty123")
        response = self.client.post("/createpost/", {'input_text':'TestPost', 'tags':['tag1','tag2']})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'You must be logged in in order to write\\comment posts') 
        self.assertContains(response, "TestPost")

    def test_create_empty_post(self):
        """Login and write an empty post. Error message is shown"""
        response = self.client.post('/createpost/', {'input_text':'', 'tags':[]})
        self.assertEqual(response.status_code, 200)
        #Unicode symbol instead of "'"
        self.assertContains(response, "Post can&#39;t be empty")

    def test_create_post_logged_out(self):
        """Do not login and trying to create a post. Error message is shown. Post isn't created"""
        response = self.client.post('/createpost/', {'input_text':'TestPost', 'tags':['tag1','tag2']})
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/")
        self.assertContains(response, "You must be logged in in order to write\\comment posts")
        self.assertNotContains(response, "TestPost")

class LikesTest(TestCase):

    def test_add_likes_to_post(self):
        """Adding likes to post and assert quantity"""
        post = prepare_quick_post()
        post.likes_add(post.id, 2)
        post.refresh_from_db()
        self.assertEqual(post.likes_amount, 2)

    def test_add_likes_to_comment(self):
        """Adding likes to comment and assert quantity"""
        comment = prepare_quick_comment()
        comment.likes_add(comment.id, 2)
        comment.refresh_from_db()
        self.assertEqual(comment.likes_amount, 2)

    def test_add_zero_likes_to_post(self):
        """Adding zero amount of likes. Assert that likes amount isn't changed"""
        """This test is pass even witn placeholder func"""
        post = prepare_quick_post()
        post.likes_amount = 5
        post.save()
        post_likes_before = post.likes_amount
        post.likes_add(post.id, 0)
        post.refresh_from_db()
        self.assertEqual(post.likes_amount, post_likes_before)

    def test_add_zero_likes_to_comment(self):
        """Adding zero likes to comment. Assert that likes amount isn't changed"""
        """This test is pass even witn placeholder func"""
        comment = prepare_quick_comment()
        comment.likes_before = 5
        comment_likes_before = comment.likes_amount
        comment.likes_add(comment.id, 0)
        comment.refresh_from_db()
        self.assertEqual(comment.likes_amount, comment_likes_before)

    def test_neg_likes_to_post(self):
        """Adding negative likes to post. Assert that likes are decreased"""
        """This test is pass even witn placeholder func"""
        post = prepare_quick_post()
        post_likes_before = post.likes_amount
        post.likes_add(post.id, -99)
        post.refresh_from_db()
        self.assertEqual(post.likes_amount, post_likes_before-99)

    def test_neg_likes_to_comment(self):
        """Adding negative likes to comment. Assert that likes are decreased"""
        """This test is pass even witn placeholder func"""
        comment = prepare_quick_comment()
        comment_likes_before = comment.likes_amount
        comment.likes_add(comment.id, -5)
        comment.refresh_from_db()
        self.assertEqual(comment.likes_amount, comment_likes_before-5)

    def test_big_likes_to_post(self):
        """Adding huge numbers of likes to post. Assert that likes amount is changed correctly"""
        post = prepare_quick_post()
        base_likes = 6
        post.likes_amount = base_likes 
        post.save()
        post.likes_add(post.id, 1000)
        post.refresh_from_db()
        self.assertEqual(post.likes_amount, base_likes+1000)

    def test_big_likes_to_comment(self):
        """Adding huge numbers of likes to comment. Assert that likes amount is changed correctly"""
        comment = prepare_quick_comment()
        base_likes = 25
        comment.likes_amount = base_likes
        comment.save()
        comment.likes_add(comment.id, 999)
        comment.refresh_from_db()
        self.assertEqual(comment.likes_amount, base_likes+999)

    def test_post_likes_view(self):
        """Assert that page contains right amount of likes after post.likes_add()"""
        post = prepare_quick_post()
        post.likes_add(post.id, 256)
        post.refresh_from_db()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "256")

    def test_comment_likes_view(self):
        """Assert that postview contains right amount of likes for comment"""
        #Using 'classic' way to prepare comment in order to obtain post.id
        post = prepare_quick_post()
        comment = create_comment("TestComment", post, -2, create_user())
        comment.likes_add(comment.id, 999)
        comment.refresh_from_db()
        response = self.client.get(f"/{post.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "999")

class DislikesTest(TestCase):

    def test_add_dislikes_to_post(self):
        """Adding dislikes to post and assert quantity"""
        post = prepare_quick_post()
        post.dislikes_add(post.id, 2)
        post.refresh_from_db()
        self.assertEqual(post.dislikes_amount, 2)

    def test_add_dislikes_to_comment(self):
        """Adding dislikes to comment and assert quantity"""
        comment = prepare_quick_comment()
        comment.dislikes_add(comment.id, 2)
        comment.refresh_from_db()
        self.assertEqual(comment.dislikes_amount, 2)

    def test_add_zero_dislikes_to_post(self):
        """Adding zero amount of dislikes. Assert that likes amount isn't changed"""
        """This test is pass even witn placeholder func"""
        post = prepare_quick_post()
        post.dislikes_amount = 5
        post_dislikes_before = post.likes_amount
        post.dislikes_add(post.id, 0)
        post.refresh_from_db()
        self.assertEqual(post.dislikes_amount, post_dislikes_before)

    def test_add_zero_dislikes_to_comment(self):
        """Adding zero dislikes to comment. Assert that likes amount isn't changed"""
        """This test is pass even witn placeholder func"""
        comment = prepare_quick_comment()
        comment.dislikes_amount = 6
        comment_dislikes_before = comment.likes_amount
        comment.dislikes_add(comment.id, 0)
        comment.refresh_from_db()
        self.assertEqual(comment.dislikes_amount, comment_dislikes_before)

    def test_neg_dislikes_to_post(self):
        """Adding negative dislikes to post. Assert that likes are decreased"""
        post = prepare_quick_post()
        post_dislikes_before = post.likes_amount
        post.dislikes_add(post.id, -99)
        post.refresh_from_db()
        self.assertEqual(post.dislikes_amount, post_dislikes_before-99)

    def test_neg_dislikes_to_comment(self):
        """Adding negative dislikes to comment. Assert that likes are decreased"""
        comment = prepare_quick_comment()
        comment_dislikes_before = comment.likes_amount
        comment.dislikes_add(comment.id, -5)
        comment.refresh_from_db()
        self.assertEqual(comment.dislikes_amount, comment_dislikes_before-5)

    def test_big_dislikes_to_post(self):
        """Adding huge numbers of dislikes to post. Assert that likes amount is changed correctly"""
        post = prepare_quick_post()
        base_dislikes = 6
        post.dislikes_amount = base_dislikes 
        post.save()
        post.dislikes_add(post.id, 1000)
        post.refresh_from_db()
        self.assertEqual(post.dislikes_amount, base_dislikes+1000)

    def test_big_dislikes_to_comment(self):
        """Adding huge numbers of dislikes to comment. Assert that likes amount is changed correctly"""
        comment = prepare_quick_comment()
        base_dislikes = 25
        comment.dislikes_amount = base_dislikes
        comment.save()
        comment.dislikes_add(comment.id, 999)
        comment.refresh_from_db()
        self.assertEqual(comment.dislikes_amount, base_dislikes+999)

    def test_post_dislikes_view(self):
        """Assert that page contains right amount of dislikes after post.likes_add()"""
        post = prepare_quick_post()
        post.dislikes_add(post.id, 256)
        post.refresh_from_db()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "256")

    def test_comment_dislikes_view(self):
        """Assert that postview contains right amount of dislikes for comment"""
        #Using 'classic' way to prepare comment in order to obtain post.id
        post = prepare_quick_post()
        comment = create_comment("TestComment", post, -2, create_user())
        comment.dislikes_add(comment.id, 999)
        comment.refresh_from_db()
        response = self.client.get(f"/{post.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "999")
