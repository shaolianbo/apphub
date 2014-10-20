# encoding: utf-8
from __future__ import unicode_literals
import json
from datetime import datetime

from optparse import make_option
from django.core.management.base import BaseCommand
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from multiprocessing.queues import Queue
import multiprocessing

from app_spider.spiders.wandoujia.wandoujia_detail_spider import WandoujiaDetailSpider


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


class CrawlerWorker(multiprocessing.Process):

    def __init__(self, apk_name, result_queue):
        super(CrawlerWorker, self).__init__()
        self.result_queue = result_queue
        # spider
        spider = WandoujiaDetailSpider(apk_name=apk_name)
        settings = get_project_settings()
        self.crawler = Crawler(settings)
        self.crawler.settings.set('APP_CRAWL_RESULT_ENABLED', True)
        self.crawler.signals.connect(self.on_spider_close, signal=signals.spider_closed)
        self.crawler.configure()
        self.crawler.crawl(spider)
        self.crawler.start()
        log.start()

    def on_spider_close(self, spider, reason):
        self.crawler.stats.set_value('finish_time', datetime.utcnow(), spider=spider)
        self.crawler.stats.set_value('finish_reason', reason, spider=spider)
        self.result_queue.put(self.crawler.stats.get_stats())
        #log.msg(json.dumps(self.crawler.stats.get_stats(), cls=DateTimeEncoder), log.WARNING)
        reactor.stop()

    def run(self):
        reactor.run()


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--apk',
                    dest='apk',
                    default=None,
                    help=''
                    ),
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        result = None
        result_queue = Queue()
        crawler = CrawlerWorker('com.douban.radio', result_queue)
        crawler.start()
        result = result_queue.get()
        crawler.join()
        return result
