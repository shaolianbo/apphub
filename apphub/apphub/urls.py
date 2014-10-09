from django.conf.urls import patterns, include, url

from app_api.urls import router

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls))
)
