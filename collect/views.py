from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .models import Post

class IndexView(generic.ListView):
    template_name = 'collect/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """ Return posts that haven't been processed. """
        return Post.objects.filter(
                processed__exact = False
                ).order_by('-created_at')
