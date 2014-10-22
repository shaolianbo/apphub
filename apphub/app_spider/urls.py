from django.conf.urls import patterns, url

from .views import crawl, change_continue


urlpatterns = patterns(
    '',
    url(r'^crawl', crawl, name='crawl'),
    url(r'^change_continue', change_continue, name='change_continue'),
)
