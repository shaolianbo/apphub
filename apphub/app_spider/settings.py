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

ITEM_PIPELINES = {
    'app_spider.pipelines.StoreAppPipeline': 100,
}

LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
