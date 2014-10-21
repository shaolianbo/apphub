from django.conf.urls import patterns, url

from .views import crawl


urlpatterns = patterns(
    '',
    url(r'^crawl', crawl, name='crawl')
)
