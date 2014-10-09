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
profile = os.environ.setdefault("APPHUB_PROFILE", "dev")
# TODO: 如果必要的话,根据profile加载django配置文件
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcrawler.settings.%s" % profile)
os.environ['DJANGO_SETTINGS_MODULE'] = 'apphub.settings'

import django
django.setup()

BOT_NAME = 'app_spider'

# scrapy

SPIDER_MODULES = [
    'app_spider.spiders'
]
NEWSPIDER_MODULE = 'app_spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'app_spider (+http://www.yourdomain.com)'

if profile in ['dev', 'test']:
    ITEM_PIPELINES = {
        'app_spider.pipelines.StoreAppPipeline': 100,
    }
else:
    ITEM_PIPELINES = {
        'app_spider.pipelines.AppImagePipeline': 1,
        'app_spider.pipelines.StoreAppPipeline': 100,
    }

LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'info.log')
LOG_STDOUT = True
COOKIES_ENABLED = False

from apphub.settings import MEDIA_ROOT

IMAGES_STORE = MEDIA_ROOT
