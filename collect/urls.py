from django.conf.urls import url
from . import views

app_name = 'collect'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^create_post$', views.create_post, name = 'create_post'),
    url(r'^process_post/(?P<post_id>[0-9]+)$', views.process_post, name = 'process_post')
]
