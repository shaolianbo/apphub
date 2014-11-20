# -*- coding: utf-8 -*-

# Scrapy settings for app_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#


# scrapy
BOT_NAME = 'app_spider'

SPIDER_MODULES = [
    'app_spider.spiders'
]
NEWSPIDER_MODULE = 'app_spider.spiders'

COOKIES_ENABLED = True

ITEM_PIPELINES = {
    'app_spider.pipelines.FilterPipeline': 50,
    'app_spider.pipelines.StoreAppPipeline': 100,
}

DOWNLOAD_DELAY = 0.25

# custome configure

FORCE_UPDATE = 0

# init Django
import os

import django

profile = os.environ.setdefault("APPHUB_PROFILE", "dev")
os.environ['DJANGO_SETTINGS_MODULE'] = 'apphub.settings.%s' % profile

django.setup()

# different config because of profile
if profile == 'dev':
    DATA_SYNC_API = 'http://0.0.0.0:8000/api/sync_from_spider'

if profile == 'test':
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'info.log')
    LOG_STDOUT = True
    LOG_LEVEL = 'INFO'
    DATA_SYNC_API = "http://t1.ams.sohuno.com/api/sync_from_spider"
