from django.shortcuts import render
from django.views import generic
from collect.models import Post
from django.utils import timezone

import datetime

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'analyze/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """ Return posts that have been processed """
        return Post.objects.filter(
                processed__exact = True,
                created_at__gte = timezone.now() + datetime.timedelta(days = -60)
                ).order_by('-created_at')

# Create your models here.
def analyze_posts(request):
    return

def predict_post(request, post_id):
    return

