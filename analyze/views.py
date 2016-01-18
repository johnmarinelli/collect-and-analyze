from django.shortcuts import render
from django.views import generic
from collect.models import Post
from django.utils import timezone
from .lead_analyzer.analyzer import PostAnalyzer
from .lead_analyzer.predictor import PostPredictor
from .lead_analyzer.metrics import PostMetrics

import datetime

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'analyze/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """ Return posts that have been processed """
        return Post.get_recent_processed_posts()

def analyze_posts(request):
    return

def predict_post(request, post_id):
    return

