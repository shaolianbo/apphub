# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from scrapy.exceptions import DropItem
from scrapy import log

from app_spider.spiders.coolapk_list_spider import CoolApkListSpider
from store.models import AppInfo


class AppSpiderStorePipeline(object):
    def process_item(self, item, spider):
        if isinstance(spider, CoolApkListSpider):
            if not AppInfo.objects.filter(apk_name__exact=item['apk_name']).exists():
                item.save()
                log.msg('add AppInfo %s' % item, level=log.INFO)
                return item
            else:
                raise DropItem("Duplicate AppItem: %s" % item)
        else:
            return item
