from django.conf.urls import url
from . import views

app_name = 'analyze'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^analyze_posts$', views.analyze_posts, name = 'analyze_posts'),
    url(r'^(?P<post_id>[0-9]+)/predict$', views.predict_post, name = 'predict_post')
]
