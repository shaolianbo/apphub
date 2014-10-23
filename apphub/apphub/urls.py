from django.conf.urls import patterns, include, url

from app_api.urls import router


urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^spider/', include('app_spider.urls', namespace='spider'))
)
