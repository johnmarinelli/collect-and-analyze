from __future__ import unicode_literals

from django.db import models

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
