# encoding: utf-8
from __future__ import unicode_literals
import json

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from app_spider import settings as spider_setting
from app_spider.spiders.wandoujia.wandoujia_detail_spider import WandoujiaDetailSpider


class Command(object):
    def handle(self, *args, **options):
        self.spider = WandoujiaDetailSpider(apk_name='com.douban.radio')
        settings = get_project_settings()
        self.crawler = Crawler(settings)
        self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        self.crawler.signals.connect(self.on_spider_idle, signal=signals.spider_idle)
        self.crawler.configure()
        self.crawler.crawl(self.spider)
        self.crawler.start()
        log.start()
        reactor.run()

    def on_spider_idle(self):
        log.msg(json.dumps(self.crawler.stats.get_stats()), log.WARNING)


c = Command()
c.handle()
