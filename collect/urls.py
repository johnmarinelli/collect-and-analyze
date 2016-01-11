from django.conf.urls import url
from . import views

app_name = 'collect'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^create_post$', views.create_post, name = 'create_post')
]
