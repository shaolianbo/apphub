# encoding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.core.management.base import BaseCommand
import requests
from requests import RequestException

from store.models import Category, AppInfo, Game


class Command(BaseCommand):
    #    option_list = BaseCommand.option_list + (
    #        make_option('--apks',
    #                    dest='apks',
    #                    default=None,
    #                    help='apk名称列表. 名称之间用逗号分隔'
    #                    ),
    #        make_option('--top_type',
    #                    dest='top_type',
    #                    default=APP,
    #                    help='app类型(1:应用, 2:游戏), 默认为应用'
    #                    ),
    #    )
    def handle(self, *args, **options):
        for category in Category.objects.filter(top_type=Game):
            apk_names = AppInfo.objects.filter(category=category, is_crawled=True, data_source=AppInfo.WANDOUJIA).values_list('app_id__apk_name')[:20]
            for item in apk_names:
                self._sync(item[0])

    def _sync(self, apk_name):
        url = "%s/?apk_name=%s&insert=1" % (settings.DATA_SYNC_API, apk_name)
        try:
            resp = requests.get(url)
        except RequestException as e:
            print "sync %s to Doraemon web error: %s" % (apk_name, e)
            return False
        if resp.status_code != 200:
            print "sync %s to Doraemon failed: %s" % (apk_name, resp.content)
            return False
        if resp.json()['success']:
            print "sync %s to Doraemon success" % apk_name
            return True
        else:
            print 'sync %s to Doraemon failed' % apk_name
            return False
