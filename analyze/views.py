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
    """
    Index for analyze will serve as a metrics viewer
    """
    template_name = 'analyze/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return PostMetrics().get_metrics()

def analyze_posts(request):
    return

def predict_post(request, post_id):
    post_predictor = PostPredictor(saved_pickle_path = 'prod')
    post_predictor.predict([Post.objects.get(pk = post_id)])
    return

