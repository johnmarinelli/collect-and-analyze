from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('collect.urls')),
    url(r'^admin/', admin.site.urls),
]
