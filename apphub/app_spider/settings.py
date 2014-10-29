# -*- coding: utf-8 -*-

# Scrapy settings for app_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# init Django
import os

import django

profile = os.environ.setdefault("APPHUB_PROFILE", "dev")
os.environ['DJANGO_SETTINGS_MODULE'] = 'apphub.settings.%s' % profile

django.setup()

# scrapy
from django.conf import settings

IMAGES_STORE = settings.MEDIA_ROOT

BOT_NAME = 'app_spider'

SPIDER_MODULES = [
    'app_spider.spiders'
]
NEWSPIDER_MODULE = 'app_spider.spiders'

COOKIES_ENABLED = True


# config defer from profiles

if profile in ['dev', 'test']:
    ITEM_PIPELINES = {
        'app_spider.pipelines.FilterPipeline': 50,
        'app_spider.pipelines.StoreAppPipeline': 100,
    }
    APK_DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'apks')
else:
    ITEM_PIPELINES = {
        'app_spider.pipelines.FilterPipeline': 50,
        'app_spider.pipelines.AppImagePipeline': 60,
        'app_spider.pipelines.StoreAppPipeline': 100,
    }

if profile in ['test', 'product']:
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'info.log')
    LOG_STDOUT = True
    DATA_SYNC_API = "http://10.10.93.39:10100/api/sync_from_spider"
else:
    DATA_SYNC_API = 'http://0.0.0.0:8000/api/sync_from_spider'

DOWNLOAD_DELAY = 0.25

# custome configure

IS_INSERT_DORAEMON = False
