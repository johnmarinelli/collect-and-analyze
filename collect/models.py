from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.TextField(blank = False)
    description = models.TextField(blank = False)
    passes = models.BooleanField(default = False)
    link = models.CharField(max_length = 200, blank = False)
    cl_id = models.CharField(max_length = 200, blank = False)
    phone_number = models.CharField(max_length = 20, blank = True)
    processed = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
