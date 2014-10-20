# coding:utf8
from __future__ import unicode_literals

from scrapy.exceptions import NotConfigured

from app_spider.signals import appinfo_saved


class CrawlResult(object):
    """
    激活条件: APP_CRAWL_RESULT_ENABLED = True
    """
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('APP_CRAWL_RESULT_ENABLED'):
            raise NotConfigured
        o = cls(crawler.stats)
        crawler.signals.connect(o.appinfo_saved, signal=appinfo_saved)
        return o

    def appinfo_saved(self, spider):
        self.stats.set_value('appinfo_saved', True, spider=spider)
