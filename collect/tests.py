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
    def test_index_view_with_no_posts(self):
        """
        If no posts exist, an appropriate message should be displayed.
        """
        res = self.client.get(reverse('collect:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'No posts available.')
        self.assertQuerysetEqual(res.context['posts_list'], [])

    def test_index_view_with_old_post(self):
        """
        A post that is over two months old should not be displayed.
        """
        post = create_random_post()
        post.created_at = timezone.now() + datetime.timedelta(days = -65)
        post.save()
        res = self.client.get(reverse('collect:index'))
        self.assertContains(res, 'No posts available.')
        self.assertQuerysetEqual(res.context['posts_list'], [])

    def test_index_view_with_single_post(self):
        """
        If a post exists, it should be displayed.
        """
        post = create_random_post()
        res = self.client.get(reverse('collect:index'))
        self.assertContains(res, post.title)
        self.assertQuerysetEqual(res.context['posts_list'], [repr(post)])

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
        self.assertQuerysetEqual(res.context['posts_list'], [repr(post1)])

    def test_create_post_with_valid_input(self):
        """
        Valid input should create a post.
        """
        old_post_count = len(Post.objects.all())
        attrs = create_random_attributes()
        attrs['token'] = os.getenv('COLLECT_AND_ANALYZE_API_TOKEN', '')
        res = self.client.post('/collect/create_post', attrs)
        self.assertEqual(len(Post.objects.all()), old_post_count + 1)

class LeadMailerTest(TestCase):
    def sends_mail_with_valid_parameters(self):
        """
        Sends an email containing an expression of interest given proper params.
        """
        LeadMailer.send_mail('subj', 'body', 'test@email.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'subj')
        self.assertEqual(mail.outbox[0].body, 'body')
