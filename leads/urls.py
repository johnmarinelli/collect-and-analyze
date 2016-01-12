from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    url(r'^collect/', include('collect.urls')),
    url(r'^analyze/', include('analyze.urls')),
    url(r'^admin/', admin.site.urls),
]
