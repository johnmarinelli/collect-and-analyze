from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from .models import Post
from .mailers.lead_mailer import LeadMailer

import string, random, datetime, os

def random_string(length, ascii_set = string.ascii_uppercase):
    return ''.join(random.choice(ascii_set) for _ in range(length))

def random_numerical_string(length):
    return random_string(length, ascii_set = string.digits)

def create_random_attributes():
    return {
        'title': random_string(5),
        'description': random_string(20),
        'link': "/%s/%s.html" % (random_string(5), random_numerical_string(10)),
        'email': "%s@%s.com" % (random_string(5), random_string(7)),
        'phone_number': random_numerical_string(9)
    }


def create_random_post():
    attrs = create_random_attributes()
    return Post.objects.create(**attrs)

class PostViewTests(TestCase):
    def assert_no_queries(self, res):
        self.assertContains(res, 'No posts available.')
        self.assertQuerysetEqual(res.context['posts_list'], [])

    def test_index_view_with_no_posts(self):
        """
        If no posts exist, an appropriate message should be displayed.
        """
        res = self.client.get(reverse('collect:index'))
        self.assertEqual(res.status_code, 200)
        self.assert_no_queries(res)

    def test_index_view_with_old_post(self):
        """
        A post that is over two months old should not be displayed.
        """
        post = create_random_post()
        post.created_at = timezone.now() + datetime.timedelta(days = -65)
        post.save()
        res = self.client.get(reverse('collect:index'))
        self.assert_no_queries(res)

    def test_index_view_with_single_post(self):
        """
        If a post exists, it should be displayed.
        """
        post = create_random_post()
        res = self.client.get(reverse('collect:index'))
        self.assertContains(res, post.title)
        self.assertEqual(res.context['posts_list'][0]['title'], post.title)

    def test_index_view_with_recent_post_and_old_post(self):
        """
        Only display recent posts.
        """
        post1 = create_random_post()
        post2 = create_random_post()
        post2.created_at = timezone.now() + datetime.timedelta(days = -65)
        post2.save()
        res = self.client.get(reverse('collect:index'))
        self.assertContains(res, post1.title)
        self.assertEqual(res.context['posts_list'][0]['title'], post1.title)

    def test_index_view_with_processed_post(self):
        """
        Processed posts should not be displayed.
        """
        post = create_random_post()
        post.processed = True
        post.save()
        res = self.client.get(reverse('collect:index'))
        self.assert_no_queries(res)


class CreatePostTest(TestCase):
    def test_create_post_with_valid_input(self):
        """
        Valid input should create a post.
        """
        old_post_count = len(Post.objects.all())
        attrs = create_random_attributes()
        attrs['token'] = os.getenv('COLLECT_AND_ANALYZE_API_TOKEN', '')
        res = self.client.post('/collect/create_post', attrs)
        self.assertEqual(len(Post.objects.all()), old_post_count + 1)

class ProcessPostTest(TestCase):
    def setUp(self):
        self.post = create_random_post()
        self.post_id = self.post.id
        self.process_post_url = reverse('collect:process_post', kwargs = { 'post_id': self.post_id })

    def tearDown(self):
        Post.objects.all().delete()

    def get_result(self,valid):
        return self.client.post('%s?valid=%s' % (self.process_post_url, str(valid)))

    def test_process_uninteresting_post(self):
        """
        Make sure uninteresting posts don't get passed, but are processed.
        """
        res = self.get_result(0)
        self.assertEqual(Post.objects.get(pk = self.post_id).passes, False)
        self.assertEqual(Post.objects.get(pk = self.post_id).processed, True)
    
    def test_process_interesting_post(self):
        """
        Make sure interesting posts get passed.
        """
        res = self.get_result(1)
        self.assertEqual(Post.objects.get(pk = self.post_id).passes, True)
        self.assertEqual(Post.objects.get(pk = self.post_id).processed, True)

class LeadMailerTest(TestCase):
    def sends_mail_with_valid_parameters(self):
        """
        Sends an email containing an expression of interest given proper params.
        """
        LeadMailer.send_mail('subj', 'body', 'test@email.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'subj')
        self.assertEqual(mail.outbox[0].body, 'body')
        self.assertItemsEqual(mail.outbox[0].recipients(), ['test@email.com', 'john@johnmarinelli.me'])

class PostModelTest(TestCase):
    def test_get_recent_unprocessed_posts_with_one_recent_unprocessed_post(self):
        """
        Retrieve all unprocessed posts within last 2 months.
        """
        post1 = create_random_post()
        posts = Post.get_recent_unprocessed_posts()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts.first().title, post1.title)

    def test_get_recent_unprocessed_posts_with_varying_posts(self):
        """
        Retrieve all unprocessed posts within last 2 months,
        given some posts don't meet criteria.
        """
        post1 = create_random_post()
        post2 = create_random_post()
        post2.created_at = timezone.now() + datetime.timedelta(days = -65)
        post2.save()
        posts = Post.get_recent_unprocessed_posts()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts.first().title, post1.title)

    def test_get_recent_processed_posts_with_one_recent_unprocessed_post(self):
        """
        Retrieve all unprocessed posts within last 2 months.
        """
        post1 = create_random_post()
        post1.processed = True
        post1.save()
        posts = Post.get_recent_processed_posts()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts.first().title, post1.title)

    def test_get_recent_processed_posts_with_varying_posts(self):
        """
        Retrieve all unprocessed posts within last 2 months,
        given some posts don't meet criteria.
        """
        post1 = create_random_post()
        post1.processed = True
        post1.save()
        post2 = create_random_post()
        post2.processed = True
        post2.created_at = timezone.now() + datetime.timedelta(days = -65)
        post2.save()
        posts = Post.get_recent_processed_posts()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts.first().title, post1.title)

