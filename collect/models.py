from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

import datetime

# Create your models here.
class Post(models.Model):
    title = models.TextField(blank = False)
    description = models.TextField(blank = False)
    link = models.CharField(max_length = 200, blank = False)
    email = models.EmailField(max_length = 70, blank = False, default = '')
    phone_number = models.CharField(max_length = 20, blank = True)
    cl_id = models.CharField(max_length = 200, blank = False)
    passes = models.BooleanField(default = False)
    processed = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_recent_posts(**kwargs):
        processed = kwargs.pop('processed')
        return Post.objects.filter(
                processed__exact = processed,
                created_at__gte = timezone.now() + datetime.timedelta(days = -60)
                ).order_by('-created_at')

    @staticmethod
    def get_recent_processed_posts():
        return Post.get_recent_posts(processed = True)

    @staticmethod
    def get_recent_unprocessed_posts():
        return Post.get_recent_posts(processed = False)

    @staticmethod
    def get_processed_posts():
        return Post.objects.filter(processed__exact = True)

    # TODO: refactor this into a separate module
    @staticmethod
    def get_cl_id(link):
        return link.split('.html')[0].split('/')[-1]

