from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Post

from .mailers.lead_mailer import LeadMailer

import datetime, json, os

class IndexView(generic.ListView):
    template_name = 'collect/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        """ Return posts that haven't been processed. """
        return Post.objects.filter(
                processed__exact = False,
                created_at__gte = timezone.now() + datetime.timedelta(days = -60)
                ).order_by('-created_at')

@csrf_exempt
def create_post(request):
    token = request.POST.get('token', '')
    if token == os.getenv('COLLECT_AND_ANALYZE_API_TOKEN'):
        attrs = {
            'title': request.POST['title'],
            'description': request.POST['description'],
            'link': request.POST['link'],
            'email': request.POST['email'],
            'phone_number': request.POST.get('phone_number', ''),
            'cl_id': Post.get_cl_id(request.POST['link'])
        }

        return JsonResponse(model_to_dict(Post.objects.create(**attrs)))
    else:
        return JsonResponse({ 'error': 'invalid api token.' })

def send_mail(request):
    post_id = request.POST['post_id']

    attrs = {
        'subject': request.POST['subject'],
        'body': request.POST['body'],
        'recipient': request.POST['recipient']
    }

    if LeadMailer.send_mail(**attrs) != 1:
        # TODO: log to errror
        return
    else:
        return


